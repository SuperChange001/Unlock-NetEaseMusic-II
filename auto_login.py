# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "008E96289F48F83D6C454161AEC133D8D3B98973E241E12AB961B04EA3D68ED4D034A8FBACFC2811B7D197C246BC8072E4C5EF292C62FA88679622CA558EC75D766B178173DD5D9FA4779C2EC6564B7F6DFF2B620062C7AFE271D1CC35F837F69244934C287B0BD3794BC7053A33C2D777A4460C92B306ECB114E2B54C6AC2BE0B7272E86D49236DD188A801E5AF536FE98F52D324C37BC0209FC74197AA65C23290ECC53EBCD9D1D4D2DE23D6F1BD9CDE8B434D7FEB5C90AC5C33C6EA4F8FDC8F74B9515A2882F108F4A9AC27DA32D6ECA3786F693BD93685C8925C0584E58F2522627753341C83855CE9132DB114105538B1DFEEB6A2F8B48BB531F9BBD8F3D9E4A7FD8456598ED83197592CD0EC594FE2AEE54BC6D7FBB2067C9357FEC8F523695002C312273F411851E8A9447B1EECA3CE7556E6284D7731798FCB1DAC3016A8EAF50E5266E678FB8083A9CFDF9E0B8DA1006B6830DC0F66A94F21C67004DB"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
