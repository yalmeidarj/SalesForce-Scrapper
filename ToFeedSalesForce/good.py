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


start_time = datetime.datetime.now()


def sleep(seconds):
    time.sleep(seconds)


fetch_report = []


username = "yalmeida.rj@gmail.com"
password = "rYeEsydWN!8808168eXkA9gV47A"

xpath_iframe_complete = "/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/force-aloha-page/div/iframe"
xpath_iframe = "/html/body/div/div[2]/div/div[4]/div[2]/div/div[3]/select"
iframe_name = "vfFrameId_1687454956510"


# for testing
test_location = 'ORLNON06_1012A'

ottawa = ["JKVLON", "KNTAON", "ORLNON", "OTWAON", "STSVON"]
toronto = ["AURRON", "GMLYON", "KNBGON", "MAPLON", "RMHLON", "SFVLON", "STTNON",
           "TNHLON", "WDBGON", "BRKLON", "ORONON", "PCNGON", "PTPYON", "WTBYON"]

toronto_codes = []
ottawa_codes = []

with open('./2beUpdated.json') as f:
    location_code_for_each_city = json.load(f)


def confirmation():
    root = tkinter.Tk()
    root.withdraw()  # Hide the main window
    print("Waiting for Login confirmation...")
    result = messagebox.askokcancel(
        "Confirmation", "Wait untill the Login process is finished, close any popups and press OK")
    root.destroy()  # Destroy the main window
    return result


def click_100_views_button(driver):
    """
    Clicks the button that changes the number of views to 100
    """
    try:
        # Wait for the button to be clickable (up to 10 seconds)
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@type="button" and @ng-click="params.count(100)"]'))
        )

        button.click()
        return True
    except Exception as e:
        print(f"Error: Button not found\n{e}")
        return False


def select_site(driver, site_name):
    """
    Selects the site from the dropdown menu
    """

    try:
        time.sleep(1)
        # Store iframe web element
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_iframe_complete)))
        iframe = driver.find_element(By.XPATH, xpath_iframe_complete)
        # switch to selected iframe
        driver.switch_to.frame(iframe)
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.col-lg-3 > select')))
        dropdown = Select(driver.find_element(
            By.CSS_SELECTOR, 'div.col-lg-3 > select'))
        dropdown.select_by_visible_text(site_name)

        # option_list = dropdown.options

        time.sleep(2)
    except Exception as e:
        print(e)
        return False
    return True


def get_table_rows_data(driver):

    to_report = {
        "site": "",
        "function_name": "get_table_data",
        "status": ""
    }

    table_data = []

    try:
        # Wait for the table rows to be present (up to 10 seconds)
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//tbody[@ng-repeat="item in $data"]/tr'))
        )

        # Iterate through each row
        for row in rows:
            # Get all columns (cells) of the row
            columns = row.find_elements(By.TAG_NAME, 'td')

            # Extract text from each column (cell)
            address = columns[0].text
            status = columns[1].text
            dsa = columns[2].text
            consent = columns[3].text
            follow_up = columns[4].text

            # Append data to the result
            table_data.append({
                "Address": address,
                "Status": status,
                "DSA": dsa,
                "Consent": consent,
                "Follow Up": follow_up
            })

        to_report["status"] = "Success"

    except Exception as e:
        print(f"An error occurred: {e}")
        to_report["status"] = "Failed"
        return to_report

    return table_data


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
            page_data = get_table_rows_data(driver)
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
            next_buttons = driver.find_element(
                By.XPATH, '//li[contains(@class, "next")]/a')
            next_buttons.click()
            sleep(2)
        except Exception as e:
            print(
                f"Info: No next page button found. It seems we've reached the end of the pages.\n{e}")
            break
        message = f'\nFetched data from site: {site_name} successfully\n'
        to_report["status"] = message
        fetch_report.append(to_report)

    return table_data


def clean_data(data):
    cleaned_data = defaultdict(lambda: {"streets": set(), "houses": []})
    for row in data:
        dsa = row.get('DSA')
        street_name = row.get('Street Name')
        status = row.get('Status')
        consent = row.get('Consent')
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
            # convert set back to list for JSON serialization
            "streets": list(info["streets"])
        })
    return output


service = Service("C:/Users/yalme/Desktop/gate/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# driver.get("file:///C:/Users/yalme/Desktop/Start/Bell/vanilla/index.html")
driver.get('https://bellconsent.my.salesforce.com/?ec=302&startURL=%2Fvisualforce%2Fsession%3Furl%3Dhttps%253A%252F%252Fbellconsent.lightning.force.com%252Flightning%252Fn%252FBell')


sleep(3)

# Replace 'username' with the actual element name
username_box = driver.find_element(By.NAME, 'username')
# Replace 'password' with the actual element name
password_box = driver.find_element(By.NAME, 'pw')

username_box.send_keys(username)
sleep(2)
password_box.send_keys(password)

sleep(1)

# Replace 'Login' with the actual element name
login_button = driver.find_element(By.NAME, 'Login')


login_button.click()

sleep(2)


if confirmation():
    print("Initializing Location fetching progress...")
    sleep(3)
    for site in location_code_for_each_city["toronto"]:
        select_site(driver, site)
        try:
            # Save to JSON file
            with open(f'{site}.json', 'w') as f:
                json.dump(clean_data(fetch_site_data(
                    driver, site)), f, indent=4)
                f.close()
            message = f"\nData saved to {site}.json\n"
            print(message)
            driver.refresh()
            # return True
        except Exception as e:
            message = f'\nData fetched, but error occurred when trying to save data for: {site}\n{e}'
            print(message)

driver.quit()
