import datetime
import time
from tkinter import messagebox
import tkinter
from httpcore import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv

import json
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from getpass import getpass
from collections import defaultdict
import os


start_time = datetime.datetime.now()


def read_csv_and_process(file_path):
    """
    # Reads a CSV file
    ## and processes its content into a list of dictionaries.
    Each dictionary contains information about a person, including their address,
    name, last name, phone number, email, type, and consent.

    Parameters:
    file_path (str): The path to the CSV file to read.

    Returns:
    list[dict]: A list of dictionaries, each containing information about a person.

    CSV file format:
    The CSV file should have the following headers:
    - streetNumber: The street number
    - street: The street name
    - name: The person's first name
    - lastName: The person's last name
    - phone: The phone number
    - email: The email address
    - type: The type or category
    - consent: The consent status
    """
    dataList = []
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {
                'streetNumber': row['streetNumber'],
                # Assuming 'street' contains the street name
                'streetName': row['street'],
                'name': row['name'],
                'lastName': row['lastName'],
                'phone': row['phone'],
                'email': row['email'],
                'type': row['type'],
                'consent': row['consent'],
                'location': row['location'],
            }
            dataList.append(data)
        return dataList


def sleep(seconds):
    time.sleep(seconds)


path_to_data_source_csv = './ToFeedSalesForce/generatedBy_small.csv'
data = read_csv_and_process(path_to_data_source_csv)
site_name = data[0]['location']
fetch_report = []
# Read environment variables
# username = os.getenv("USERNAME")
# password = os.getenv("PASSWORD")
username = "yalmeida.rj@gmail.com"
password = "rYeEsydWN!8808168eXkA9gV47A"


# Define a city to be fetched
city_to_fetch = 'toronto'

# Check if the variables were read successfully
if username is None or password is None:
    raise Exception("Please set USERNAME and PASSWORD in the .env file.")


xpath_iframe_complete = "/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/force-aloha-page/div/iframe"
xpath_iframe = "/html/body/div/div[2]/div/div[4]/div[2]/div/div[3]/select"
iframe_name = "vfFrameId_1687454956510"


# with open('./2beUpdated.json') as f:
#     location_code_for_each_city = json.load(f)


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

        button = driver.find_element(
            By.XPATH, '//button[@type="button" and @ng-click="params.count(100)"]')
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
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "next")]/a')))
        next_button.click()
        return True
    except TimeoutException as e:
        print(
            f"Info: No next page button found. It seems we've reached the end of the pages.\n{e}")
        return False
    except Exception as e:
        print(f"Error: Next page button not found\n{e}")
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


def click_100_views_button(driver):
    """
    Clicks the button that changes the number of views to 100

    """
    try:

        button = driver.find_element(
            By.XPATH, '//button[@type="button" and @ng-click="params.count(100)"]')
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
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "next")]/a')))
        next_button.click()
        return True
    except TimeoutException as e:
        print(
            f"Info: No next page button found. It seems we've reached the end of the pages.\n{e}")
        return False
    except Exception as e:
        print(f"Error: Next page button not found\n{e}")
        return False


