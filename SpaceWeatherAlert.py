import requests as r
import time as t
import datetime as dt
import slackclient as sc

# Sets up connection to the Slack Client
print("Space Weather Alert")
token = input("Spackbot Token: ")
print("DO NOT CLOSE - Austin")
slack_client = sc.SlackClient(token)

# Sets an initial date to check against
SW = dt.datetime(1970, 1, 1, 0, 0, 0)

# Checks for a new space weather event every 10 seconds
while True:
    data = r.get('http://services.swpc.noaa.gov/products/alerts.json').json() #Loads alert data from NOAA
    evt_t = data[0]['issue_datetime']
    evt_t = dt.datetime.strptime(evt_t, "%Y-%m-%d %H:%M:%S.%f")
    if evt_t > SW: # Checks latest event time against previous event time
        slack_client.api_call(
            "chat.postMessage",
            channel="spaceweather-alerts", # Slack channel
            text="New Space Weather Event! \n"
            + str(data[0]['product_id']) + "\n"
            + "Date-Time: " + str(evt_t) + "\n"
            + str(data[0]['message'])
        )
        SW = evt_t
    t.sleep(120)