## NetBox Automation Scripts

This repository contains various Python scripts that automate tasks related to NetBox, a popular open-source IPAM and DCIM tool. The automation is designed to enhance efficiency in networking environments by utilizing the NetBox API for operations such as data synchronization, device management, and reporting. These scripts facilitate seamless interaction with NetBox to streamline processes, reduce manual intervention, and automate repetitive tasks.

## required libraries
To run these scripts, the following Python libraries are required:

	•	requests
	•	pynetbox
	•	urllib3
	•	csv
	•	pandas
	•	json
	•	HTTPBasicAuth

## Script Details

### add_new_site.py
This script automates adding new sites to NetBox by reading site details from an Excel file with site details (name, location, status, region, physical address). It prevents duplicate entries, logs errors if a site cannot be created, and provides status updates for successful additions.

### coverage_end_date_in6month.py
This script, designed as a custom NetBox report, identifies devices whose coverage will end within the next six months. It retrieves and displays the device name, site name, serial number, and coverage end date if the end date falls within the next six months. The script calculates the six-month period from the current date and logs relevant device information for easy tracking.

### device_coverage_report.py
This script generates a report in NetBox displaying devices along with their name and coverage end date. It retrieves all devices, checks if each device has a coverage end date set, and logs the device name and coverage end date if available, making it easy to track coverage statuses.

### fetch_serial_no.py
This script retrieves and exports details of all devices in NetBox to a CSV file. It fetches the device name, serial number, and site name for each Cisco device and writes this information to a file called serialnumber.csv, enabling easy tracking and documentation of device information.

### get_site_details.py
This script exports site details from NetBox into an Excel file. It retrieves each site’s name, region, ID, and physical address, organizes this information in a DataFrame, and saves it to exported_sites_details.xlsx for easy reference and documentation.

### import_contacts.py
This script imports contact details from an Excel file into NetBox, handling name, title, email, phone, and address fields. For each row in the Excel file, it attempts to create a new contact or update an existing one if a contact with the same name already exists. Errors and skipped entries are logged in error_contact.txt for easy tracking.

### import_device_by_ids.py
This script imports device details from an Excel file into NetBox, handling fields like device name, device type ID, role ID, site ID, serial number, manufacturer ID, and device status. Each row is processed to add the device to NetBox, with a brief delay to avoid rate limits. Errors, missing columns, and any issues with adding devices are logged in error_devices.txt for easy troubleshooting.

### ser_to_info.py
This script performs a multi-step process for managing device data between NetBox and Cisco’s API, including exporting device serials, fetching Cisco coverage information, and updating NetBox with the details. Here’s a structured overview of the tasks it performs:

	1.	Export Serial Numbers from NetBox:
	•	Connects to the specified NetBox URL using an API key and fetches all active devices.
	•	Writes each device’s name and serial number to devices.csv.

	2.	Cisco Access Token Retrieval:
	•	Requests an access token using provided Cisco API credentials.
	•	If successful, it saves the access token in cisco_access_token.txt for subsequent API calls.

	3.	Fetch Cisco Coverage Information:
	•	Reads serial numbers from devices.csv.
	•	For each serial number, retrieves coverage status and summary details from Cisco’s API.
	•	Appends the Cisco information (such as warranty type, end date, and coverage status) to the devices.csv file.

	4.	Update NetBox Custom Fields:
	•	Reads the enriched data from devices.csv.
	•	For each device, matches its name with NetBox entries and updates custom fields like is_covered, coverage_end_date, warranty_end_date, etc., with the Cisco API data.


