import requests
import json

class Notifier:
    def __init__(self, notification_url):
        self.notification_url = notification_url
    
    def send(self, past_trend, present_trend, mean_trend):
        notification_data = {"value1": past_trend.tolist(), "value2": present_trend.tolist(), "value3": mean_trend.tolist()}
        requests.post(self.notification_url, data=json.dumps(notification_data), headers={'content-type': 'application/json'})
