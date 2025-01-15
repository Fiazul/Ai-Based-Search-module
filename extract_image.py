"""
This is not related to this project. I am here just collecting some images from random
 sites using selenium
 just for showing them in frontend after the search.
"""
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import requests
from selenium.common.exceptions import StaleElementReferenceException
import sqlite3
import sqlite3
import logging
import hashlib
from colander import colander_images
from config import emailp, passwordp
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def setup_driver():
    chrome_options = Options()
    base_dir = os.getcwd()
    driver_dir = os.path.join(base_dir, "driver")
    downloaded_driver_path = os.path.join(driver_dir, "chromedriver.exe")
    os.makedirs(driver_dir, exist_ok=True)

    def find_chromedriver():
        if os.path.exists(downloaded_driver_path):
            return downloaded_driver_path
        return None

    chrome_driver_path = find_chromedriver()
    if chrome_driver_path:
        service = Service(executable_path=chrome_driver_path)
    else:
        downloaded_path = ChromeDriverManager().install()
        try:
            shutil.move(downloaded_path, downloaded_driver_path)
        except Exception as e:
            print(f"Error moving ChromeDriver: {e}")
            raise
        service = Service(executable_path=downloaded_driver_path)

    return webdriver.Chrome(service=service, options=chrome_options)


def random_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))


def login_to_pinterest(driver, username, password):
    driver.get('https://www.pinterest.com/login')
    random_delay()
    driver.implicitly_wait(10)

    username_input = driver.find_element(By.XPATH, '//*[@id="email"]')
    username_input.send_keys(username)
    random_delay()
    password_input = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_input.send_keys(password)
    random_delay()

    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()
    random_delay()
    driver.implicitly_wait(10)


def open_new_tab(driver, url):
    try:
        driver.execute_script(f"window.open('{url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
    except Exception as e:
        logging.error(f"Error opening new tab with URL {url}: {e}")


def get_images(driver):
    try:
        div_role_list = driver.find_element(
            By.XPATH, '//div[@role="list"]')
        return div_role_list.find_elements(By.TAG_NAME, 'img')
    except StaleElementReferenceException:
        logging.warning(
            "StaleElementReferenceException encountered, retrying get_images()")
        return get_images(driver)
    except NoSuchElementException as e:
        logging.error(f"Error finding elements in get_images: {e}")
        return []


def collect_image(driver, url):
    try:
        open_new_tab(
            driver, 'https://www.pinterest.com/pin-builder/?tab=save_from_url')

        url_input = driver.find_element(
            By.XPATH, '//*[@id="scrape-view-website-link"]')
        url_input.clear()
        url_input.send_keys(url)
        random_delay()

        submit_button = driver.find_element(
            By.XPATH, '//button[@aria-label="Submit"]')
        submit_button.click()
        random_delay(5, 10)
    except NoSuchElementException as e:
        logging.error(f"Error during Pinterest login: {e}")

    images = get_images(driver)
    media_folder = 'media'
    temp_media_folder = 'temp'
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)
    if not os.path.exists(temp_media_folder):
        os.makedirs(temp_media_folder)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    url_hash = hashlib.md5(url.encode()).hexdigest()

    for i, img in enumerate(images):
        src = img.get_attribute('src')
        if src:
            img_data = requests.get(src).content
            if img_data:
                temp_image_path = os.path.join(
                    temp_media_folder, f'{url_hash}_image_{i}.jpg')

                with open(temp_image_path, 'wb') as handler:
                    handler.write(img_data)
                try:
                    if colander_images(temp_image_path):
                        final_image_path = os.path.join(
                            media_folder, f'{url_hash}_image_{i}.jpg')
                        shutil.move(temp_image_path, final_image_path)
                        cursor.execute(
                            "INSERT INTO url_images (url, image_path) VALUES (?, ?)", (url, final_image_path))

                        random_delay()
                    else:
                        os.remove(temp_image_path)
                except Exception as e:
                    logging.error(
                        f"Error processing image {temp_image_path}: {e}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    driver = setup_driver()

    try:
        login_to_pinterest(driver, emailp, passwordp)
        random_delay()

        # Read URLs from urls.txt
        with open('urls.txt', 'r') as file:
            urls = [line.strip() for line in file.readlines()]

        for url in urls:
            collect_image(driver, url)
            time.sleep(5)
    finally:
        driver.quit()
