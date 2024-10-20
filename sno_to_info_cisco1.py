import requests
import pynetbox
import urllib3
import csv
from requests.auth import HTTPBasicAuth
import pandas as pd
import json
import os

# Check if 'cisco_devices.csv' exists in the current directory and delete it if it does
csv_file_path = 'cisco_devices.csv'
if os.path.exists(csv_file_path):
    os.remove(csv_file_path)
    print(f"Deleted existing {csv_file_path} file.")
else:
    print(f"No existing {csv_file_path} file found.")

# ***************************************************************
# ============fetch serial number from NetBox====================

netbox_url = "enter your netbox URL"
netbox_api_key = "enter your netbox token"

response = pynetbox.api(url=f"https://{netbox_url}", token=netbox_api_key)
response.http_session.verify = False
urllib3.disable_warnings()

# Fetch all manufacturers
manufacturers = response.dcim.manufacturers.all()

# Find the manufacturer with the name "Cisco"
cisco_manufacturer = next((m for m in manufacturers if m.name.lower() == 'cisco'), None)

if not cisco_manufacturer:
    print("Cisco manufacturer not found in NetBox.")
    exit()

# Fetch all devices with the manufacturer "Cisco"
devices = response.dcim.devices.filter(manufacturer_id=cisco_manufacturer.id)

# Open a CSV file in write mode
with open(csv_file_path, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)

    # Write the header row
    csvwriter.writerow(['Device Name', 'Device Serial Number'])

    # Iterate over the devices and write their details to the CSV file
    for device in devices:
        csvwriter.writerow([device.name, device.serial])
print("Serial number for all devices has been added to cisco_devices.csv")
