import datetime
import time
from tkinter import messagebox
import tkinter
from httpcore import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import json
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from getpass import getpass
from collections import defaultdict
import os


start_time = datetime.datetime.now()

def sleep(seconds):
    time.sleep(seconds)


fetch_report = []

# Read environment variables
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Check if the variables were read successfully
if username is None or password is None:
    raise Exception("Please set USERNAME and PASSWORD in the .env file.")


xpath_iframe_complete = "/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/force-aloha-page/div/iframe"
xpath_iframe = "/html/body/div/div[2]/div/div[4]/div[2]/div/div[3]/select"
iframe_name= "vfFrameId_1687454956510"



with open('./LOCATIONS.json') as f:
    location_code_for_each_city = json.load(f)

def confirmation():
    root = tkinter.Tk()
    root.withdraw()  # Hide the main window
    print("Waiting for Login confirmation...")
    result = messagebox.askokcancel("Confirmation", "Wait untill the Login process is finished, close any popups and press OK")
    root.destroy()  # Destroy the main window
    return result

def select_site(driver, site_name):
    """
    Selects the site from the dropdown menu
    """

    try:
        time.sleep(1)
        # Store iframe web element
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_iframe_complete)))
        iframe = driver.find_element(By.XPATH, xpath_iframe_complete)
        # switch to selected iframe
        driver.switch_to.frame(iframe)
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.col-lg-3 > select')))
        dropdown = Select(driver.find_element(By.CSS_SELECTOR, 'div.col-lg-3 > select'))
        dropdown.select_by_visible_text(site_name)
               
        # option_list = dropdown.options
           
        time.sleep(2)
    except Exception as e:
        print(e)
        return False
    return True
    
def click_100_views_button(driver):
    """
    Clicks the button that changes the number of views to 100

    """
    try:

        button = driver.find_element(By.XPATH, '//button[@type="button" and @ng-click="params.count(100)"]')
        button.click()
        return True
    except Exception as e:
        print(f"Error: Button not found\n{e}")
        return False
def click_next_page_button(driver):
    """
    Clicks the button to go to the next page
    """
    try:
        # Wait until the next page button is located
        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "next")]/a')))
        next_button.click()
        return True
    except TimeoutException as e:
        print(f"Info: No next page button found. It seems we've reached the end of the pages.\n{e}")
        return False
    except Exception as e:
        print(f"Error: Next page button not found\n{e}")
        return False

    
def get_table_data(driver):
    to_report = {
        "site": "",
        "function_name": "get_table_data",
        "status": ""
    }
    table_data = []
    try:
        sleep(2)
        rows = driver.find_elements(By.TAG_NAME, 'tr')

        for row in rows:
            row_dict = {}
            cells = row.find_elements(By.TAG_NAME, 'td')
            for cell in cells:
                key = cell.get_attribute('data-title-text')
                value = cell.text
                if key in ["Address", "Status", "DSA", "Consent", "Follow Up"]:
                    row_dict[key] = value
            table_data.append(row_dict)
        return table_data
    except Exception as e:
        print(f"Error: Table not found\n{e}")
        return False

def clean_data(data):
    cleaned_data = defaultdict(lambda: {"streets": set(), "houses": []})
    for row in data:
        dsa = row.get('DSA')
        status = row.get('Status')
        consent = row.get('Consent')
        street_name = row.get('Street Name')
        cleaned_data[dsa]["streets"].add(street_name)
        cleaned_data[dsa]["houses"].append(
            {
                "streetNumber": row.get('Number'),
                "lastName": None,
                "name": None,
                "phoneOrEmail": None,
                "notes": None,
                "statusAttempt": status,
                "consent": consent,
                "type": None,
                "street": street_name
            }
        )

    output = []
    for dsa, info in cleaned_data.items():
        output.append({
            "name": dsa,
            "neighborhood": "to be verified",
            "priorityStatus": 1,
            "houses": info["houses"],
            "streets": list(info["streets"])  # convert set back to list for JSON serialization
        })
    return output


def fetch_site_data(driver, site_name):
    to_report = {
        "site": site_name,
        "function_name": "fetch_site_data",
        "status": "",
    }
    table_data = []
    click_100_views_button(driver)
    while True:
        try:
            page_data = get_table_data(driver)
            for row in page_data:
                address = row.get('Address')  
                if address:  
                    parts = address.split()
                    number = parts[0]
                    street_name = ' '.join(parts[1:])
                    row['Number'] = number 
                    row['Street Name'] = street_name
                    table_data.append(row)
        except Exception as e:
            message = f'\nNot able to fetch data from site: {site_name}\n{e}'
            to_report["status"] = message

            fetch_report.append(to_report)
            print(message)
            break        
        try:
            next_buttons = driver.find_element(By.XPATH, '//li[contains(@class, "next")]/a')
            next_buttons.click()
            sleep(2)
        except Exception as e:
            print(f"Info: No next page button found. It seems we've reached the end of the pages.\n{e}")
            break
        message = f'\nFetched data from site: {site_name} successfully\n'
        to_report["status"] = message
        fetch_report.append(to_report)

    return table_data
  





service = Service("C:/Users/yalme/Desktop/gate/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get('https://bellconsent.my.salesforce.com/?ec=302&startURL=%2Fvisualforce%2Fsession%3Furl%3Dhttps%253A%252F%252Fbellconsent.lightning.force.com%252Flightning%252Fn%252FBell')


username_box = driver.find_element(By.NAME, 'username')  
password_box = driver.find_element(By.NAME, 'pw')  

username_box.send_keys(username)

password_box.send_keys(password)


login_button = driver.find_element(By.NAME, 'Login')  


login_button.click()

sleep(2)


if confirmation():
    sleep(3)
    print("Initializing Location fetching progress...")
    for site in location_code_for_each_city["toronto"]:
        to_report = {
            "site": site,
            "function_name": "main",
            "status": "",
        }
        select_site(driver, site)
        sleep(2)
        try:
            cleaned_data = clean_data(fetch_site_data(driver, site))
            with open(f'{site}.json', 'w') as f:
                json.dump(cleaned_data, f, indent=4)
                f.close()
            message = f"\nData saved to {site}.json\n"
            to_report["status"] = message
            fetch_report.append(to_report)
            driver.refresh()
            sleep(2)
        except Exception as e:
            message = f"Error: Data not saved to {site}.json\n{e}"
            to_report["status"] = message
            fetch_report.append(to_report)
            driver.refresh()
            sleep(2)
    driver.close()



end_time = datetime.datetime.now()

script_duration =  start_time - end_time


fetch_report.append({ str(script_duration): script_duration.total_seconds() })


with open('fetch_report.json', 'w') as f:
    json.dump(fetch_report, f, indent=4)
    f.close()
  

 
