import threading
import pymongo




# Define the query function
def process_data(container_port):
    # Connect to the MongoDB instance in the container
    client = pymongo.MongoClient(host, container_port)

    # Access the appropriate database and collection
    db = client['mydatabase']
    collection = db['your_collection_name']

    # Retrieve all documents and calculate the average 'gpa'
    total_gpa = 0
    count = 0
    for document in collection.find():
        total_gpa += document['gpa']
        count += 1

    # Close the MongoDB connection
    client.close()

    return total_gpa / count if count > 0 else 0


# Create a list to store the threads
threads = []

# Create and start a thread for each container
for port in ports:
    thread = threading.Thread(target=process_data, args=(port,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()