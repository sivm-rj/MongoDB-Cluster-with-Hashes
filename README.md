# MongoDB-Cluster-with-Hashes
# MongoDB Cluster with Hashes

## Overview

This project (completed on **May 16, 2023**) explores optimizing query times in MongoDB using hash-based clustering, asynchronous processing, and multi-threading. It involves distributing a large dataset across MongoDB instances using cryptographic hash functions and evaluating performance improvements.

---

## Features

- Hash-based sharding of MongoDB documents.
- Evaluation of various hash functions: SHA-1, SHA-256, SHA3-256, MD5.
- Performance analysis using asynchronous vs. multi-threaded data ingestion.
- Web application built using Streamlit.
- Benchmarking with datasets of sizes 10³, 10⁴, and 10⁵ records.

---

## Dataset Structure

```json
Student = {
    "Name": "string",
    "Age": int,
    "Major": "string",
    "CGPA": float
}
```

---

## Hash Functions Used

- **SHA-1** (vulnerable to collisions)
- **SHA-256** (more secure)
- **SHA3-256** (resistant to extension attacks)
- **MD5** (less secure)
- **Mod-based hashing** (simplistic approach)

Each function was tested by distributing 10⁶ records across 50 and 100 clusters. Below is one example result from the report:

![Hash Comparison 100 Clusters](attachment:graph_sha1_sha256_100.png)

---

## Architecture

- **MongoDB containers** deployed via Docker (v4.18.0)
- Ports mapped starting from 27017 onward.
- Max 5 containers used for local simulation.

---

## Performance Techniques

### Asynchronous Processing

- Used `asyncio` to concurrently push data.
- Works well but limited by single-thread execution.

### Multi-threading

- Used Python's `threading` module.
- Each MongoDB instance operated in a separate thread.
- Better resource utilization, significantly faster.

Graphs for data ingestion using 10⁵, 10⁴, and 10³ records:

![Async Push Time - 10^5](attachment:async_10e5.png)  
![Threaded Push Time - 10^5](attachment:thread_10e5.png)  

---

## Query Processing

Two types of queries were evaluated:

1. **Indexed (hash field) Query:** Extremely fast using MongoDB indexes.
2. **General Query:** Requires scanning all containers; multi-threading greatly improves performance.

Query response graph for 10⁵ data points using different hash functions:

![Query Performance - 10^5](attachment:query_10e5.png)

---

## Streamlit Web Application

The app includes:

- File upload for dataset (.csv)
- Choice of hash function
- Container selection
- Data ingestion timer
- Query execution with timing display

---

## Future Scope

- Deploy on real multi-machine environment.
- Add more hash and clustering methods.
- ML-based recommendations for configuration.
- Cost-performance trade-off analysis.
- Extend for varied query types.

---

## Requirements

- Python 3.8+
- MongoDB
- Docker
- Streamlit
- Libraries: asyncio, threading, pandas, numpy, matplotlib

---

## Usage

1. Install Docker and MongoDB.
2. Launch containers:
   ```bash
   docker-compose up
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Upload your CSV file and begin testing.

---

**Report Date:** May 16, 2023
