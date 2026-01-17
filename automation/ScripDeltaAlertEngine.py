import time
from datetime import datetime

import winsound

import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By

from plyer import notification




class ScripDeltaAlertEngine:
    losers=False
    first_delta=None

    def __init__(self):
        self.first_delta=set()
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


    def refresh_and_find(self):
        last_fetched_scrips=set()

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
            if len(last_fetched_scrips)==0:
                print(f"====================Scrips To Trade================================\n{data}\n===================================================================")
            current_scrips=set(data.split(", "))
            print("Number of last fetched symbols:", len(last_fetched_scrips))
            print("Number of current symbols:", len(current_scrips))
            if last_fetched_scrips:
                delta=current_scrips-last_fetched_scrips
                print("Number of new symbols found ", len(delta))
                current_time=datetime.now()
                present_time=current_time.strftime("%H:%M:%S")
                if delta:
                    print(f"New scrips found at {present_time} ", delta)
                    if len(self.first_delta)==0:
                        self.first_delta.update(delta)
                        winsound.Beep(1200, 300)
                        self.send_notification("New Scrips", delta)
                    elif delta-self.first_delta:
                        winsound.Beep(1200, 300)
                        self.send_notification("New Scrips", self.first_delta.update(delta-self.first_delta))
                else:
                    print("No new scrips found")


            last_fetched_scrips=current_scrips
            print("Going for refresh")
            time.sleep(60)

    def send_notification(self, title, new_symbols, timeout=10):
        notification.notify(
            title=title,
            message=str(new_symbols),
            app_name="My Notifier",
            # Use an absolute path for the icon file (must be .ico on Windows)
            # app_icon="/path/to/my_icon.ico",
            timeout=timeout,
        )




start_time= time.time()

scrip_delta_alert_engine= ScripDeltaAlertEngine()
scrip_delta_alert_engine.refresh_and_find()





