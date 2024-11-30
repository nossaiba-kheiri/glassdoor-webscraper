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

# Login to Glassdoor
url = "https://www.glassdoor.com/profile/login_input.htm"
try: 
    driver.get(url)
    time.sleep(5)  # Allow page to load

    # Fill in login details (replace with your credentials)
    email = driver.find_element(By.ID, "userEmail")
    email.send_keys(username)  # Replace with your email
    password = driver.find_element(By.ID, "userPassword")
    password.send_keys(password)  
    password.send_keys(Keys.RETURN)


    time.sleep(5)  # Allow login to complete
    

except: 
    url = "https://www.glassdoor.com/Salary/ADM-Salaries-E55.htm"
    driver.get(url)
    overlay_script = get_overlay_removal_script()
    driver.execute_script(overlay_script)

driver.get("https://www.glassdoor.com/Salary/ADM-Salaries-E55.htm")
time.sleep(5)  # Allow page to load
print(f"Current URL: {driver.current_url}")
print(driver.page_source)  # Save the page source to inspect manually
with open("page_source.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)
salaries = []
try:
    # Wait for the table to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.salarylist_salary-table__rZfcR"))
    )
    print("Table found successfully!")


    # Find all rows in the table body
    rows = driver.find_elements(By.CSS_SELECTOR, "table.salarylist_salary-table__rZfcR tbody tr")
    print(f"Total rows detected (including header): {len(rows)}")

    for i, row in enumerate(rows):
        # Skip the first row (header)
        if i == 0:
            print("Skipping header row...")
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
            print(f"Error processing row {i}: {e}")

    print(f"Scraped {len(salaries)} rows (excluding header).")
except Exception as e:
    print(f"Error during scraping: {e}")

# Save to CSV
df = pd.DataFrame(salaries)
df.to_csv("ADM_Salaries.csv", index=False)
print("Data saved to ADM_Salaries.csv")

# Close the browser
driver.quit()