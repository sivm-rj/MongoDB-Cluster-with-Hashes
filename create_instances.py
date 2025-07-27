import os

# Define the base directory where the MongoDB instances will be stored
print('aaa')
base_dir = os.path.expanduser("mongodb_instances")

# Define the configuration for each instance
instances = [
    {"name": "instance1", "port": 27018},
    {"name": "instance2", "port": 27019},
    {"name": "instance3", "port": 27020},
    {"name": "instance4", "port": 27021},
    {"name": "instance5", "port": 27022}
]

# Create data and log directories for each instance
for instance in instances:
    data_dir = os.path.join(base_dir, instance["name"], "data")
    log_dir = os.path.join(base_dir, instance["name"], "log")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    

    print(f"Created data directory for instance {instance['name']} at {data_dir}")
    print(f"Created log directory for instance {instance['name']} at {log_dir}")

    # Start the instance using the config file
    cmd = f"start mongod --config mongodb.conf --dbpath {data_dir} --logpath {log_dir}/mongodb.log --port {instance['port']}"
    os.system(cmd)
    print(f"Started MongoDB instance {instance['name']} on port {instance['port']}")
