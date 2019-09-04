# UDN CLI

## Installation
* requires python 3
* Although not required, it's recommended that you use virtualenv to manage the python 
environment in which the udn-cli is installed. There's a 
[good tutorial from RealPython here](https://realpython.com/python-virtual-environments-a-primer/#using-different-versions-of-python) 
on using virtual environments and Python3.  A good way to 
[install Python3 on MacOS is with Homebrew](https://docs.python-guide.org/starting/install3/osx/).   
```
$ git clone git@github.com:hms-dbmi/udn-cli.git
$ cd udn-cli
$ pip install .
```

## Configuration
This config is required to be located at `~/.udn/config`.  Tokens for UDN Gateway can be found on the API tab of both
the production and development systems.  Tokens for FileService can be obtained by logging into 
[production](https://fileservice.dbmi.hms.harvard.edu/) or [development](https//fileservicedev.aws.dbmi.hms.harvard.edu/)

```
[PROD]
host = https://gateway.undiagnosed.hms.harvard.edu/
fileservice_token = yourprodfileservicetoken
udn_token = yourprodudntoken
bucket = udnarchive
[TEST]
host = https://udndev.dbmi.hms.harvard.edu/
fileservice_token = yourdevfilservicetoken
udn_token = yourdevudntoken
bucket = udnarchive-ci
```

## Usage

Each sequencing file, say for example test1.bam, must have an accompanying file test1.bam.json in the same directory. It should be formatted in the following way:

```
{
  "patient_uuid": "asdf-asdf-asdf-asdfsd",
  "seq_request_id": 42,
  "metadata": {}
}
```
 
### Upload a single file
`udn upload <path_to_file> <seq_req_id> <patient_uuid>`
  
### Upload multiple files
`udn multi-upload <path_to_dir>`


### Logs
A new log file will be produced each time a udn-cli command is executed. They are named in the following way: `<command_name>-<YYYYMMDD>-<seconds>.log`. For example, `upload-20190603-1233322.log`.

### Options
* `--bucket <bucket>`: Upload files to a specific bucket.  Ask UDN CC for bucket options and guidance.
* `--test`: The "TEST" section in the config file will be used instead of the "PROD" section.
* `--force`: If the file that you're trying to upload already exists, the udn-cli will block the upload. You can override this behavior by setting the `--force` option. The existing data will not be overwritten, but the overriding file will now be the one referenced by the UDN gateway.
