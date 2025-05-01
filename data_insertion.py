import pandas as pd
import numpy as np
from pymongo import MongoClient
from multiprocessing import Process

#------------------------------------------------------------------------------------
# Small file for testing purposes
# CSV_FILE = "vessel_265410000.csv"
# DB_NAME = "testDB"
CSV_FILE = "aisdk-2025-01-23.csv"
DB_NAME = "vesselsDB"
MONGO_URI = 'mongodb://localhost:27020'

COLLECTION_NAME = 'raw_data'
NUM_PROCESSES = 10

def insert_chunk(chunk):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    batch_size = 1000
    for i in range(0, len(chunk), batch_size):
        batch = chunk[i:i + batch_size]
        batch = batch.to_dict(orient="records")
        collection.insert_many(batch)
        
    client.close()


def main():
    df = pd.read_csv(CSV_FILE)
    print("df size", df.shape)
    chunks = np.array_split(df, NUM_PROCESSES)


    processes = []

    for chunk in chunks:
        p = Process(target=insert_chunk, args=(chunk,))
        p.start()
        processes.append(p)

    
    for p in processes:
        p.join()

    print("Parallelized data insertion complete.")

if __name__ == '__main__':
    main()