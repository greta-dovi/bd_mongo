from pymongo import MongoClient
import math
import multiprocessing as mp


def mmsis(collection_str: str):
    with MongoClient("mongodb://localhost:27020") as client:
        db = client["vesselsDB"]
        collection = db[collection_str]

        mmsis = collection.distinct("MMSI")
        return mmsis


# mmsi_lst = mmsis()


def data_cleaning(mmsi):
    with MongoClient("mongodb://localhost:27020") as client:
        db = client["vesselsDB"]
        collection = db["raw_data"]
        collection_clean = db["clean_data"]

        obj = collection.find({"MMSI": mmsi})
        data = []
        for row in obj:
            data.append(row)

        if len(data) < 100:
            return

        clean_data = []
        for row in data:
            skip_row = False
            fields_to_check = [
                "Latitude",
                "Longitude",
                "Navigational status",
                "ROT",
                "SOG",
                "COG",
                "Heading",
            ]
            for field in fields_to_check:
                value = row.get(field, None)
                if value is None:
                    skip_row = True
                    break
                if isinstance(value, float) and math.isnan(value):
                    skip_row = True
                    break
                if field == "Latitude" and abs(value) > 90:
                    skip_row = True
                    break
                if field == "Longitude" and abs(value) > 180:
                    skip_row = True
                    break
                    

            if skip_row:
                continue

            
            clean_data.append(row)
        
        if len(clean_data) > 100:
            collection_clean.insert_many(clean_data)



# task: Identify and filter out noise based on specific criteria,
# including vessels with less than 100 data points and missing or
# invalid fields (e.g., Navigational status, MMSI, Latitude, Longitude,
# ROT, SOG, COG, Heading).

# 1616 2565 3340

# for mmsi in mmsi_lst[60:61]:  # NOTE for test purposes only!
#     data_cleaning(mmsi)

def do_parallel():
    workers = mp.cpu_count() - 1
    mmsi_lst = mmsis("raw_data")
    mmsi_lst = mmsi_lst[100:200] # NOTE: for test purposes only!
    with mp.Pool(workers) as pool:
        pool.map(data_cleaning, mmsi_lst)

if __name__ == "__main__":
    do_parallel()