def get_table_data(driver, address,  data):

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
            row_data = row.find_element(By.XPATH, "//*[@data-title='Address']")
            # if row_data in address:
            go_to_button = row.find_element(By.TAG_NAME, "button")
            go_to_button.click()
            name = driver.find_element(By.NAME, "firstName")
            last_name = driver.find_element(By.NAME, "lastName")
            phone = driver.find_element(By.NAME, "phone")
            email = driver.find_element(By.NAME, "email")
            installation_type = driver.find_element(
                By.NAME, "installationType")
            consent = driver.find_element(
                By.XPATH, "/html/body/div/div[2]/div/div/form/div[13]/div[3]/select")
            # // consent notes
            # Default Notes,  paper and letter delivery

            consent_options = consent.find_elements(By.TAG_NAME, "option")
            notes = driver.find_element(By.NAME, "note")
            property_ownership_type = driver.find_element(
                By.XPATH, "/html/body/div/div[2]/div/div/form/div[26]/div[3]/select")
            save_button = driver.find_element(
                By.XPATH, "/html/body/div/div[2]/div/div/div[3]/div[2]/button[5]")
            name.send_keys(data.name)
            last_name.send_keys(data.last_name)
            phone.send_keys(data.phone)
            email.send_keys(data.email)
            installation_type.send_keys(data.installation_type)
            notes.send_keys(data.notes)
            if data.consent == "No":
                consent_options.click(data.consent)
                refusal_reason = driver.find_element(
                    By.NAME, "refusalReason")
                refusal_reason.send_keys(data.refusal_reason)
            consent_options.click(data.consent)
            property_ownership_type.send_keys("Owned")
            save_button.click()
    except Exception as e:
        print(e)
        return False
    return True


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


def get_property_in_table(driver, data):
    address = str(data[0]['streetNumber']) + \
        ' ' + data[0]['streetName']
    address_to_update = address.upper()
    click_100_views_button(driver)
    print(f'Address to be updated: {address_to_update}')

    while True:  # Keep looping until address is found or no more pages
        try:
            sleep(2)
            rows = driver.find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                row_dict = {}
                cells = row.find_elements(By.TAG_NAME, 'td')
                for cell in cells:
                    key = cell.get_attribute('data-title-text')
                    value = cell.text
                    row_dict[key] = value

                if address_to_update in row_dict.get("Address", ""):
                    go_to_button = row.find_element(
                        By.XPATH, "td//button[contains(text(), 'Go To')]")
                    go_to_button.click()
                    return row_dict  # Returning the found row data, you can adjust this

            # If address not found on this page, click next and continue loop
            if not click_next_page_button(driver):
                print("Address not found")
                return None  # or any suitable value if you've reached the last page

        except Exception as e:
            print("Error:", e)
            return None


# # Wait for the form to load before sending data
# sleep(2)

# try:
#     # Fill in the form fields
#     driver.find_element(
#         By.XPATH, "/html/body/div/div[2]/div/div/form/div[3]/div[3]/input[1]").send_keys(data["name"])
#     driver.find_element(
#         By.XPATH, "/html/body/div/div[2]/div/div/form/div[3]/div[3]/input[2]").send_keys(data["lastName"])
#     driver.find_element(
#         By.XPATH, "/html/body/div/div[2]/div/div/form/div[5]/div[3]/input").send_keys(data["phone"])
#     driver.find_element(
#         By.XPATH, "/html/body/div/div[2]/div/div/form/div[6]/div[3]/input").send_keys(data["email"])

#     # Select Language
#     language_select = driver.find_element(By.NAME, "language")
#     language_options = language_select.find_elements(By.TAG_NAME, "option")
#     for option in language_options:
#         if option.text.strip() == "English":
#             option.click()
#             break

#     # Select Feed
#     feed_options = driver.find_elements(By.NAME, "feed")
#     for option in feed_options:
#         if option.get_attribute("value") == "Aerial":
#             option.click()
#             break

#     # Select Installation Type
#     installation_type_select = driver.find_element(
#         By.NAME, "installationType")
#     installation_type_options = installation_type_select.find_elements(
#         By.TAG_NAME, "option")
#     for option in installation_type_options:
#         if option.text.strip() == data["type"]:
#             option.click()
#             break

#     # Select Consent
#     consent_select = driver.find_element(By.NAME, "Consent")
#     consent_options = consent_select.find_elements(By.TAG_NAME, "option")
#     for option in consent_options:
#         if option.text.strip() == data["consent"]:
#             option.click()
#             break

#     # Submit the form
#     submit_button = driver.find_element(
#         By.XPATH, "//button[contains(text(), 'Submit')]")
#     submit_button.click()

