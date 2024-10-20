import requests
import pynetbox
import urllib3
import csv
from requests.auth import HTTPBasicAuth
import pandas as pd
import json

# Define your NetBox URL and API key
netbox_url = "enter your netbox URL"
netbox_api_key = "enter your netbox token"

response = pynetbox.api(url=f"https://{netbox_url}", token=netbox_api_key)
response.http_session.verify = False
urllib3.disable_warnings()

# Function to read the Excel file and create new sites in NetBox
def add_sites_to_netbox(excel_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    
    # Handle NaN values, replacing them with empty strings
    df.fillna('', inplace=True)
    
    # Open the error log file in write mode
    with open('error_site.txt', 'w') as error_file:
        # Iterate over the rows of the DataFrame to add new sites
        for index, row in df.iterrows():
            # Format the site name
            site_name = f"{row['site name']}-{row['site location']}"
            
            try:
                # Check if the site already exists to avoid duplication
                existing_site = response.dcim.sites.get(name=site_name)
                if not existing_site:
                    # Create the new site in NetBox
                    response.dcim.sites.create(
                        name=site_name,
                        slug=site_name.lower().replace(' ', '-'),
                        status=row['site status'],
                        region=row['region'],
                        physical_address=row['physical address']
                    )
                    print(f"Site '{site_name}' created successfully.")
                else:
                    existing_site_message = f"Site '{site_name}' already exists."
                    print(existing_site_message)
                    error_file.write(existing_site_message + '\n')
            except Exception as e:
                # Log the error in the error log file
                error_message = f"Error adding site '{site_name}' (Location: {row['site location']}): {e}\n"
                error_file.write(error_message)
                print(error_message)

# Path to the Excel file which contains all site details to be added
excel_file = 'new_sites_details.xlsx'

# Add sites to NetBox
add_sites_to_netbox(excel_file)
