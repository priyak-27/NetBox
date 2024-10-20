import pandas as pd
import pynetbox
import urllib3
from requests.auth import HTTPBasicAuth

# Define your NetBox URL and API key
netbox_url = "enter your netbox URL"
netbox_api_key = "enter your netbox token"

response = pynetbox.api(url=f"https://{netbox_url}", token=netbox_api_key)
response.http_session.verify = False
urllib3.disable_warnings()

# Function to export site details from NetBox
def export_sites_from_netbox():
    # Retrieve all sites from NetBox
    sites = response.dcim.sites.all()
    
    # List to store site details
    site_details = []

    # Extract details for each site
    for site in sites:
        site_details.append({
            'name': site.name,
            'region': site.region.name if site.region else '',
            'id': site.id,
            'physical address': site.physical_address if hasattr(site, 'physical_address') else ''
        })

    # Create a DataFrame from the site details
    df = pd.DataFrame(site_details)

    # Write the DataFrame to an Excel file
    df.to_excel('exported_sites_details.xlsx', index=False)

# Export sites from NetBox
export_sites_from_netbox()
