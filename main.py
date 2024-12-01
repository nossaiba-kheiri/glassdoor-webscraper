from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from remove_overlay import get_overlay_removal_script
from dotenv import load_dotenv
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
username = os.getenv('GLASSDOOR_USERNAME')
password = os.getenv('GLASSDOOR_PASSWORD')

# Configure Chrome options
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service('/opt/homebrew/bin/chromedriver', port=9515)  # Specify the port
driver = webdriver.Chrome(service=service, options=chrome_options)

def login_to_glassdoor(driver, url, username, password):
    try:
        driver.get(url)
        time.sleep(5)  # Allow page to load

        # Fill in login details
        email = driver.find_element(By.ID, "userEmail")
        email.send_keys(username)  
        password_element = driver.find_element(By.ID, "userPassword")
        password_element.send_keys(password)  
        password_element.send_keys(Keys.RETURN)

        time.sleep(5)  # Allow login to complete
        logging.info("Logged in successfully")
    except Exception as e:
        logging.error(f"Error during login: {e}")

def scrape_salaries(driver, url):
    driver.get(url)
    time.sleep(5)  # Allow page to load
    logging.info(f"Current URL: {driver.current_url}")
    salaries = []
    while True: 
        try:
            # Wait for the table to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.salarylist_salary-table__rZfcR"))
            )
            logging.info("Table found successfully!")

            # Find all rows in the table body
            rows = driver.find_elements(By.CSS_SELECTOR, "table.salarylist_salary-table__rZfcR tbody tr")
            logging.info(f"Total rows detected (including header): {len(rows)}")


            for i, row in enumerate(rows):
                # Skip the first row (header)
                if i == 0:
                    logging.info("Skipping header row...")
                    continue

                try:
                    # Extract columns
                    job_title_element = row.find_element(By.CSS_SELECTOR, "td[data-testid='jobTitle'] a")
                    total_pay_element = row.find_element(By.CSS_SELECTOR, "td[data-testid='totalComp'] p.salarylist_total-pay-range__ECY78")
                    open_jobs_element = row.find_element(By.CSS_SELECTOR, "td[data-testid='totalComp'] ~ td a")

                    # Get text data
                    job_title = job_title_element.text
                    salary_range = total_pay_element.text
                    open_jobs = open_jobs_element.text if open_jobs_element else "N/A"

                    # Append data to list
                    salaries.append({
                        "Job Title": job_title,
                        "Salary Range": salary_range,
                        "Open Jobs": open_jobs,
                    })
                except Exception as e:
                    logging.error(f"Error processing row {i}: {e}")

            logging.info(f"Scraped {len(salaries)} rows (excluding header).")
            try:
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="next-page"]'))
                    )
                    next_button.click()
                    WebDriverWait(driver, 10).until(
                        lambda d: d.current_url != current_url  # Wait until URL changes
                    )
                    current_url = driver.current_url  # Update the current URL
            except TimeoutException:
                print("No more pages to scrape.")
                break
        except Exception as e:
            logging.error(f"Error during scraping: {e}")
            continue
            
        
        
        return salaries

def save_to_csv(salaries, filename):
    try:
        df = pd.DataFrame(salaries)
        df.to_csv(filename, index=False)
        logging.info(f"Data saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

def main():
    login_url = "https://www.glassdoor.com/profile/login_input.htm"
    salaries_url = "https://www.glassdoor.com/Salary/ADM-Salaries-E55.htm"
    filename = "ADM_Salaries.csv"

    #login_to_glassdoor(driver, login_url, username, password)
    salaries = scrape_salaries(driver, salaries_url)
    save_to_csv(salaries, filename)

    driver.quit()

if __name__ == "__main__":
    main()