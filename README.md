# Lithops4Ray - Object Storage data processing for Ray framework

## Background

Object storage is a popular platform for persisting large amounts of unstructured data. The goal of 
Lithops4Ray project is to enable [Ray](https://ray.io) tasks or actors to access object data without forcing developers to write additional boiler plate code or address advanced aspects of accessing Big Data. Lithops4Ray supports almost any object storage platforms, like IBM Cloud Object Storage, Amazon S3, Azure, Google, CEPH, and so on.

## Lithops4Ray

Lithops4Ray is based on the [Lithops](http://lithops.cloud)  framework that benefit Ray's task or actors to process data persisted in  the object storage. To integrate Lithops with Ray you need to install Lithops both at the head and worker nodes and configure Lithops with specific storage backend


## Installation
The first step is to configure Lithops with the storage backend. Edit provided `../scripts/lithops_config.yaml` and update IBM Cloud Object Storage access details including storage bucket. For other object storage providers, follow [storage backends](https://github.com/lithops-cloud/lithops/blob/master/config/README.md#compute-and-storage-backends)

Now, edit Ray's cluster `cluster.yaml` file and configure

```
file_mounts: {
  "~/lithops/lithops_config.yaml":"/code-flare-data-integration/scripts/lithops_config.yaml" 
 }
setup_commands:
 - echo 'export LITHOPS_CONFIG_FILE=~/lithops/default_config.yaml' >> ~/.bashrc
 - pip install lithops
```
More details on the `cluster.yaml` file can be found [here](https://docs.ray.io/en/master/cluster/config.html)

## Usage example

We run a simple test accessing local image CSV file and count number of lines
[TO-DO]

## Big Data processing

## Additional material
[Accelerating object storage processing for Ray framework](https://medium.com/p/f581863c7662)

