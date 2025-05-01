from pymongo import MongoClient
from data_cleaning import mmsis
from datetime import datetime
import matplotlib.pyplot as plt

mmsi_lst = mmsis("clean_data")

def convert_time(date_string: str):
    date_time = datetime.strptime(date_string, '%d/%m/%Y %H:%M:%S')
    return date_time

def calculate_delta_t(mmsi):
    with MongoClient("mongodb://localhost:27020") as client:
        db = client["vesselsDB"]
        collection = db["clean_data"]

        obj = collection.find({"MMSI": mmsi})
        time = []
        for row in obj:
            time.append(convert_time(row["# Timestamp"]))
        time.sort()
        delta_t = []
        for i in range(0, len(time) - 1):
            delta_t.append((time[i + 1] - time[i]).total_seconds() * 1000)
        
        return delta_t


for mmsi in mmsi_lst[0:5]:
    lst = calculate_delta_t(mmsi)
    # plt.hist(lst, range=(min(lst), min(lst)+5))
    plt.hist(lst)
    plt.show()

