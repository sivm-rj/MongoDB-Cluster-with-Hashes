from pymongo import MongoClient


clients = [MongoClient('localhost', port) for port in [27017, 27018, 27019, 27020, 27021, 27022]]
dbs = [cli['mydatabase'] for cli in clients]
collections = [db['my_collection'] for db in dbs]
for collection in collections:
    collection.drop()

# if os.path.exists("students.csv"):
#     os.remove("students.csv")

# Connect to MongoDB
# client = MongoClient('localhost', 27017)

# # Select the database and collection
# db = client['mydatabase']
# collection = db['my_collection']

# # Delete the collection
# collection.drop()