### serial_no_to_info_for_active_devices.py
This script follows a systematic process to fetch active device data from NetBox, request Cisco API data on device coverage, and update NetBox custom fields with the obtained information. Here’s a detailed breakdown of its functionality:

	1.	CSV File Preparation:
	•	Checks if an active_devices.csv file already exists in the working directory. If found, deletes it, ensuring that the file always contains fresh data.

	2.	Retrieve Device Serial Numbers from NetBox:
	•	Connects to NetBox using the provided URL and API token.
	•	Fetches all active devices and writes their names and serial numbers to active_devices.csv.

	3.	Cisco Access Token Retrieval:
	•	Obtains an access token from the Cisco API using client credentials. The token is required for subsequent Cisco API requests.

	4.	Fetch Cisco Coverage Information:
	•	Reads device serial numbers from active_devices.csv.
	•	Skips entries where serial numbers are empty or missing.
	•	Calls the Cisco API to retrieve coverage summary information, including warranty type, end date, and coverage status.
	•	Appends the fetched data as new columns in the same active_devices.csv file.

	5.	Update NetBox Custom Fields:
	•	Reads the enriched data from active_devices.csv.
	•	Searches for each device by name in NetBox and updates custom fields like is_covered, coverage_end_date, and warranty_end_date with the Cisco data.

### serial_no_to_info_meraki.py
This script is the same as above script but it is for Meraki devices instead of active devices. 

### sno_to_info_cisco1.py and sno_to_info_cisco2.py
this whole script is divided into two parts because there is a limitation on Cisco side that you can make 10,000 api calls to cisco in a day. The first part is just to get the list of all Cisco devices with their serial number. The second part is to fetch coverage information from Cisco. If in case you have 10,000+ devices, you can copy the details of the rest of the devices in another file and run the second script for the 
first 10,000 devices. 

**sno_to_info_cisco1.py**- The script is designed to interact with the NetBox API to manage and store information about Cisco devices. It starts by checking for an existing CSV file named cisco_devices.csv in the current directory; if found, it deletes the file to prevent any old data from interfering with the new data collection. The script then establishes a connection to the NetBox API using the provided URL and API token, while suppressing SSL verification warnings for convenience. Afterward, it retrieves a list of manufacturers from the NetBox database and searches for the manufacturer named “Cisco.” If the Cisco manufacturer is not found, the script exits with a message indicating the absence of the manufacturer. Assuming Cisco devices are present, it filters the devices by the Cisco manufacturer ID and prepares to write the device details to the new CSV file. It opens the file in write mode, creates a CSV writer object, and writes the header row. Finally, the script iterates through the Cisco devices, recording each device’s name and serial number into the CSV file, confirming that the details have been successfully added.

**sno_to_info_cisco2.py**- This Python script facilitates the retrieval and storage of coverage information for Cisco devices using the Cisco API and updates corresponding custom fields in NetBox. It begins by defining the necessary client ID and secret for Cisco’s OAuth2 authentication process and constructs a POST request to acquire an access token. If the token request is successful, the script retrieves and stores the token for subsequent API calls. Following authentication, the script defines a function to request coverage summary information based on device serial numbers. It reads a CSV file named cisco_devices.csv, which contains device serial numbers, ensuring all serial numbers are treated as strings. As it iterates through these serial numbers, the script retrieves coverage information, storing various details such as coverage status, end dates, and warranty information into separate lists. After processing all serial numbers, these details are added as new columns in the DataFrame, which is then saved back to the original CSV file.

Lastly, the script connects to the NetBox API and reads the updated CSV file to fetch each device by name. It updates the custom fields of each device with the retrieved coverage information, ensuring that all relevant data is stored in NetBox. If a device is not found, a message is printed. The script concludes by confirming that all custom fields have been updated, providing a streamlined approach to managing device information across both Cisco and NetBox platforms.

### update_serial_number.py
This Python script updates device serial numbers in NetBox using data from an Excel file (update_serial_number.xlsx). It connects to the NetBox API with a specified URL and API key, reads the device names and serial numbers from the Excel file, and replaces any missing values with empty strings.
For each device, the script attempts to fetch it from NetBox and update its serial number. If a device is not found or an error occurs, the script logs the issue in an error file (error_serial.txt). It concludes by printing a message indicating the update process is complete.
