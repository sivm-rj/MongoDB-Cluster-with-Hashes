import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import time
import hashlib
import random
import csv
import os
import pandas as pd
import subprocess

random.seed(123)


def generate_student_data(num_students):
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


def push_data_async(data_dict, num_containers, hash_function):

    # Set up database connections
    clients = [AsyncIOMotorClient('localhost', 27018 + i) for i in range(num_containers)]
    dbs = [clients[i]['mydatabase'] for i in range(num_containers)]

    # Read data from CSV file
    # my_data = []
    # with open('students.csv', 'r') as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         my_data.append(row)

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
        coroutines = [push_to_db(data) for data in data_dict]
        await asyncio.gather(*coroutines)

    asyncio.run(main())

    # Print time taken to push data
    elapsed_time = time.time() - start_time
    print('Time taken:', elapsed_time)

    # Write results to CSV file
    file_exists = os.path.isfile('results_async_v2.csv')
    with open('results_async_v2.csv', 'a', newline='') as f:
        fieldnames = ['Containers', 'Time', 'Data', 'Hash_Algorithm']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Containers': num_containers, 'Time': elapsed_time, 'Data': len(data_dict), 'Hash_Algorithm': hash_function().name})



def main():
    data_length = [100000, 10000, 1000]
    for data_len in data_length:
        file_path = 'students.csv'
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
        generate_student_data(data_len)
        df = pd.read_csv('students.csv')
        data_dict = df.to_dict('records')
        for hash_algorithm in ['md5', 'sha1', 'sha256']:
            for num_containers in range(1, 6):
                hash_function = getattr(hashlib, hash_algorithm)
                # print(hash_function().name, num_containers, data_len)
                subprocess.run(['python', 'delete_data.py'])
                push_data_async(data_dict, num_containers, hash_function)
    


if __name__ == '__main__':
    main()