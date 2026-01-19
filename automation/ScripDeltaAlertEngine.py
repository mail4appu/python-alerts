import time
from datetime import datetime

import winsound

import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By

from plyer import notification




class ScripDeltaAlertEngine:
    losers=False
    last_fetched_trading_scrips=None

    def __init__(self):

        self.last_fetched_trading_scrips=set()
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
        delta=set()
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
            if len(self.last_fetched_trading_scrips)==0:
                print(f"====================Scrips To Trade================================\n{data}\n===================================================================")
            current_scrips=set(data.split(", "))
            if len(self.last_fetched_trading_scrips) == 0:
                self.last_fetched_trading_scrips=current_scrips
            print("Number of last fetched symbols:", len(self.last_fetched_trading_scrips))
            print("Number of current symbols:", len(current_scrips))
            if self.last_fetched_trading_scrips:
                delta = current_scrips - self.last_fetched_trading_scrips
                print(f"Delta between last vs current {delta}")
                if delta:
                    current_time = datetime.now()
                    present_time = current_time.strftime("%H:%M:%S")
                    copy_delta = delta.copy()
                    for x in copy_delta:
                        if x in self.last_fetched_trading_scrips:
                            delta.remove(x)
                    if len(delta) > 0:
                        print(f"New scrips different from current trading scrips found at {present_time} ", delta)
                        winsound.Beep(1200, 300)
                        self.send_notification("New Scrips", delta)
                else:
                    print("No new scrips found")

            if len(delta)>0:
                self.last_fetched_trading_scrips.update(delta)
            print("Going for refresh")
            now = datetime.now()
            if now.hour==15 and now.minute >= 5:
                break
            time.sleep(120)
        print(f"ITS TIME UP FOR THE DAY. HENCE CLOSING")
        self.driver.quit()


    def send_notification(self, title, new_symbols, timeout=0):
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