#     # Wait for the form to submit
#     sleep(2)

#     # Get the success message or any relevant data after submitting the form
#     success_message = driver.find_element(
#         By.XPATH, "//div[contains(text(), 'Success!')]").text
#     table_data.append(success_message)

#     # Close the form
#     close_button = driver.find_element(
#         By.XPATH, "//button[contains(text(), 'Close')]")
#     close_button.click()
# except Exception as e:
#     print("Error:", e)
#     return None

# return table_data


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
print("\nLogin confirmed!\nInitializing fetching process...")
select_site(driver, site_name)
print(get_property_in_table(driver, data))


end_time = datetime.datetime.now()

script_duration = start_time - end_time


fetch_report.append({str(script_duration): script_duration.total_seconds()})


with open('fetch_report.json', 'w') as f:
    json.dump(fetch_report, f, indent=4)
    f.close()


"""

data example:
{  "id": 25706,  "streetNumber": 773,  "lastName": "Kim",  "name": "Yoonhe ",  "notes": " ",  "salesForceNotes": " ",  "phone": " ",  "email": "Ckim.Grey@gmail.com",  "type": "Moderate",  "streetId": 986,  "locationId": 97,  "lastUpdated": "2023-07-28T15:47:54.523Z",  "lastUpdatedBy": "Yuri Almeida",  "statusAttempt": "Consent Final",  "consent": "Yes"}
def get_property_in_table(driver, data):
    address_to_update = str(data['streetNumber']) + ' ' + data['streetName']
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
                if address_to_update in ["Address"]:
                    go_to_button = row.find_element(By.XPATH, "td//button[contains(text(), 'Go To')]")
                    go_to_button.click()
complete function to send data to form
def get_property_in_table(driver, data):
	address_to_update = str(data['streetNumber']) + ' ' + data['streetName']
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
				row_dict[key] = value
			if address_to_update in row_dict.get("Address", ""):
				go_to_button = row.find_element(By.XPATH, "td//button[contains(text(), 'Go To')]")
				go_to_button.click()

                    
		# driver.find_element(By.NAME, "firstName").send_keys(data["name"])
		driver.find_element(
			By.XPATH, "/html/body/div/div[2]/div/div/form/div[3]/div[3]/input[1]").send_keys(data["name"])
		driver.find_element(
			By.XPATH, "/html/body/div/div[2]/div/div/form/div[3]/div[3]/input[2]").send_keys(data["lastName"])
		# driver.find_element(By.NAME, "lastName").send_keys(data["lastName"])
		# driver.find_element(By.NAME, "phone").send_keys(data["phone"])
		driver.find_element(
			By.NAME, "/html/body/div/div[2]/div/div/form/div[5]/div[3]/input").send_keys(data["phone"])
		# driver.find_element(By.NAME, "email").send_keys(data["email"])
		driver.find_element(
			By.NAME, "/html/body/div/div[2]/div/div/form/div[6]/div[3]/input").send_keys(data["email"])		# driver.find_element(By.NAME, "firstName").send_keys(data["name"])
		driver.find_element(
			By.XPATH, "/html/body/div/div[2]/div/div/form/div[3]/div[3]/input[1]").send_keys(data["name"])
		driver.find_element(
			By.XPATH, "/html/body/div/div[2]/div/div/form/div[3]/div[3]/input[2]").send_keys(data["lastName"])
		# driver.find_element(By.NAME, "lastName").send_keys(data["lastName"])
		# driver.find_element(By.NAME, "phone").send_keys(data["phone"])
		driver.find_element(
			By.NAME, "/html/body/div/div[2]/div/div/form/div[5]/div[3]/input").send_keys(data["phone"])
		# driver.find_element(By.NAME, "email").send_keys(data["email"])
		driver.find_element(
			By.NAME, "/html/body/div/div[2]/div/div/form/div[6]/div[3]/input").send_keys(data["email"])
"""
