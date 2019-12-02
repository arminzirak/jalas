import json

import requests
from requests.exceptions import HTTPError


def get_rooms(start, end, timeout=3):
    uri = f'http://213.233.176.40/available_rooms?start={start}&end={end}'

    try:
        response = requests.get(uri, timeout=timeout)
        response.raise_for_status()

    except HTTPError as http_err:
        return f'HTTP error occurred: {http_err}'  # Python 3.6
    except Exception as err:
        return f'Other error occurred: {err}'  # Python 3.6
    else:
        rooms = json.loads(response.content.decode('utf-8').replace("'", '"'))['availableRooms']
        return rooms


# res = get_rooms("2017-09-13T19:00:00", "2020-09-13T20:00:00", 5)
# print(res)


# TODO: remove these examples


def reserve_room(room_number, username, start, end):
    import requests

    url = f'http://213.233.176.40/rooms/{room_number}/reserve'

    payload = "{\n        \"username\": \"" + username + "\",\n        \"start\": \"" + start + "\",\n        \"end\": \"" + end + "\"\n\t\n}"
    
    # payload = {
    #     "username": username,
    #     "start": start,
    #     "end": end,
    # }
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "eda3ddf2-adee-4304-9b70-5989ba41ad2a"
    }
    try:
        response = requests.request("POST", url, data=payload, headers=headers)

    except HTTPError as http_err:
        return f'HTTP error occurred: {http_err}'
    except Exception as err:
        return f'Other error occurred: {err}'
    else:
        return response.text, response.status_code



res = reserve_room("803", "rkhosravi", "2019-09-13T19:00:00", "2019-09-13T20:00:00")
print(res)
