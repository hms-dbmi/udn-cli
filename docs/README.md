# UDN CLI

## Installation
* requires python 3
* Although not required, it's recommended that you use virtualenv to manage the python 
environment in which the udn-cli is installed. There's a 
[good tutorial from RealPython here](https://realpython.com/python-virtual-environments-a-primer/#using-different-versions-of-python) 
on using virtual environments and Python3.  A good way to 
[install Python3 on MacOS is with Homebrew](https://docs.python-guide.org/starting/install3/osx/).

You can also follow the steps below to update an existing installation   
```
(env)$ git clone <either https or ssh link from github>
(env)$ cd udn-cli
(env)$ pip install .
```

## Configuration
This config is required to be located at `~/.udn/config` where `~` represents your home directory. 
Tokens for UDN Gateway can be found on the API tab of both the production and development systems. 
Tokens for FileService can be obtained by logging into 
[production](https://fileservice.dbmi.hms.harvard.edu/) or 
[development](https://fileservicedev.aws.dbmi.hms.harvard.edu/). 
An example of this file is provided in this repo  as `config.example` for you to copy and edit with your own tokens. 

```
[PROD]
host = https://gateway.undiagnosed.hms.harvard.edu/
fileservice_token = yourprodfileservicetoken
udn_token = yourprodudntoken
bucket = udnarchive
[TEST]
host = https://dev.undiagnosed.hms.harvard.edu/
fileservice_token = yourdevfilservicetoken
udn_token = yourdevudntoken
bucket = udnarchive-ci
```

## Usage

Each sequencing file (e.g. test1.bam) must have an accompanying JSON file with the same base name and be located in the same directory (e.g. test1.bam.json). 
An example JSON file is below. 

The JSON file **must** include the patient UUID, the sequence request ID, site, and metadata as shown below.  Any extra 
data you wish to store must be put in the metadata field (see below).

All values should be strings or valid JSON  
```
{
  "patient_uuid": "<uuid string>",
  "seq_request_id": "<id>",
  "site": "<your site>",
  "metadata": {<valid json>}
}
```

The UDN requires that the following data be included in the metadata field: `assembly`, `coverage`, and `md5`. This tool will automatically add the `md5` value for you. Other fields such as `description` may also be included but are not required. This must be valid JSON.
```
{
  ...
  "metadata": {
    "assembly": "<assembly info>",
    "coverage": "<coverage info>",
    "description": "<other details>",
    "md5": "<md5 sum>",
  }
}
```

Valid site values include:

- `baylorseq` : Baylor Sequencing
- `mcw` : Hudson Alpha
- `baylorrna` : Baylor (RNA Sequencing)
- `dukerna` : Duke (RNA Sequencing)
- `stanfordrna` : Stanford (RNA Sequencing)
- `uclarna`: UCLA (RNA Sequencing)
- `externaldata`: External data upload

 
### Upload a single file
`udn upload <path_to_file>`
  
### Upload multiple files
`udn multi-upload <path_to_dir>`


### Logs
A new log file will be produced each time a udn-cli command is executed. They are named in the following way: 
`<command_name>-<YYYYMMDD>-<seconds>.log`. For example, `upload-20190603-1233322.log`.

### Options
* `--test`: The "TEST" section in the config file will be used instead of the "PROD" section. Used to test your local
process for uploading to our development UDN Gateway server 
* `--force`: If the file that you're trying to upload already exists, the udn-cli will block the upload. You can 
override this behavior by setting the `--force` option. The existing data will not be overwritten, but the overriding 
file will now be the one referenced by the UDN gateway.
