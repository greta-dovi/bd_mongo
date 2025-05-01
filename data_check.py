from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27020')
# db = client["testDB"]
db = client["vesselsDB"]
collection = db["raw_data"]
# collection = db["clean_data"]

print("Total docs:", collection.count_documents({}))

for doc in collection.find().limit(5):
    print(doc)

# If data needs to be wiped out
##################################
# collection.delete_many({}) 
# print("Collection cleared.")
##################################

client.close()