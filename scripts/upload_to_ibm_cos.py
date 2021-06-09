'''
Created on 15 Mar 2021

@author: gilv
'''
#http://vis-www.cs.umass.edu/lfw/lfw.tgz
#http://vis-www.cs.umass.edu/lfw/lfw-a.tgz

import urllib.request
import yaml
import requests
import json
import io
from multiprocessing import Process
import ibm_boto3
from ibm_botocore.client import Config
from ibm_botocore.client import ClientError
import os
import glob
import random
import string


ENDPOINT = '<Endpoint to the IBM Cloud Object Storage'

ACCESS_KEY = '<access key to IBM Cloud Object Storage>'
SECRET_KEY = '<secret key to IBM Cloud Object Storage>'
#alternatively use API KEY
API_KEY = None

BUCKET = '<your bucket in the IBM Cloud Object Storage>'

def get_ibm_cos_client(config):

    if API_KEY == None:
        print("Using access_key and secret_key")
        client_config = Config(max_pool_connections=128,
                                                   user_agent_extra='lithops-ibm-cloud',
                                                   connect_timeout=1)
        return ibm_boto3.client('s3',
                                           aws_access_key_id=ACCESS_KEY,
                                           aws_secret_access_key=SECRET_KEY,
                                           config=client_config,
                                           endpoint_url=ENDPOINT)
    else:    
        return ibm_boto3.client(service_name='s3',
                            ibm_api_key_id=API_KEY,
                            ibm_auth_endpoint="https://iam.ng.bluemix.net/oidc/token",
                            config=Config(signature_version='oauth'),
                            endpoint_url=ENDPOINT)


def generate_big_random_letters(size):
    """
    generate big random letters/alphabets to a file
    :param filename: the filename
    :param size: the size in bytes
    :return: void
    """
    chars = ''.join([random.choice(string.ascii_letters) for i in range(size)])
    return chars

if __name__ == "__main__":

    target_bucket = "gilvdata"
    os.environ['LITHOPS_CONFIG_FILE'] = '/Users/gilv/Dev/lithops/default_config.yaml'
    with open(os.environ['LITHOPS_CONFIG_FILE']) as file:
        config = yaml.full_load(file)
    
    cos_client = get_ibm_cos_client(config)
    chars = generate_big_random_letters(1024*1024*10)
     
    for ind in range(500):
        target_key = 'test/txtfile-' + str(ind) +  '.txt'
        print (target_key)
        fruit = random.choice(['oranges', 'grapefruits', 'mandarins', 'bananas'])
        data = fruit + ' ' + chars
        cos_client.put_object(Bucket=config['lithops']['storage_bucket'], Key=target_key, 
                              Body=data.encode('utf-8'))
