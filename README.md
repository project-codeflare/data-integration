# Lithops4Ray - Object Storage data processing for Ray

Object storage is widely used platform for persisting large amounts of unstructured data. The goal of 
Lithops4Ray project is to enable [Ray](https://ray.io) tasks or actors to access object data without forcing developers to write additional boiler plate code or address advanced aspects of accessing Big Data persisted in object storage. Lithops4Ray supports almost any object storage platforms, like IBM Cloud Object Storage, Amazon S3, Azure, Google, CEPH, and so on.

## Lithops4Ray

Lithops4Ray is based on the [Lithops](http://lithops.cloud)  framework that benefit Ray's task or actors to process data persisted in  the object storage. To integrate Lithops with Ray you need to install Lithops both at the head and worker nodes and configure Lithops to access object storage backend


## Installation
Configure Lithops to access the storage backend. Edit provided `../scripts/lithops_config.yaml` and update IBM Cloud Object Storage access details including storage bucket. For other object storage providers, follow [storage backends](https://github.com/lithops-cloud/lithops/blob/master/config/README.md#compute-and-storage-backends). 

Now, edit Ray's cluster `cluster.yaml` file and configure

```
file_mounts: {
  "~/lithops/lithops_config.yaml":"project-codeflare/data-integration/blob/main/scripts/lithops_config.yaml" 
 }
setup_commands:
 - echo 'export LITHOPS_CONFIG_FILE=~/lithops/default_config.yaml' >> ~/.bashrc
 - pip install lithops
```
More details on the `cluster.yaml` file can be found [here](https://docs.ray.io/en/master/cluster/config.html)

## Usage example

We run a simple example accessing CSV files and find a string match. Folder `examples/data` contains two CSV files that we use to find a string match

  	import lithops
	import ray
	import csv

	def read_csv(obj):
	    buff = io.StringIO(obj.data_stream.read().decode())
	    reader = csv.reader(buff, delimiter=',')
	    for row in reader:
	        print(row)
	        if 'John' in row[0]:
	            return'John is found in {}'.format(obj.key)
	    return 'John not found in {}'.format(obj.key) 
	
	@ray.remote
	def test_csv(data):
	    res =  data.result()
	    return res

	if __name__ == '__main__':
    
	    ray.init(ignore_reinit_error=True)
	    fexec = lithops.LocalhostExecutor(log_level=None)
	    
	    my_data = fexec.map(read_csv, 'data-integration/examples/data/', extra_args = ['John'])
	    results = [test_csv.remote(d) for d in my_data]
	
	    for res in results:
	        print(ray.get(res))

Running the code should print

	John is found in ages-part1.csv
	John not found in ages-part2.csv


## Additional material
[Accelerating object storage processing for Ray framework](https://medium.com/p/f581863c7662)

