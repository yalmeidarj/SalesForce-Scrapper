from fetcher_bot import FetcherBot
import os

print(os.getcwd())

brain = FetcherBot()
bell_salesForce_url = "https://bellconsent.my.salesforce.com/?ec=302&startURL=%2Fvisualforce%2Fsession%3Furl%3Dhttps%253A%252F%252Fbellconsent.lightning.force.com%252Flightning%252Fn%252FBell"

site_to_be_updated = "TNHLON40_3104A"
# site_data = [{}]

# Read environment variables to get credentials
# username = os.getenv("USERNAME")
# password = os.getenv("PASSWORD")

# If environment variables are not set, use hardcoded credentials
user = "yalmeida.rj@gmail.com"
keyword = "rYeEsydWN!8808168eXkA9gV47A"

csv_file_path = "./ToFeedSalesForce/generatedBy_small.csv"

site_data = brain.process_csv_to_dict(file_path=csv_file_path)


def main():
    """
    Main function to run the bot

    - return: None
    """
    brain.go_to_url(bell_salesForce_url)
    brain.login(username=user, password=keyword)
    login_confirmed = brain.get_login_confirmation()
    if not login_confirmed:
        print("Error: Login confirmation failed")
        pass
    else:
        brain.select_site(site_to_be_updated)
        # loop through site_data and update each site in salesforce
        for data in site_data:
            # address_match = brain.find_matching_address_from_table(data)
            if not brain.find_matching_address_from_table(data):
                pass
            else:
                brain.switch_to_forms_iframe()
                # TODO: check if site is already updated
                check = brain.update_site_form_1(data)
                if not check:
                    print('Error: Site not updated, unable to submit form 1')
                    break
                else:
                    brain.switch_to_second_form_iframe()
                    brain.draw_signature()


main()
