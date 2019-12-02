import requests
from requests.exceptions import HTTPError


def get_rooms(start, end, timeout):
	uri = f'http://213.233.176.40/available_rooms?start={start}&end={end}'

	try:
		response = requests.get(uri, timeout = timeout)
		response.raise_for_status()

	except HTTPError as http_err:
		return f'HTTP error occurred: {http_err}'  # Python 3.6
	except Exception as err:
		return f'Other error occurred: {err}'  # Python 3.6
	else:
		return response.content


res = get_rooms("2017-09-13T19:00:00", "2020-09-13T20:00:00", 5)
print(res)


def reserve_room(room_number, username, start, end):
	uri = f'http://213.233.176.40/rooms/{room_number}/reserve'
	body = {
        "username": username,
        "start": start,
        "end": end
    }	

	try:
		response = requests.post(uri, body)
		response.raise_for_status()

	except HTTPError as http_err:
		return f'HTTP error occurred: {http_err}' 
	except Exception as err:
		return f'Other error occurred: {err}'  
	else:
		return response.content

res = reserve_room(801, "rkhosravi", "2019-09-13T19:00:00", "2019-09-13T20:00:00")
print(res)