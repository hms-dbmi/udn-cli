# UDN CLI

# Example config 
This config is required to be located at ~/.udn/config (I'll be adding an option to for configuring this).

```
[PROD]
host = https://fileservice.dbmi.hms.harvard.edu/
fileservice_token = yourprodfileservicetoken
udn_token = yourprodudntoken
bucket = udnarchive
[TEST]
host = http://fileservicedev.aws.dbmi.hms.harvard.edu/
fileservice_token = yourdevfilservicetoken
udn_token = yourdevudntoken
bucket = udnarchive-ci
```

# Installation
* requires python 3
* Although not required, it would be best to install the udn-cli using in a virtualenv.

```
$ git clone git@github.com:hms-dbmi/udn-cli.git
$ cd udn-cli
$ pip install .
```

# Usage 
## Upload a single file
`udn upload <path_to_file> <seq_req_id> <patient_uuid> --test`
  
## Upload multiple files
`udn multi-upload <path_to_dir> --test`

Each sequencing file, say for example test1.bam, must have an accompanying file test1.bam.json in the same directory. It should be formatted in the following way:

```
{
  "patient_uuid": "asdf-asdf-asdf-asdfsd",
  "seq_request_id": 42,
  "metadata": {}
}
```


  
  
