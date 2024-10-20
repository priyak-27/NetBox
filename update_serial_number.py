import requests
import pynetbox
import urllib3
import csv
from requests.auth import HTTPBasicAuth
import pandas as pd
import json

# ***************************************************************
# ============update serial number on NetBox====================

netbox_url = "enter your netbox URL"
netbox_api_key = "enter your netbox token"

response = pynetbox.api(url=f"https://{netbox_url}", token=netbox_api_key)
response.http_session.verify = False
urllib3.disable_warnings()

# Read Excel file
excel_file = 'update_serial_number.xlsx'
df = pd.read_excel(excel_file)

# Handle NaN values which replaces NaN values with empty strings
df.fillna('', inplace=True) 

# Open the error log file in write mode
with open('error_serial.txt', 'w') as error_file:
    # Ensure your Excel has 'device_name' and 'serial_number' columns
    for index, row in df.iterrows():
        device_name = row['device_name']
        serial_number = row['serial_number']

        # Fetch the device from NetBox
        try:
            device = response.dcim.devices.get(name=device_name)
            if device:
               # Update the serial number
               device.update({'serial': serial_number})
               print(f"Updated {device_name} with serial number {serial_number}")
            else:
               print(f"Device {device_name} not found in NetBox.")
               error_file.write(f"Device {device_name} not found in NetBox." + '\n')
        except Exception as e:
            print(f"Error updating device {device_name}: {e}")
            error_file.write(f"Error updating device {device_name}: {e}" + '\n')

print("Update complete.")
