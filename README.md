# CS2 Trade-up Contracts Optimizer

优化汰换合同  
A small Python project for analyzing and optimizing CS2 trade-up contracts. This repository contains data, scrapers, utilities, and optimization code used to evaluate and search for desirable trade-up outcomes.

## Key Features

- Data ingestion and simple scrapers for building datasets.
- Optimization utilities (genetic algorithm fitness, helpers) in `src/cs2/optimize`.
- Notebooks for inspecting data and exploratory analysis in `notebooks/`.

## File structure

Below is the repository layout and a short description for key files and folders:

```
├─ README.md                       # This file
├─ pyproject.toml                   # Python project metadata and dependencies
├─ data/                            # Raw and processed data
├─ notebooks/                       # Jupyter notebooks for exploration
├─ src/
│  └─ cs2/
│     ├─ config.py                  # Crawler configuration and constants
│     ├─ data_model/
│     ├─ optimize/                  # Optimization implementation
│     └─ scrape/
└─ tests/                           # Unit/integration tests

```
