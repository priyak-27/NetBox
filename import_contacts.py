import pandas as pd
import pynetbox
import logging
import urllib3


# Configure logging
logging.basicConfig(filename='error_contact.txt', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# Load your Excel file
file_path = 'import_contact.xlsx'
df = pd.read_excel(file_path)

# Connect to NetBox
netbox_url = "enter your netbox URL"
netbox_api_key = "enter your netbox token"

response = pynetbox.api(url=f"https://{netbox_url}", token=netbox_api_key)
response.http_session.verify = False
urllib3.disable_warnings()

# Iterate through the DataFrame and create/update contacts in NetBox
for index, row in df.iterrows():
    try:
        # Skip the row if the 'name' field is empty
        if pd.isna(row['name']):
            logging.error(f"Row {index+1} skipped: 'name' is required.")
            continue
        
        # Handle empty cells by filling NaN with empty strings
        contact_data = {
            'name': row['name'] if pd.notna(row['name']) else '',
            'title': row['title'] if pd.notna(row['title']) else '',
            'email': row['email'] if pd.notna(row['email']) else '',
            'phone': row['phone'] if pd.notna(row['phone']) else '',
            'address': row['address'] if pd.notna(row['address']) else ''
        }

        # Attempt to create a new contact
        contact = response.tenancy.contacts.create(contact_data)
        
        # If contact creation fails, try updating the existing contact
        if contact is None:
            existing_contact = response.tenancy.contacts.get(name=contact_data['name'])
            if existing_contact:
                existing_contact.update(contact_data)
            else:
                logging.error(f"Row {index+1} error: Unable to create or update contact with name {contact_data['name']}")
    
    except Exception as e:
        logging.error(f"Row {index+1} error: {str(e)}")

print("Contacts import complete.")
print("check error_contact.txt to see if there was any error.")
