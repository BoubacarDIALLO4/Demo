# AIVI infrastructure plant

`develop` | `master`  
----------|---------  
[![Build Status](https://dev.azure.com/faurecia-dsf/AIVI/_apis/build/status/aivi/aivi%20CI?branchName=develop)](https://dev.azure.com/faurecia-dsf/AIVI/_build/latest?definitionId=37&branchName=develop) | [![Build Status](https://dev.azure.com/faurecia-dsf/AIVI/_apis/build/status/aivi/aivi%20CI?branchName=master)](https://dev.azure.com/faurecia-dsf/AIVI/_build/latest?definitionId=37&branchName=master)

AIVI (Artificial Intelligence Visual Inspection) is an application that checks the quality of a car seat on a 
production line in a plant. It takes a picture of the seat and analyses it with deep learning models.

## Requirements

- Conda environment based on `environment.yml`
- Docker 18.09 or higher. The containers must be able to use **at least 3GB of RAM**
- VirtualBox 5.2 or higher
- Vagrant 2.2.4 or higher

## Development with molecule

The roles are developed and tested with the Molecule Framework.

To start developing, you need to create a dedicated Python3.6 env as such, and install some Molecule requirements 
(more system installation details [here](https://molecule.readthedocs.io/en/latest/installation.html)):

```shell
$ conda env create -f deployment/environment.yml
```

Also please install ssh-pass on your local computer. 

Then you can launch the Molecule sequence

```
$ cd deployment/ansible/roles/aivi_service
$ molecule test

└── default
    ├── destroy
    ├── dependency
    ├── syntax
    ├── create
    ├── prepare
    ├── converge
    ├── idempotence
    ├── lint
    ├── side_effect
    ├── verify
    └── destroy
```

The pipeline on Azure Devops runs the Molecule tests.

It uses a custom image, based on CentOS 7 packaging miniconda3 and docker. It is named `molecule`.

The dockerfile is hosted in the Azure repository in `dockerfile-aivi`. The resulting image is then hosted on the Azure registry.

### How to run molecule tests

Molecule will try to download the docker images and virtualbox VMs to run the tests. The credentials are used to connect to the Azure container registry. Two environment variables are used to that effect:

```bash
export export LOGIN_NAME=acrprodaivi001
export export PASSWORD=REGISTRYPASSWORD
```

with REGISTRYPASSWORD replaced by the acrprodaivi001 registry password that can be found in the KeePass database.

Almost each role has a set of tests (defined mith the testinfra library) that are checked with molecule. To run these tests:
- go to the role directory (ex: `deployment/ansible/role/init_system`)
- run the command `molecule test`

Warning : the `aivi_service` role requires the app package to run. To do so:
- You need to get the app package first (you can use the Azure Devops Web interface for that) and put it in `ansible/roles/extract_archives/files`
- You go to `ansible/role/aivi_service`
- You can run the test with this command : `APP_VERSION=X.Y.Z molecule test` where X.Y.Z is the correct app version

### How to manage AIVI services

A "proxy" service is available to manage the aivi-inference service as well as the desync services.
This service will start aivi-inference and N desync services. When stopping aivi.service, it will stop
these services, and also basler-configurator.

That way, all of the generic services are handled by one aivi service.

Doing a "systemctl start/stop/restart aivi" will start/stop/restart all aivi services.


### How to deploy AIVI without urbancode 

```
$ cd ansible
$ ansible-playbook edge_station.yml --vault-id ./.vault-pass -e 'app_version-<APP_VERSION> stations=[{"ip":"<IP_ADDRESS>","station_name":"<STATION_NAME>"}] plant_name=<PLANT_NAME>'
```
Where:
- <APP_VERSION> = app version
- <STATION_NAME> = name of the station in the configuration file structure
- <PLANT_NAME> = name of the plant in the configuration file structure
- <IP_ADDRESS> = ip address of the station in the AIVI network

The configuration file structure is located in `ansible/roles/configuration_files/files`

For example, to deploy the 1.3.4 version with the qualif configuration on 10.42.153.171:

```
$ ansible-playbook edge_station.yml --vault-id ./.vault-pass -e 'app_version=1.3.4 stations=[{"ip":"10.42.153.171","station_name":"qualif1"}] plant_name=qualif'
```

### How to deploy desync stations

In order to deploy one or multiple desync stations, one should add the configuration files in a folder
for each desync station. Here is an example:

```
$ ls -lR default_station

default_station:
total 16
drwxr-xr-x 2 pachakamakk pachakamakk 4096 19 août  14:44 desync1
drwxr-xr-x 2 pachakamakk pachakamakk 4096 20 août  13:21 desync2
drwxr-xr-x 2 pachakamakk pachakamakk 4096 20 août  13:21 desync3
drwxr-xr-x 2 pachakamakk pachakamakk 4096 19 août  14:15 inference

default_station/desync1:
total 8
-rw-r--r-- 1 pachakamakk pachakamakk 325 19 août  14:44 configuration.json
-rw-r--r-- 1 pachakamakk pachakamakk 663 19 août  14:15 pipeline.json

default_station/desync2:
total 8
-rw-r--r-- 1 pachakamakk pachakamakk 325 20 août  13:21 configuration.json
-rw-r--r-- 1 pachakamakk pachakamakk 663 19 août  14:15 pipeline.json

default_station/desync3:
total 8
-rw-r--r-- 1 pachakamakk pachakamakk 325 20 août  13:21 configuration.json
-rw-r--r-- 1 pachakamakk pachakamakk 663 19 août  14:15 pipeline.json

default_station/inference:
total 48
-rw-r--r-- 1 pachakamakk pachakamakk 13396 19 août  14:15 barcode_seat_mapping.csv
-rw-r--r-- 1 pachakamakk pachakamakk    82 19 août  14:15 configuration.json
-rw-r--r-- 1 pachakamakk pachakamakk  1229 19 août  14:15 pipeline.json
-rw-r--r-- 1 pachakamakk pachakamakk 19876 19 août  14:15 seat_templates.json
-rw-r--r-- 1 pachakamakk pachakamakk   335 19 août  14:15 wrinkle_threshold.csv
```

For each "desyncN" folder, a desync station will be deployed. The config files will be placed
in /etc/aivi/desync*.
Each desync station should be linked to the port 5000 + N. For example, if i have 3 desync stations, then:

- desync1 is linked to port 5001
- desync2 is linked to port 5002
- desync3 is linked to port 5003


#### Ansible Vault

To view the content of the vault password for the user:
```
$ ansible-vault view /path_to_vault_file/vault.yml --vault-id .vault-pass
```

## Interaction with Urban Code

Urban Code is used as an orchestrator to deploy AIVI in the plant. It is responsible to :
- deploy the `aivi.tar.gz` artefact to the central station
- extract it and run the ansible playbook for the plant
- handle rollbacks if necessary

**WIP: TO BE UPDATED**


### Dynamic inventory
To manage different inventories corresponding to different plants, Urban Code variables are used with Ansible dynamic inventory feature.
A bash variable `stations`, filled by the Urban Code variable `${p:environment/station_list_json}` is given with the necessary info in it:
``` 
[{"station_name":"station1","ip":"1.2.3.4"},{"station_name":"station2","ip":"1.2.3.5"},{"station_name":"station3","ip":"1.2.3.6"}]
```
Be careful: it has to be in json format with no space, carriage return, or newline.

Also, the Urban Code environment names have to match the plant names defined in the configuration files structure.

### Vault interface

In order to use vault with Urban Code, an Urban code secret variable `${p:environment/vault_password}` is used to export the `ANSIBLE_VAULT_PASSWORD` bash variable in the environment.

This variable is then echoed by the `vault-env.sh` script which is given to the ansible-deploy command.

## AIVI result retrieval process

### Automated pipeline

To upload the results from the edge station, the folowing mechanism is used:

- the newest AIVI results are saved in `/storage/aivi/buffer` on the edge station
- the result directory `/storage/aivi` of each edge station is mounted on the central station using [NFS](https://fr.wikipedia.org/wiki/Network_File_System).
- (To be done) a NIFI agent is in charge of uploading the results from the `buffer` directory to the datalake. 
- (To be done) when the results are uploaded, the results are moved by the Nifi agent from the buffer directory and saved following a date partitioning scheme : <YYYY>/<MM>/<DD>
- (To be done) an automatic deletion mechanism on the edge station is in charge of removing old results after a specific duration.

### Manuel extraction with USB stick

An operator may have the need to retrieve some results directly from an edge station.
However, Usbguard being enabled, one cannot simply plug a usb drive.

The process is as follows:

- The operator wants to retrieve data
- The operator plugs a key
- The operator will contact us (How to secure this? Social engineering risk)
- We connect onto the edge station
- With the following command, we retrieve the list of devices:

```
$ usbguard list-devices
```

- We spot the usb drive ID, and then authorize it:

```
$ usbguard allow-device <ID>
```

- Once the operation is done, we should block the same usb drive:

```
$ usbguard block-device <ID>
```

- Upon reboot, the USB drive won't be authorized. However, it is very important not to forget to block the USB drive.

- This process should be automated in the future. We should create a script to manage
  this and make sure no device is forgotten.

For more information about configuring usbguard, please visit the following site:

https://usbguard.github.io/documentation/configuration.html

