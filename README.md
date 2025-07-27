# MongoDB Cluster with Hashes

## Project Overview
This project focuses on enhancing the performance of MongoDB query searches by dividing a large database into smaller clusters using hash functions. Each smaller database (cluster) contains approximately equal numbers of entries, enabling faster search times through parallel processing of these clusters.

The goal is mathematically represented as:

> k > max(k1 + k2 + k3 + ....)  

where  
- *k* = average query search time in the larger database  
- *k1, k2, k3…* = search times in smaller databases processed concurrently

## Choosing an Appropriate Hash Function

### Hash Functions Used:
- **SHA-1:** Produces 160-bit output. Vulnerable to collision attacks.
- **SHA-256:** Produces 256-bit output. More secure than SHA-1 but susceptible to length extension attacks.
- **MD5:** Produces 128-bit output. Less secure compared to SHA algorithms.
- **SHA3-256:** Enhanced resistance to attacks, particularly length extension attacks.

### Additional Approach:
- **Mod function:** Uses ASCII conversion and modulus by the number of clusters but has limitations when deleting elements and works best with serialized keys like admission numbers.

### Findings:
- All hash functions produced similar clustering results with Gaussian distribution characteristics improving when cluster count increases.
- The choice of hash function depends on the data type and query pattern (e.g., mod function for serialized primary keys).

## Data Pushing to the Database

- **Database Used:** MongoDB (NoSQL, scalable, flexible).
- **Environment Simulation:** Docker containers run multiple MongoDB instances on a single machine.
- **Container Ports:** Default MongoDB port is 27017, subsequent containers mapped to 27018, 27019, etc.
- **Container Limit:** Max 5 containers for resource management.

### Methods to Increase Speed:
- **Asynchronous Functions:** Use of Python’s `asyncio` to push data simultaneously to containerized MongoDB instances.
- **Multi-threading:** Use of Python’s `Threading` module ensures each container runs on a separate thread, effectively utilizing system resources compared to asynchronous single-threaded approach.

### Performance Observations:
- Multi-threading drastically reduces data push time compared to asynchronous functions.
- More containers reduce push time due to better resource allocation.
- Different hash functions perform similarly but depend on dataset properties.

## Query Searching

Two types of queries tested:

1. **Query using the hash field:**  
   - Uses MongoDB indexing.
   - Search time is O(log n), very fast.
   - Number of containers has little effect on time due to indexed search.

2. **General Query (non-indexed):**  
   - Requires linear search O(n).
   - Parallelized search across multiple containers using multi-threading.
   - Increasing containers significantly improves performance.

## Application

A web application was developed with Python’s Streamlit to:

- Accept CSV uploads to load data into the database.
- Allow user selection of hash function.
- Choose the number of MongoDB containers.
- Show time taken to push data.
- Enable query searching and display results along with container-wise execution times.

## Future Scope

- Experiment with additional hash functions and clustering algorithms.
- Deploy on multiple physical machines instead of Docker containers to remove instance limits.
- Use machine learning to suggest optimal hash functions and container counts based on hardware.
- Provide cost-benefit analysis of processing power vs efficiency improvements.
- Minimize overhead in multi-machine setups.
- Test with a broader range of query types.

## Summary

This project creates a scalable and efficient approach to storing and querying large datasets in MongoDB by clustering data with hash functions and leveraging multithreading and containerization for parallel processing, significantly improving search and insertion times.

Thank you.
