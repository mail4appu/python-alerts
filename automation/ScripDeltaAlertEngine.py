import time
import winsound

import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By




class ScripDeltaAlertEngine:
    losers=False

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.chartink.com/login")
        print("Title", self.driver.title)
        email_address = self.driver.find_element(By.ID, "login-email")
        email_address.send_keys("itsmevizapp@gmail.com")
        time.sleep(3)
        password = self.driver.find_element(By.ID, "login-password")
        password.send_keys("pulpen@viz1!")

        button = self.driver.find_element(By.XPATH, "//button/span[text()='Log in']")
        button.click()
        time.sleep(5)
        pass


    def refresh_and_copy(self):
        prev_symbols = set()
        # Stocks up by 2% daily and volume surge in last 15 mins
        while True:
            self.driver.get("https://chartink.com/screener/volume-surge-in-last-15-mins-for-raising-stocks")
            time.sleep(10)
            copy_button = self.driver.find_element(By.XPATH, "//span[text()='Copy']")
            copy_button.click()
            time.sleep(5)
            symbols_button = self.driver.find_element(By.XPATH, "//span[text()='symbols']")
            symbols_button.click()
            time.sleep(5)
            data=pyperclip.paste()
            current_symbols=set(data.splitlines())

            if prev_symbols:
                delta=current_symbols-prev_symbols
                if delta:
                    print("New scrips found", delta)
                    winsound.Beep(1200,300)

            prev_symbols=current_symbols
            time.sleep(100)




start_time= time.time()

scrip_delta_alert_engine= ScripDeltaAlertEngine()
scrip_delta_alert_engine.refresh_and_copy()




