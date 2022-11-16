from credential import API_KEY
import requests
from functions import non_callback_query,callback_query

TOKEN = API_KEY
message_received_total = 0
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
r = requests.get(url)
json = r.json()
message_received_total = len(json["result"])
while 1:
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    r = requests.get(url)
    json = r.json()
    if len(json["result"]) > message_received_total:
        message_received_total_before = message_received_total
        message_received_total = len(json["result"])
        for result in json["result"][message_received_total_before : message_received_total]:
            # Detect if it is a callback query from inline keyboard
            if "callback_query" in result:
                callback_query(result,TOKEN)
            # Else if it is not a callback query then it is a direct message
            else:
                non_callback_query(result,TOKEN)


















