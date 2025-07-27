import subprocess

# Define a list of host ports to map
host_ports = ['27018', '27019', '27020', '27021', '27022']

# Start containers in a loop
for i, port in enumerate(host_ports):
    # Map the container's port 27017 to the host machine's port i+1
    container_port = '27017'
    container_name = f'mongodb{i+1}'
    subprocess.run(['docker', 'run', '-d', '-p', f'{port}:{container_port}', '--name', container_name, 'mongo:latest'])
