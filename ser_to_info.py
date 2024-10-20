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

devices = response.dcim.devices.all()

# Open a CSV file in write mode
with open('devices.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)

    # Write the header row
    csvwriter.writerow(['Device Name', 'Device Serial Number'])

    # Iterate over the devices and write their details to the CSV file
    for device in devices:
        if device.status.value == 'active' and device.status.label == 'Active':
            csvwriter.writerow([device.name, device.serial])
print("Serial number for all devices has been added to devices.csv")


# ************************************************************
# =================get your Cisco access token================

# enter your client key/id and secret
client_id = 'enter your cisoc id'
client_secret = 'enter your cisco token'

# Cisco API token endpoint
token_url = 'https://id.cisco.com/oauth2/default/v1/token?'

# Parameters for the token request
payload = {
    'grant_type': 'client_credentials'
}

# Make the POST request to get the token
response = requests.post(token_url, auth=HTTPBasicAuth(client_id, client_secret), data=payload)

# Check if the token request was successful
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info['access_token']

    # Save the token to a text file
    with open('cisco_access_token.txt', 'w') as token_file:
        token_file.write(access_token)
    print("Access token saved to cisco_access_token.txt")
else:
    print(f"Failed to obtain token: {response.status_code}")


# *************************************************************************
# ===========to get serial info and add it in same csv file=================


COVERAGE_STATUS_URL = 'https://apix.cisco.com/sn2info/v2/coverage/status/serial_numbers/'
COVERAGE_SUMMARY_URL = 'https://apix.cisco.com/sn2info/v2/coverage/summary/serial_numbers/'

# Function to get coverage status
def get_coverage_status(serial_number, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    response = requests.get(COVERAGE_STATUS_URL + serial_number, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"failed to get coverage status": response.status_code, "message": response.text}
    
# Function to get coverage summary
def get_coverage_summary(serial_number, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    response = requests.get(COVERAGE_SUMMARY_URL + serial_number, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"failed to get coverage summary": response.status_code, "message": response.text}
    
# Read CSV file containing serial numbers
csv_file_path = 'devices.csv'  # Path to your CSV file
df = pd.read_csv(csv_file_path)

# Ensure all serial numbers are strings
df['Device Serial Number'] = df['Device Serial Number'].astype(str)

# Assuming the CSV has a column named 'Device Serial Number'
serial_numbers = df['Device Serial Number'].tolist()

# Initialize lists to store the extracted information
is_covered_list = []
coverage_end_date_list = []
service_contract_number_list = []
contract_site_country_list = []
contract_site_city_list = []
warranty_type_list = []
warranty_end_date_list = []

# Loop through serial numbers and fetch their info and store in the results
for sn in serial_numbers:
    status_info = get_coverage_status(sn, access_token)
    if 'serial_numbers' in status_info and len(status_info['serial_numbers']) > 0:
        status_info = status_info['serial_numbers'][0]
        is_covered_list.append(status_info.get('is_covered', ''))
        coverage_end_date_list.append(status_info.get('coverage_end_date', ''))
    else:
        is_covered_list.append('')
        coverage_end_date_list.append('')

    summary_info = get_coverage_summary(sn, access_token)
    if 'serial_numbers' in summary_info and len(summary_info['serial_numbers'])>0:
        summary_info = summary_info['serial_numbers'][0]
        service_contract_number_list.append(summary_info.get('service_contract_number', ''))
        contract_site_country_list.append(summary_info.get('contract_site_country', ''))
        contract_site_city_list.append(summary_info.get('contract_site_city', ''))
        warranty_type_list.append(summary_info.get('warranty_type', ''))
        warranty_end_date_list.append(summary_info.get('warranty_end_date', ''))
    else:
        service_contract_number_list.append('')
        contract_site_country_list.append('')
        contract_site_city_list.append('')
        warranty_type_list.append('')
        warranty_end_date_list.append('')

# Add the extracted info to the DataFrame as new columns
df['is_covered'] = is_covered_list
df['coverage_end_date'] = coverage_end_date_list
df['service_contract_number'] = service_contract_number_list
df['contract_site_country'] = contract_site_country_list
df['contract_site_city'] = contract_site_city_list
df['warranty_type'] = warranty_type_list
df['warranty_end_date'] = warranty_end_date_list


# Save the updated DataFrame back to the CSV file
df.to_csv(csv_file_path, index=False)

print(f"Serial number info has been saved to {csv_file_path}")


# *************************************************************************
# ===========add information to the custom field in NetBox=================  


response = pynetbox.api(url=f"https://{netbox_url}", token=netbox_api_key)
response.http_session.verify = False
urllib3.disable_warnings()

# Read data from CSV file
with open('devices.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        device_name = row['Device Name'].strip()
        is_covered = row['is_covered'].strip()
        coverage_end_date = row['coverage_end_date'].strip()
        service_contract_number = row['service_contract_number'].strip()
        contract_site_country = row['contract_site_country'].strip()
        contract_site_city = row['contract_site_city'].strip()
        warranty_type = row['warranty_type'].strip()
        warranty_end_date = row['warranty_end_date'].strip()

        # Fetch device by name
        devices = response.dcim.devices.filter(name=device_name)

        if devices:
            # Iterate through all devices with the same name (if any)
            for device in devices:
                # Update custom fields
                device.custom_fields = {
                    'is_covered': is_covered,
                    'coverage_end_date': coverage_end_date,
                    'service_contract_number': service_contract_number,
                    'contract_site_country': contract_site_country,
                    'contract_site_city': contract_site_city,
                    'warranty_type': warranty_type,
                    'warranty_end_date': warranty_end_date
                }

                device.save()
                print(f"Custom fields updated for device: {device_name}")
        else:
            print(f"Device not found in NetBox: {device_name}")

print("Custom fields updated for all devices.")