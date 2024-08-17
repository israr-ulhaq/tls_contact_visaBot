import os
import pickle
import random
import time
from datetime import datetime

from selenium.common.exceptions import (ElementClickInterceptedException,
                                        TimeoutException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telegram import Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, filters)

from selenium import webdriver

# Load sensitive data from environment variables or configuration files
API_TOKEN = '' #telegramAPI
def human_like_delay():
    time.sleep(random.uniform(1.5, 3.0))  # Random delay

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I can help you find visa appointments.')

async def info(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /info is issued."""
    await update.message.reply_text('This is a simple Telegram bot implemented in Python.')

async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def search_appointments(update: Update, context: CallbackContext) -> None:
    result = ''
    while True:
        try:
            # Setup WebDriver
            chrome_options = Options()
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

            webdriver_service = Service('webdriver')  # Ensure this path is correct
            driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

            # Open the website
            driver.get('https://visas-de.tlscontact.com/visa/gb/gbLON2de/home') #You can change the url to required city
            human_like_delay()

            # Accept cookies
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'osano-cm-accept-all') and text()='Accept All']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", accept_button)
            human_like_delay()
            accept_button.click()
            print("Cookies accepted.")

            wait = WebDriverWait(driver, 20)
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'tls-button-link') and text()='Login']")))
            human_like_delay()
            login_button.click()
            print("Clicked on the Login button.")

            email_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
            email = ""  # Replace this with the actual email
            email_input.send_keys(email)
            human_like_delay()

            password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
            password = ""  # Replace this with the actual password
            password_input.send_keys(password)
            human_like_delay()

            submit_button = wait.until(EC.element_to_be_clickable((By.ID, "kc-login")))
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            driver.execute_script("arguments[0].click();", submit_button)
            human_like_delay()

            print("Login form submitted successfully.")
            pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

            # Click "Enter" button
            driver.execute_script("window.scrollTo(0, 500)")
            try:
                enter_button = driver.find_element(By.XPATH, '//button[@class="tls-button-primary button-neo-inside"]')
                enter_button.click()
                print("Clicked on the 'Enter' button successfully using custom JavaScript.")
            except:
                enter_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='tls-button-primary button-neo-inside']")))
                actions = ActionChains(driver)
                actions.move_to_element(enter_button).click().perform()
                print("Clicked on the 'Enter' button successfully using Action Chains.")

            # Click "Book appointment" button
            try:
                human_like_delay()
                driver.execute_script("window.scrollTo(0, 3000)")
                book_appointment_button = driver.find_element(By.XPATH, '//button[@class="button-neo-inside -primary"]')
                driver.execute_script("arguments[0].scrollIntoView(true);", book_appointment_button)
                book_appointment_button.click()
                human_like_delay()
            except:
                enter_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button-neo-inside -primary']")))
                actions = ActionChains(driver)
                actions.move_to_element(enter_button).click().perform()
                print("Clicked on the 'Book appointment' button successfully using Action Chains.")
                human_like_delay()

            # Check for available appointments
            try:
                no_appointments_popup = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='tls-button-primary -uppercase']")))
                print("No appointments available until: ", datetime.now().time())
                actions = ActionChains(driver)
                actions.move_to_element(no_appointments_popup).click().perform()
                # await update.message.reply_text("No appointments available. Retrying...")
                time.sleep(900)  # Wait 10 minutes before trying again
                continue  # Restart the loop and reinitialize WebDriver
            except:
                print("Checking for available appointments...")

            # If appointment is available
            try:
                available_appointment = driver.find_element(By.XPATH, "//button[contains(@class, '-available')]")
                if available_appointment:
                    print("Available appointment found!")
                    current_time = datetime.now().time()
                    result = f'Available appointment found at London {current_time}'
                    await update.message.reply_text(result)
                    available_appointment.click()
                    return True
            except:
                result = 'No appointments available yet.'
                print(result)
                await update.message.reply_text(result)
                time.sleep(60)
                continue
                
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {e}")

        finally:
            driver.quit()  # Ensure driver quits to reset the session and prevent errors when retrying

def main():
    """Start the bot."""
    application = Application.builder().token(API_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("search", search_appointments))  # New command to trigger Selenium task
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
