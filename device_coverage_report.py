from extras.scripts import Script 
from dcim.models import Device

class DeviceCoverageReport(Script):
    #Report on device names and coverage end dates.

    description = "Shows devices with their name and coverage end date."

    def test_device_coverage(self):
        # Get all devices
        for device in Device.objects.all():
            device_name = device.name
            coverage_end_date = device.custom_field_data.get('coverage_end_date')
            
            # check if coverage end date is set
            if coverage_end_date:
                 # Log each device's info in the report
                 self.log_success(
                        obj=device, 
                        message=f"Name: {device_name}\tCoverage end date:{coverage_end_date}"
                    )

