# Python: Garmin Connect

Python 3 API wrapper for Garmin Connect to get your statistics.

## About

This package allows you to request your device, activity and health data from your Garmin Connect account.
See https://connect.garmin.com/


## Installation

```bash
pip install garminconnect
```

## Usage

```python
#!/usr/bin/env python3

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from datetime import date


"""
Enable debug logging
"""
import logging
logging.basicConfig(level=logging.DEBUG)

today = date.today()


"""
Initialize Garmin client with credentials
Only needed when your program is initialized
"""
print("Garmin(email, password)")
print("----------------------------------------------------------------------------------------")
try:
    client = Garmin(YOUR_EMAIL, YOUR_PASSWORD)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client init: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client init")
    quit()


"""
Login to Garmin Connect portal
Only needed at start of your program
The library will try to relogin when session expires
"""
print("client.login()")
print("----------------------------------------------------------------------------------------")
try:
    client.login()
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client login: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client login")
    quit()


"""
Get full name from profile
"""
print("client.get_full_name()")
print("----------------------------------------------------------------------------------------")
try:
    print(client.get_full_name())
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get full name: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get full name")
    quit()


"""
Get unit system from profile
"""
print("client.get_unit_system()")
print("----------------------------------------------------------------------------------------")
try:
    print(client.get_unit_system())
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get unit system: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get unit system")
    quit()


"""
Get activity data
"""
print("client.get_stats(%s)", today.isoformat())
print("----------------------------------------------------------------------------------------")
try:
    print(client.get_stats(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get stats: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get stats")
    quit()


"""
Get steps data
"""
print("client.get_steps_data\(%s\)", today.isoformat())
print("----------------------------------------------------------------------------------------")
try:
    print(client.get_steps_data(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get steps data: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get steps data")
    quit()


"""
Get heart rate data
"""
print("client.get_heart_rates(%s)", today.isoformat())
print("----------------------------------------------------------------------------------------")
try:
    print(client.get_heart_rates(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get heart rates: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get heart rates")
    quit()


"""
Get body composition data
"""
print("client.get_body_composition(%s)", today.isoformat())
print("----------------------------------------------------------------------------------------")
try:
    print(client.get_body_composition(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get body composition: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get body composition")
    quit()


"""
Get stats and body composition data
"""
print("client.get_stats_and_body_composition(%s)", today.isoformat())
print("----------------------------------------------------------------------------------------")
try:
    print(client.get_stats_and_body(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get stats and body composition: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get stats and body composition")
    quit()


"""
Get activities data
"""
print("client.get_activities(0,1)")
print("----------------------------------------------------------------------------------------")
try:
    activities = client.get_activities(0,1) # 0=start, 1=limit
    print(activities)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get activities: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get activities")
    quit()


"""
Download an Activity
"""
try:
    for activity in activities:
        activity_id = activity["activityId"]
        print("client.download_activities(%s)", activity_id)
        print("----------------------------------------------------------------------------------------")

        gpx_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.GPX)
        output_file = f"./{str(activity_id)}.gpx"
        with open(output_file, "wb") as fb:
            fb.write(gpx_data)

        tcx_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.TCX)
        output_file = f"./{str(activity_id)}.tcx"
        with open(output_file, "wb") as fb:
            fb.write(tcx_data)

        zip_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
        output_file = f"./{str(activity_id)}.zip"
        with open(output_file, "wb") as fb:
            fb.write(zip_data)

        csv_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.CSV)
        output_file = f"./{str(activity_id)}.csv"
        with open(output_file, "wb") as fb:
          fb.write(csv_data)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get activity data: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get activity data")
    quit()


"""
Get sleep data
"""
print("client.get_sleep_data(%s)", today.isoformat())
print("----------------------------------------------------------------------------------------")
try:
    print(client.get_sleep_data(today.isoformat()))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get sleep data: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get sleep data")
    quit()


"""
Get devices
"""
print("client.get_devices()")
print("----------------------------------------------------------------------------------------")
try:
    devices = client.get_devices()
    print(devices)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get devices: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get devices")
    quit()


"""
Get device settings
"""
try:
    for device in devices:
        device_id = device["deviceId"]
        print("client.get_device_settings(%s)", device_id)
        print("----------------------------------------------------------------------------------------")

        print(client.get_device_settings(device_id))
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get device settings: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get device settings")
    quit()
```
