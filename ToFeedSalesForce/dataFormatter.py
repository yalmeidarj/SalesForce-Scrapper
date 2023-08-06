"""
This script formats the data from the a csv file (containing the site information) to a JSON file
"""

import pandas as pd
import re


def split_address(address):
    """Splits an address into street name and street number."""
    if pd.isna(address) or address == "":
        return "", ""
    # Adjusted regex to better match street number and name
    match = re.match(r'^(.*?)(\d+)?$', address.strip())
    if match:
        return match.group(2).strip() if match.group(2) else "", match.group(1).strip() if match.group(1) else ""
    return "", address


def split_phone_email(cell):
    """Splits a cell containing phone and email into separate phone and email."""
    if pd.isna(cell) or cell == "":
        return "", ""
    # Simple regex to identify emails
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', cell)
    email = email_match.group(0) if email_match else ""
    phone = cell.replace(email, "").strip()
    return phone, email


# List of columns to exclude
exclude_columns = ['Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10']


# Load the data
gmlyon = pd.read_csv("./ToFeedSalesForce/GMLYON20_3011A.csv", skiprows=1)

# Drop unnecessary columns
gmlyon = gmlyon.drop(columns=exclude_columns)

# Apply the split_address function
gmlyon["streetNumber"], gmlyon["street"] = zip(
    *gmlyon["Unnamed: 1"].apply(split_address))

# Apply the split_phone_email function
gmlyon["phone"], gmlyon["email"] = zip(
    *gmlyon["Phone - Email"].apply(split_phone_email))

# Rename the columns
gmlyon = gmlyon.rename(columns={
    "LAST NAME": "lastName",
    "NAME": "name",
    "Notes": "salesForceNotes",
    "Type": "type"
})

# Keep only the required columns
gmlyon = gmlyon[['streetNumber', 'lastName', 'name',
                 'salesForceNotes', 'type', 'street', 'phone', 'email']]


# Create a csv file
gmlyon.to_csv("output.csv", index=False)

# # Convert DataFrame to JSON
# gmlyon_json = gmlyon.to_json(orient="records")


# # Save the JSON to a file if needed
# with open("output.json", "w") as f:
#     f.write(gmlyon_json)
