## Python Web Scraping Script

This file contains a Python script that automates web scraping of data from a web application using Selenium WebDriver. The script interacts with the Salesforce web application to fetch data from different sites. It performs the following actions:

### Imports

The script imports the following required modules:

- datetime
- time
- messagebox from tkinter
- httpcore.TimeoutException
- selenium.webdriver
- selenium.webdriver.support.ui.Select
- selenium.webdriver.common.by.By
- selenium.webdriver.common.keys.Keys
- json
- pandas
- selenium.webdriver.chrome.service.Service
- selenium.webdriver.support.ui.WebDriverWait
- selenium.webdriver.support.expected_conditions
- collections.defaultdict

### Custom Function

The script defines a custom function `sleep(seconds)` for pausing execution for a specified number of seconds.

### Variables

The script stores a list called `fetch_report` that will be used to store information about the execution status of different functions during data fetching. It also sets up the credentials `username` and `password` to log in to the Salesforce web application.

### Constants

The script defines several constants related to XPath and iframes for locating elements in the web application.

### Reading Data

The script reads data from a JSON file called `LOCATIONS.json` into variables `location_code_for_each_city`.

### Confirmation Message

The script defines a function `confirmation()` to display a confirmation message for the user during login.

### Utility Functions

The script defines several utility functions for interacting with the web application:

- `select_site(driver, site_name)`: Selects a site from a dropdown menu.
- `click_100_views_button(driver)`: Clicks a button to change the number of views to 100.
- `click_next_page_button(driver)`: Clicks a button to go to the next page of data.
- `get_table_data(driver)`: Fetches table data from the current page.
- `clean_data(data)`: Cleans the fetched data into a structured format.
- `fetch_site_data(driver, site_name)`: Fetches data from a specific site.

### Configuring WebDriver

The script configures the WebDriver for Chrome and opens the Salesforce login page. It then logs in to the Salesforce web application using the provided credentials.

### Main Data Fetching Process

The script executes the main data fetching process:

- Displays a confirmation message to wait for login completion.
- Iterates through the location in `location_code_for_each_city`, defined in `city_to_fetch`.
- Selects a site, fetches data, cleans it, and saves it as a JSON file for each site.
- Calculates the script's execution time.
- Appends the script execution duration to the `fetch_report` list.
- Saves the `fetch_report` list as a JSON file called `fetch_report.json`.

This script is designed to fetch data from the Salesforce web application for various sites and store the cleaned data in separate JSON files for each site. Additionally, it records the execution status and duration in the `fetch_report.json` file.
