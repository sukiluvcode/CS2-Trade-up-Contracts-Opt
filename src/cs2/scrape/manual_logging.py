# 手动登入悠悠有品账号
import time
from cs2.config import USER_DATA_DIR
from playwright.sync_api import sync_playwright


url = 'https://www.youpin898.com/market/'

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        # executable_path=chrome_path,
        headless=False,
        viewport={"width": 1920, "height": 1080},
    )
    time.sleep(60)
    context.close()
    