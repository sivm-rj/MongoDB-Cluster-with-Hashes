import threading
import pymongo
import time
import csv
import os

# Take input for the number of containers
num_containers = 1

# Set up database connections
client = [pymongo.MongoClient('localhost', 27018 + i) for i in range(num_containers)]
db = [cli['mydatabase'] for cli in client]

# Define the query function
def process_data(i, query_times):
    # Connect to the MongoDB instance in the container
    client = pymongo.MongoClient('localhost', 27018 + i)

    # Access the appropriate database and collection
    collection = db[i]['my_collection']

    # Retrieve all documents and calculate the average 'gpa'
    total_gpa = 0
    count = 0

    start_time = time.time()  # Record the start time of the query

    for document in collection.find():
        total_gpa += float(document['GPA'])
        count += 1


    end_time = time.time()  # Record the end time of the query

    # Close the MongoDB connection
    client.close()

    average_gpa = total_gpa / count if count > 0 else 0

    # Record the query time
    query_time = end_time - start_time
    query_times.append(query_time)

    return average_gpa


# Create a list to store the threads and query times
threads = []
query_times = []

# Create and start a thread for each container
for i in range(num_containers):
    thread = threading.Thread(target=process_data, args=(i, query_times))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Calculate the total query time
total_query_time = sum(query_times)
max_query_time = max(query_times)

# Print the query time for each thread in a single line
query_times_str = ' '.join([f'{t:.4f}s' for t in query_times])
print("Query Times:", query_times_str)

# Print the total query time
print("Total Query Time:", total_query_time)


# Write results to CSV file
file_exists = os.path.isfile('results_thread_query_general.csv')
with open('results_thread_query_general.csv', 'a', newline='') as f:
    fieldnames = ['Containers', 'Max Time', 'Total Time', 'Time Threads', 'Hash Algorithm', 'Data']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    writer.writerow({'Containers': num_containers, 'Max Time': max_query_time, 'Total Time': total_query_time, 'Time Threads': query_times_str, 'Hash Algorithm': 'sha256', 'Data': 10000})



