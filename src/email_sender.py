from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

# Load environment variables for email credentials
load_dotenv()

username = os.getenv("SENDER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")

driver_path = os.getenv("PATH_TO_CHROMEDRIVER")

def send_email(recipient_email, subject_text, email_body):
    # Initialize WebDriver (using Chrome in this example)
    service = Service(driver_path)  # Use Service to define the path to ChromeDriver
    driver = webdriver.Chrome(service=service)

    try:
        # Open the OWA (Outlook Web Access) URL
        driver.get("https://www.hsbi.de/login?target=https://www.hsbi.de/webmail/login")
        wait = WebDriverWait(driver, 20) 

        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        email_input.send_keys(username)

        # Find the password input field and enter the password
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_input.send_keys(password)

        # Submit the login form (either by pressing Enter or clicking login)
        password_input.send_keys(Keys.RETURN)

        new_email_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[1]/div/div[1]/div/div/div[1]/div/button[1]/span[1]')))
        new_email_button.click()

        # Enter recipient's email address
        to_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/div[3]/div[4]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div/span/div[1]/form/input')))
        to_field.send_keys(recipient_email)
        time.sleep(2)
        to_field.send_keys(Keys.RETURN)
        time.sleep(2)

        # Enter the subject of the email
        subject_field = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/div[3]/div[4]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[6]/div[2]/input')))
        subject_field.send_keys(subject_text)

        # Enter the email body content
        body_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/div[3]/div[4]/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div[1]/div[3]/div/p[1]')))
        body_field.send_keys(email_body)

        # Send the email
        send_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="primaryContainer"]/div[5]/div/div[1]/div/div[5]/div[3]/div/div[5]/div[1]/div/div[3]/div[5]/div/div[2]/div[1]/button[1]')))
        send_button.click()

        time.sleep(5)  # Wait for the email to be sent
        print("Email sent successfully!")
    finally:
        # Close the WebDriver after the task is completed
        driver.quit()
