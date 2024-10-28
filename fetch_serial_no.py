import requests
import pynetbox
import urllib3
import csv
from requests.auth import HTTPBasicAuth
import pandas as pd
import json

# ***************************************************************
# ============fetch serial number from NetBox====================

netbox_url = "enter your netbox URL"
netbox_api_key = "enter your netbox token"

response = pynetbox.api(url=f"https://{netbox_url}", token=netbox_api_key)
response.http_session.verify = False
urllib3.disable_warnings()


# Fetch all devices
devices = response.dcim.devices.all()

# Open a CSV file in write mode
with open('serialnumber.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)

    # Write the header row
    csvwriter.writerow(['Device Name', 'Device Serial Number', 'site'])

    # Iterate over the devices and write their details to the CSV file
    for device in devices:
        csvwriter.writerow([device.name, device.serial, device.site.name])
print("Serial number for all devices has been added to serialnumber.csv")
