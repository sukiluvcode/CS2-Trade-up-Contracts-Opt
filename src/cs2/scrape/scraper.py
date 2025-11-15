"""
Web scraper for youpin898.com market data.
Automates float range searches and saves response data.
"""

import logging
import time
import random
import json
import itertools
from typing import Optional

import numpy as np
from tqdm import tqdm
from playwright.sync_api import sync_playwright, Page, Response, TimeoutError, Error

from .throttle import Throttle, wait
from cs2.config import USER_DATA_DIR, OUTPUT_FILE  # user-specific values


# Configuration constants
TARGET_URL = 'https://www.youpin898.com/market/goods-list'

# CSS Selectors
FLOAT_RANGE_BUTTON = (
    '#rc-tabs-0-panel-sale > div > div:nth-child(1) > div > '
    'div.left-cont___jQJRq > div:nth-child(2)'
)
MIN_INPUT_SELECTOR = 'div.input-box___ENjgN > input[type="text"]:nth-child(1)'
MAX_INPUT_SELECTOR = 'div.input-box___ENjgN > input[type="text"]:nth-child(3)'

# throttler
throttler = Throttle(capacity=1, recovery_rate=0.4)  # 1 request per second

# logger
logger = logging.getLogger(__name__)
logger_file = 'scrape.log'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=logger_file)


