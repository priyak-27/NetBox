from extras.scripts import Script
from dcim.models import Device
from datetime import datetime, timedelta
 
class DeviceCoverageReportSixMonth(Script):
    #Report on device names and coverage end dates within the next 6 months.
 
    description = "Shows device name, site name, serial number and coverage end date if the coverage ends within 6 months."
 
    def test_device_coverage_six_months(self):
        # Calculate the date 6 months from now
        today = datetime.today()
        # Approximate 6 months as 180 days
        six_months_from_now = today + timedelta(days=6*30) 
 
        # Get all devices
        for device in Device.objects.all():
            device_name = device.name
            serial_number = device.serial if device.serial else "No Serial Number"
            site_name = device.site.name if device.site else "No Site"
            coverage_end_date = device.custom_field_data.get('coverage_end_date')
             
            # Check if coverage_end_date is set and within the next 6 months
            if coverage_end_date:
                # Convert coverage_end_date to a datetime object
                coverage_end_date = datetime.strptime(coverage_end_date, '%Y-%m-%d')
                 
                if today <= coverage_end_date <= six_months_from_now:
                    # Log each device's info in the report
                    self.log_success(
                        obj=device,
                        message=f"Name: {device_name}\tSerial No: {serial_number}\tSite: {site_name}\tCoverage end date:{coverage_end_date.strftime('%Y-%m-%d')}"
                    )