# hyperfoil-python-client
This is a python client for [Hyperfoil](https://hyperfoil.io/). 

Right now it's a wrapper for Hyperfoil's REST API. In the future, I would like to add factories for easier benchmark creation in python.

## Usage
```python
from hyperfoil import HyperfoilClient
import yaml

# Initialize client
client = HyperfoilClient('http://hyperfoil_url.com')

# Create new benchmark
with open('tests/benchmarks/hello-world.yaml') as file:
    data = file.read()
data = yaml.load(data, Loader=yaml.loader)
client.benchmark.create(params=data)

# Start benchmark
benchmark_run = client.benchmark.start('benchmark_name')

# Kill benchmark
benchmark_run.kill()

# All stats of run
stats = benchmark_run.all_stats()

# Accessing logs:
logs = client.log()
```

## Run the tests
**Before running** the tests you need to export the `HYPERFOIL_URL` environment variable.