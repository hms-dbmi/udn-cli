# udn-cli

# example config (currently it has to be at this location: ~/.udn/config)
[PROD]
host = https://produdn.com
fileservice_token = yourprodfileservicetoken
udn_token = yourprodudntoken
bucket = udnarchive
[TEST]
host = https://devudn.com
fileservice_token = yourdevfilservicetoken
udn_token = yourdevudntoken
bucket = udnarchive-ci

# install
* requires python 3.7
* python setup.py install

# example usage (upload single file)
  udn upload <path_to_file> <seq_req_id> <patient_uuid> --test
  
# example usage (upload multiple files)
Each sequencing file, say for example test1.bam, must have an accompanying file test1.bam.json in the same directory. It should be formatted in the following way:

{
  "patient_uuid": "asdf-asdf-asdf-asdfsd",
  "seq_request_id": 42,
  "metadata": {}
}

  udn multi-upload <path_to_dir> --test
  
  
