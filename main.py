import datetime
import os
import threading
import time


def start_api():
    os.system("uvicorn api:api --reload")


x = threading.Thread(target=start_api)
print("Started API")


def run_scraper():
    print("Running scraper at " + str(datetime.datetime.now()))
    os.system("scraper.py")


# Run the scheduled tasks indefinitely
while True:
    run_scraper()
    time.sleep(600)
