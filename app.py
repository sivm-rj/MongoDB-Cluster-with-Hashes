import streamlit as st
import pandas as pd
import hashlib
from pymongo import MongoClient
import threading
from queue import Queue
import csv
import os
import time
import pymongo

session_state = {}

# Function to push data to MongoDB instances
# @st.cache(allow_output_mutation=True)
def push_data_to_mongodb(data, num_containers, hash_function):
    # print(data)
    # print(num_containers)
    # print(hash_function)
    # Set up database connections
    # for row in data:
    #     print(row)
    #     print(row['Name'])
    print("started Data Pushing")
    print(num_containers)
    print(hash_function)
    client = [MongoClient('localhost', 27018 + i) for i in range(num_containers)]
    db = [cli['mydatabase'] for cli in client]

    # Define number of threads to use
    num_threads = num_containers

    # Create a list of queues, one for each thread
    queues = [Queue() for _ in range(num_threads)]

    # Define function to push data to database
    def push_to_db(queue):
        while True:
            row = queue.get()
            # Determine which database to push data to based on hash value
            hash_value = int.from_bytes(hash_function(row['Name'].encode()).digest(), 'big') % num_threads
            db[hash_value].my_collection.insert_one(row)
            queue.task_done()

    # Create and start threads
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=push_to_db, args=(queues[i],))
        t.daemon = True
        t.start()
        threads.append(t)

    # Start timer
    start_time = time.time()

    # Iterate through the data and enqueue to appropriate queue
    for row in data:
        hash_value = hash(row['Name']) % num_threads
        queues[hash_value].put(row)

    # Wait for all tasks to be completed
    for queue in queues:
        queue.join()

    # Print time taken to push data
    elapsed_time = time.time() - start_time
    print('Time taken:', elapsed_time)
    return elapsed_time

def process_data(collection, query_times, gpa_sum):
    # Connect to the MongoDB instance in the container
    # client = pymongo.MongoClient('localhost', 27018 + i)

    # Access the appropriate database and collection
    # collection = db[i]['my_collection']

    # Retrieve all documents and calculate the average 'gpa'
    total_gpa = 0

    start_time = time.time()  # Record the start time of the query

    for document in collection.find():
        total_gpa += float(document['GPA'])


    end_time = time.time()  # Record the end time of the query

    # Close the MongoDB connection
    # client.close()

    # average_gpa = total_gpa / count if count > 0 else 0

    # Record the query time
    query_time = end_time - start_time
    query_times.append(query_time)
    gpa_sum.append(total_gpa)

def get_average_gpa(num_containers):
    client = [pymongo.MongoClient('localhost', 27018 + i) for i in range(num_containers)]
    db = [cli['mydatabase'] for cli in client]
    # Create a list to store the threads and query times
    threads = []
    query_times = []
    gpa_sum = []
    # Create and start a thread for each container
    for i in range(num_containers):
        thread = threading.Thread(target=process_data, args=(db[i]['my_collection'], query_times, gpa_sum))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(gpa_sum)
    print(query_times)
    total_gpa = sum(gpa_sum)
    query_time = max(query_times)
    return total_gpa, query_time

# CSS styles for improved layout
STYLE = """
<style>
.sidebar .sidebar-content {
    padding: 2rem;
    align-items: flex-start;
}

/* Align inputs to left */
.stTextInput>div>div>input {
    text-align: left;
}

.stSlider>div>div>div>input {
    text-align: left;
}
</style>
"""

# Streamlit application
def main():
    st.set_page_config(page_title="MongoDB Data Pusher", layout="wide")
    st.markdown(STYLE, unsafe_allow_html=True)

    st.title("MongoDB Data Pusher")

    # User inputs
    csv_file = st.sidebar.file_uploader("Upload CSV file", type="csv")
    hash_algorithm = st.sidebar.selectbox("Hash Function", ['md5', 'sha1', 'sha256', 'sha512'], index=0)
    num_containers = st.sidebar.slider("Number of Containers", min_value=1, max_value=5, value=5)

    if csv_file is not None:
        # Read CSV file into a pandas DataFrame
        @st.cache(allow_output_mutation=True)
        def load_csv(file):
            return pd.read_csv(file)

        df = load_csv(csv_file)

        # Display the DataFrame
        st.subheader("CSV Data")
        st.dataframe(df)

    # Button to start data pushing
    if st.button("Start Data Push", key='push_button'):
        # Disable the inputs during data pushing
        inputs_disabled = True

        # Push data to MongoDB instances
        hash_function = getattr(hashlib, hash_algorithm)
        elapsed_time = push_data_to_mongodb(df.to_dict('records'), num_containers, hash_function)
        st.write(f"Time Taken: {elapsed_time}")

        # Enable the inputs after data pushing is completed
        inputs_disabled = False

        # Button to retrieve query results
    if st.button("Get Query Results", key='query_button'):
        # Disable the inputs during data pushing
        inputs_disabled = True

        total_gpa, query_time = get_average_gpa(num_containers)
        total_gpa = total_gpa / len(df)
        st.subheader("Query Results")
        st.write(f"Average GPA: {total_gpa}")
        st.write(f"Query Time: {query_time} seconds")
    
        # Enable the inputs after data pushing is completed
        inputs_disabled = False
    


if __name__ == '__main__':
    main()