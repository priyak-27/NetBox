import pynetbox
import urllib3
import time
import pandas as pd
import csv

# Define your NetBox URL and API key
netbox_url = "enter your netbox URL"
netbox_api_key = "enter your netbox token"

# Initialize the pynetbox API instance
response = pynetbox.api(url=f"https://{netbox_url}", token=netbox_api_key)
response.http_session.verify = False
urllib3.disable_warnings()


def add_device(device_name, device_type_id, role_id, site_id, serial_number, manufacturer_id, device_status):
    """Add a device with the provided details."""
    device_data = {
        "name": device_name,
        "device_type": device_type_id,
        "role": role_id,
        "site": site_id,
        "serial": serial_number,
        "manufacturer": manufacturer_id, 
        "status": device_status,   
    }

    try:
        result = response.dcim.devices.create(device_data)
        print(result)
    except pynetbox.RequestError as e:
        error_message = f"Error creating device {device_name}: {e}"
        print(error_message)
        with open('error_devices.txt', 'a') as error_file:
            error_file.write(f"{error_message}\n")

# Read the device details from the Excel file
excel_file = 'import_device_details.xlsx'
df = pd.read_excel(excel_file)

# Strip any leading or trailing whitespace from the column names
df.columns = df.columns.str.strip()

# Ensure all expected columns are present
expected_columns = ['device_name', 'device_type_id', 'role_id', 'site_id', 'serial_number', 'manufacturer_id', 'device_status']
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    print(f"Missing columns in the Excel file: {missing_columns}")
else:

    # Handle NaN values which replaces NaN values with empty strings
    df.fillna('', inplace=True)  
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        try:
            time.sleep(0.5)  # Optional delay to avoid hitting rate limits
            device_name = row['device_name']
            device_type_id = row['device_type_id']
            role_id = row['role_id']
            site_id = row['site_id']
            serial_number = row['serial_number']
            manufacturer_id = row['manufacturer_id']
            device_status = row['device_status']
            
            print(f"Adding device: {device_name} to site ID: {site_id}")
            add_device(device_name, device_type_id, role_id, site_id, serial_number, manufacturer_id, device_status)
        except KeyError as e:
            error_message = f"Missing column in row {index}: {e}"
            print(error_message)
            with open('error_devices.txt', 'a') as error_file:
                error_file.write(f"{error_message}\n")
        except Exception as e:
            error_message = f"Error processing row {index}: {e}"
            print(error_message)
            with open('error_devices.txt', 'a') as error_file:
                error_file.write(f"{error_message}\n")
