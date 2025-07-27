import asyncio
import csv
import os
import random
import subprocess
import threading
import time
from queue import Queue

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

def push_data_async(num_containers: int) -> None:

    # Set up database connections
    clients = [AsyncIOMotorClient('localhost', 27018 + i) for i in range(num_containers)]
    dbs = [client['mydatabase'] for client in clients]

    # Read data from CSV file
    my_data = []
    with open('students.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            my_data.append(row)

    # Define function to push data to database
    async def push_to_db(data):
        # Determine which database to push data to based on hash value
        hash_value = hash(data['Name']) % num_containers
        db = dbs[hash_value]
        # Insert data into appropriate database
        await db.my_collection.insert_one(data)

    # Start timer
    start_time = time.time()

    # Create and run coroutines to push data to database
    async def main():
        coroutines = [push_to_db(data) for data in my_data]
        await asyncio.gather(*coroutines)

    asyncio.run(main())

    # Print time taken to push data
    elapsed_time = time.time() - start_time
    print('Time taken:', elapsed_time)

    # Write results to CSV file
    with open('results_async.csv', 'a', newline='') as f:
        fieldnames = ['Containers', 'Time', 'Data']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({'Containers': num_containers, 'Time': elapsed_time, 'Data': len(my_data)})


def push_data_thread(num_containers: int) -> None:
    # Set up database connections
    clients = [AsyncIOMotorClient('localhost', 27018 + i) for i in range(num_containers)]
    db = [cli['mydatabase'] for cli in clients]

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
    file_exists = os.path.isfile('results.csv')
    with open('results.csv', 'a', newline='') as f:
        fieldnames = ['Containers', 'Time', 'Data']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Containers': num_containers, 'Time': elapsed_time, 'Data': len(my_data)})


def start_containers(num_containers: int) -> None:
    # Define a list of host ports to map
    host_ports = [str(2018 + i) for i in range(num)]

    # Start containers in a loop
    for i, port in enumerate(host_ports):
        # Map the container's port 27017 to the host machine's port i+1
        container_port = '27017'
        container_name = f'mongodb{i+1}'
        subprocess.run(['docker', 'run', '-d', '-p', f'{port}:{container_port}', '--name', container_name, 'mongo:latest'])


def generate_student_data(num_students: int) -> None:
    # Define possible majors
    majors = ['Computer Science', 'Mechanical Engineering', 'English', 'Biology', 'Psychology', 'History']
    
    # Define column headers
    headers = ['Name', 'Age', 'Major', 'GPA']
    
    # Initialize list to store student data
    student_data = []
    
    # Generate unique names for students
    names = set()
    x = 0
    while len(names) < num_students:
        name = 'Student{}'.format(x)
        names.add(name)
        x = x + 1
    
    # Generate student data
    for name in names:
        age = random.randint(18, 24)
        major = random.choice(majors)
        gpa = round(random.uniform(2.5, 4.0), 2)
        student_data.append([name, age, major, gpa])
    
    # Write data to CSV file
    with open('students.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(student_data)