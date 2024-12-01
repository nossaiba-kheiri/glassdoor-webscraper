# Glassdoor Web Scraper for ADM Salaries

This project is a web scraper developed as part of the labor analysis for Archer Daniels Midland (ADM) in my Fundamental Analysis class. The goal of the scraper is to gather salary data for various roles at ADM from Glassdoor to aid in analyzing labor costs and trends.

---

## Table of Contents
1. [Overview](#overview)
2. [Technologies Used](#technologies-used)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [License](#license)
7. [Acknowledgments](#acknowledgments)

---

## Overview
This web scraper automates the process of collecting salary data from Glassdoor for ADM. The collected data includes:
- Job Titles
- Salary Ranges
- Open Job Counts

The scraper navigates through multiple pages of results to collect all relevant data, saving it to a CSV file for further analysis.

---

## Technologies Used
- **Python**: Core programming language
- **Selenium**: For web automation and scraping
- **Pandas**: For data manipulation and storage
- **Dotenv**: For managing sensitive environment variables
- **ChromeDriver**: For automating the Chrome browser

---

## Features
- Automated login to Glassdoor using environment variables for secure authentication.
- Scrapes job titles, salary ranges, and open job counts.
- Iterates through multiple pages of results.
- Saves the scraped data to a CSV file.

---

## Installation

### Prerequisites
1. **Python 3.7+** installed on your system.
2. **Google Chrome** browser installed.
3. **ChromeDriver** installed and available in your PATH. Download it from [here](https://chromedriver.chromium.org/downloads).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/nossaiba-kheiri/glassdoor-webscraper.git
   cd glassdoor-webscraper
