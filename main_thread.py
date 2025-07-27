import os
import threading
from queue import Queue
from pymongo import MongoClient
import csv
import time

# Take input for number of containers
num_containers = 5

# Set up database connections
client = [MongoClient('localhost', 27018 + i) for i in range(num_containers)]
db = [cli['mydatabase'] for cli in client]

# Define number of threads to use
num_threads = num_containers

# Create a list of queues, one for each thread
queues = [Queue() for _ in range(num_threads)]

# Define function to push data to database
def push_to_db(queue):
    while True:
        data = queue.get()
        # Determine which database to push data to based on hash value
        hash_value = hash(data['Name']) % num_threads
        db[hash_value].my_collection.insert_one(data)
        queue.task_done()

# Create and start threads
threads = []
for i in range(num_threads):
    t = threading.Thread(target=push_to_db, args=(queues[i],))
    t.daemon = True
    t.start()
    threads.append(t)

# Read data from CSV file
my_data = []
with open('students.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        my_data.append(row)

# Start timer
start_time = time.time()

# Iterate through the data and enqueue to appropriate queue
for data in my_data:
    hash_value = hash(data['Name']) % num_threads
    queues[hash_value].put(data)

# Wait for all tasks to be completed
for queue in queues:
    queue.join()

# Print time taken to push data
elapsed_time = time.time() - start_time
print('Time taken:', elapsed_time)

# Write results to CSV file
file_exists = os.path.isfile('results_thread.csv')
with open('results_thread.csv', 'a', newline='') as f:
    fieldnames = ['Containers', 'Time', 'Data']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    writer.writerow({'Containers': num_containers, 'Time': elapsed_time, 'Data': len(my_data)})