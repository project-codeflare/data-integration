#
# (C) Copyright IBM Corp. 2021
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from multiprocessing import Process
import ibm_boto3
from ibm_botocore.client import Config
import os
import glob

ENDPOINT = '<Endpoint to the IBM Cloud Object Storage'

ACCESS_KEY = '<access key to IBM Cloud Object Storage>'
SECRET_KEY = '<secret key to IBM Cloud Object Storage>'
#alternatively use API KEY
API_KEY = None

def get_ibm_cos_client():

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


def copy(bucket, target_key, src):
    print('Copying from {} to {}'.format(src, target_key))
    f = open(src, "rb")
    r = cos_client.put_object(Bucket=bucket, Key=target_key, Body=f)
    print('Copy completed for {}'.format(target_key))

if __name__ == "__main__":

    src = 'local path to images'
    # folder in COS. All images will be copied into bucket/<target_key_prefix>/imaage
    target_bucket = '<your IBM Cloud Object Storage bucket'
    target_key_prefix = 'myimages'

    cos_client = get_ibm_cos_client()
    src_paths = glob.glob(os.path.join(src, '*.*'))

    total = 0
    procs = []
    for index, src_path in enumerate(src_paths):
        total = total + 1
        tatget_output_dir = os.path.join(target_key_prefix, '', os.path.basename(os.path.dirname(src_path)))
        output_path = os.path.join(tatget_output_dir, os.path.basename(src_path))
        copy(output_path, src_path)
        p = Process(target=copy, args=(target_bucket, output_path, src_path))
        p.start()
        procs.append(p)
    
    for p in procs:
        p.join()
    print('All done! Total {}'.format(total))

