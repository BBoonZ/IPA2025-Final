import os
import requests

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

url = "https://webexapis.com/v1/rooms"
r = requests.get(url, headers=headers)

if r.status_code == 200:
    rooms = r.json()["items"]
    for room in rooms:
        print(f"Room name: {room['title']}  |  Room ID: {room['id']}")
else:
    print("Error:", r.status_code, r.text)