def load_extracted_tuples(logger_file: str) -> set:
    """Load already extracted (id, min, max) tuples from log file."""
    extracted = set()
    extracted_ids = set()
    try:
        with open(logger_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            if "Success" in line:
                parts = line.split('\t')
                id_part = parts[0].split('id: ')[-1]
                if "full" in line:
                    extracted_ids.add(int(id_part))
                    continue
                range_part = parts[1].split('range: ')[-1]
                min_val, max_val = map(float, range_part.split('-'))
                extracted.add((int(id_part), min_val, max_val))
    except FileNotFoundError:
        pass
    return extracted, extracted_ids

class YouPin898Scraper:
    """Scraper for youpin898.com market commodity data."""
    
    def __init__(self, output_file: str = OUTPUT_FILE):
        self.output_file = output_file
        self.page: Optional[Page] = None
        self.extracted_tuples = set()
        self.extracted_ids = set()
        self.viewport_seed = self.gen_viewport_parameters()
        self.timeout_occurred_times = 0
        self.logging_format = "id: {id_}\trange: {min_float}-{max_float}\t{e}"
        self.logging_format_pagination = "id: {id_}\trange: full\t{e}"
    
    def save_response_data(self, response: Response) -> None:
        """
        Save the best data from API response to file.
        
        Args:
            response: The HTTP response object from the API
        """
        if response.status != 200:
            print(f"Warning: Response status {response.status}, skipping save")
            return
        
        data = response.json()
        if not data.get("Data"):
            # no data found
            return
        
        best_data = data["Data"][0]
        with open(self.output_file, encoding='utf-8', mode='a') as f:
            f.write(f"{json.dumps(best_data, ensure_ascii=False)}\n")
    
    def save_response_data_full_page(self, data) -> None:
        """
        Save the full API response data to file.
        
        Args:
            response: The HTTP response object from the API
        """
        if not data:
            # no data found
            return
        
        with open(self.output_file, encoding='utf-8', mode='a') as f:
            for d in data:
                f.write(f"{json.dumps(d, ensure_ascii=False)}\n")
            

    @wait(throttler)
    def set_float_range(self, min_float: float, max_float: float) -> None:
        """
        Set custom float range filter and capture the response.
        
        Args:
            min_float: Minimum float value
            max_float: Maximum float value
        """
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        id_ = self.page.url.split('templateId=')[-1]
        
        # Open float range dropdown
        self.page.locator(FLOAT_RANGE_BUTTON).click()
        
        # Select custom option
        self.page.locator("text=自定义").nth(0).click()
        
        # Fill in min and max values
        min_input = self.page.locator(MIN_INPUT_SELECTOR)
        max_input = self.page.locator(MAX_INPUT_SELECTOR)
        min_input.fill(str(min_float))
        max_input.fill(str(max_float))
        
        # Capture API response when confirming
        with self.page.expect_response(
            lambda r: "queryOnSaleCommodityList" in r.url and r.request.method == "POST"
        ) as response_info:
            self.page.locator('div.btn2___x8GlT:has-text("确认")').click()
        
        response = response_info.value
        self.save_response_data(response)

        logger.info(self.logging_format.format(id_=id_, min_float=min_float, max_float=max_float, e="Success"))
    
    def pagination_extract(self, id_):
        data_pages = []
        while True:
            throttler.wait_consume()
            # Check if next page button is disabled; if so, break the loop
            try:
                next_button = self.page.locator('div.paginationItem___cPDSU.next___CBWi0')
                btn_class = next_button.get_attribute('class')
                if btn_class and 'disabled___ncf6R' in btn_class:
                    break
                with self.page.expect_response(
                    lambda r: "queryOnSaleCommodityList" in r.url and r.request.method == "POST"
                ) as response_info:
                    next_button.click()
                response = response_info.value
                data_pages.extend(response.json()['Data'])
            except TimeoutError as e:
                if len(data_pages) > 10:
                    # inevitably some data is lost, but save what we have
                    self.save_response_data_full_page(data_pages)
                    logger.error(self.logging_format_pagination.format(id_=id_, e="Success")) 
                raise e

        self.save_response_data_full_page(data_pages)
        logger.info(self.logging_format_pagination.format(id_=id_, e="Success"))
        
    
    @staticmethod
    def get_url(yyid: int) -> tuple:
        """
        Get URL for a specific weapon by YYID.
        
        Args:
            yyid: The unique identifier for the weapon
            
        Returns:
            url 
        """
        s = f'?listType=10&templateId={yyid}'
        return TARGET_URL + s
    
    def yield_float_range(self, id_, min_val: float, max_val: float, step_size=0.01, drop_out=1.00):
        """
        Run multiple float range searches across a specified range.
        
        Args:
            min_val: Minimum float value to start from
            max_val: Maximum float value to end at
        """
        steps = (max_val - min_val) // step_size
        values = np.linspace(min_val, max_val, int(steps), endpoint=False)
        
        for start in values:
            # Skip already extracted ranges
            if (id_, round(start, 2), round(start + step_size, 2)) in self.extracted_tuples:
                continue
            if id_ in self.extracted_ids:
                continue
            if start >= drop_out:
                continue
            yield round(start, 2), round(start + step_size, 2)
    
    def scrape(self, id_min_maxs: list[tuple], flag=False) -> None:
        """Main scraping workflow."""
        # clean logic: initialize context with different viewport then reload uk value
        init_run = True
        while True:
            with sync_playwright() as playwright:
                # Launch browser with persistent context (keeps login state)
                width, height = next(self.viewport_seed)
                context = playwright.chromium.launch_persistent_context(
                    user_data_dir=USER_DATA_DIR,
                    headless=False,
                    viewport={'width': width, 'height': height},
                )

                self.extracted_tuples, self.extracted_ids = load_extracted_tuples(logger_file)

                for id_, min_val, max_val in tqdm(id_min_maxs):

                    float_range_l = list(self.yield_float_range(id_, min_val, max_val))
                    float_range_operations_count = len(float_range_l)
                    if not float_range_l:
                        continue

                    try:
                        self.page = context.new_page()
                        url = self.get_url(id_)
                        with self.page.expect_response(
                            lambda r: "queryOnSaleCommodityList" in r.url and r.request.method == "POST"
                        ) as response_info:
                            self.page.goto(url)
                            if flag or init_run:
                                self.clear_local_storage()
                                flag = False
                                init_run = False

                        response = response_info.value
                        total_count = response.json().get("TotalCount", 0)
        
                        # pagination logic
                        if total_count <= 10: # no need to do float range search
                            self.save_response_data_full_page(response.json()['Data'])
                            logger.info(self.logging_format_pagination.format(id_=id_, e="Success"))
                            continue
                        if total_count // 10 < float_range_operations_count or not self.page.query_selector(FLOAT_RANGE_BUTTON): # pagination is cheaper
                        
                            self.pagination_extract(id_=id_)

                        # float range logic
                        else:
                            for min_float, max_float in float_range_l:
                                    self.set_float_range(min_float, max_float)

                    except (TimeoutError, Error):
                            flag = True
                            time.sleep(3)  # Wait before retrying
                            self.timeout_occurred_times += 1
                            break  # break inner loop to reset local storage

                    finally:
                        if not self.page.is_closed():
                            self.page.close()

                    if flag:
                        break  # break outer loop to reset local storage

                context.close()

                if not flag:
                    logger.info(f"Completed all tasks with {self.timeout_occurred_times} timeouts.")
                    break  # exit while loop if no timeout occurred
    
    def clear_local_storage(self) -> None:
        """Clear local storage and reload the page."""
        if not self.page:
            raise RuntimeError("Page not initialized")
        if self.page.locator("text=SMS Login").is_visible():
            raise RuntimeError("Not logged in, please log in manually and restart.")
        original_uk = self.page.evaluate("window.localStorage.getItem('WEB_UK')")
        self.page.evaluate("localStorage.clear()")
        i = 0
        while True:
            if i > 5:
                raise RuntimeError("Failed to reload page after clearing local storage")
            i += 1
            try:
                self.page.reload()
                self.page.wait_for_load_state("networkidle")
            except TimeoutError:
                continue
            break
        now_uk = self.page.evaluate("window.localStorage.getItem('WEB_UK')")
        assert original_uk != now_uk, "Local storage clear failed, WEB_UK unchanged"
        assert now_uk is not None, "WEB_UK is None after clearing local storage"
        time.sleep(5)
    
    @staticmethod
    def gen_viewport_parameters():
        default_width = list(range(1901, 1920))
        default_height = list(range(1051, 1080))
        width_height_combinations = list(itertools.product(default_width, default_height))
        random.shuffle(width_height_combinations)
        for combo in itertools.cycle(width_height_combinations):
            yield combo
        

def read_yyid_file(file_path: str) -> list[tuple]:
    ts = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split('\t')
        id_ = parts[0]
        min_val, max_val = map(float, parts[1].split('-'))
        ts.append((int(id_), min_val, max_val))
    return ts

def main():
    """Entry point for the scraper."""
    scraper = YouPin898Scraper()
    id_min_maxs = read_yyid_file('yyid_high_tier_weapons.txt')
    scraper.scrape(id_min_maxs)


if __name__ == "__main__":
    main()
