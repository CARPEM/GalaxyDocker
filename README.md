# GalaxyDockerPublic

![Carpem](http://www.carpem.fr/wp-content/themes/carpem/img/logo.gif)![Docker](http://blog.cloudera.com/wp-content/uploads/2015/12/docker-logo.png)

### Table of content

* [Requirements](#requirements)
* [Automated installation](#autoinstall)
* [Using the platform](#usage)
* [(optional) manual installation](#manualinstall)

# Introduction
This docker image was based on the [bgruening/docker-galaxy-stable:16.04](https://github.com/bgruening/docker-galaxy-stable)
and was developed for the [European Hospital Georges Pompidou](http://hopital-georgespompidou.aphp.fr/) (HEGP). This project is based on docker-compose and on the *docker in docker* deployment facility.

This project uses 7 docker containers :
- Galaxy: A bioinformatics analysis management platform, managing tools and pipelines
- DataManager/analysisManager: a web interface to faciliate an automatized NGS analysis
- PostgreSQL: A database that contains the analysis manager database
- ReGaTE: to generate the annotation of tools using the EDAM ontology
- Redis server: used by the analysis manager to generate cron job
- DockerTools2Galaxy: to generate galaxy xml file from a docker image.
 

The following instructions will describe the prerequisites, installation and the deployement of the system.

## <a name="requirements"></a>Requirements

- OS:
    - Recommanded: Ubuntu 14.04 64 bits
    - Kernel 3.13.0-79-generic (if not changed. Processes could generated java defunc/Java zombie process)

The Kernel change is strongly recommended for production platform, not need for development purpose. Please see the [section kernel change](#kernelchange) for more information.

- Required packages:
    - [Docker version 1.12](https://www.docker.io/gettingstarted/#h_installation)
    - Docker-compose version 1.12


### Install docker

```sh
wget https://apt.dockerproject.org/repo/pool/main/d/docker-engine/docker-engine_1.12.3-0~trusty_amd64.deb 
dpkg -i docker-engine_1.12.3-0~trusty_amd64.deb 
rm docker-engine_1.12.3-0~trusty_amd64.deb 
```

### Install docker-compose

```sh
curl -L https://github.com/docker/compose/releases/download/1.12.0/docker-compose-`uname -s`-`uname -m` > docker-compose 
sudo cp docker-compose /usr/local/bin/docker-compose
```

### Manage Docker as a non-root user

Add the docker group if it does not already exist:

```sh
sudo groupadd docker
```

Add the connected user "$USER" to the docker group. Change the user name to match your preferred user if you do not want to use your current user:

```sh
sudo gpasswd -a $USER docker
```

Either do a newgrp docker or log out/in to activate the changes to groups.
You can use

```sh
docker run hello-world
```

to check if you can run docker without sudo

### Folder mapping

- bin : contains the main scripts generating the Analysis manager
- templates : contains some templates needed by the scripts in the bin folder
- config : contains the main configuration files
- data : contains temporary files needed for the docker-compose generation
- test_data : contains the files needed by the AnalysisManager
- images : contains template images for samtools used as material for the dockertools2galaxy tutorials
- dockertools2galaxy : contains the scripts needed for the tool dockertools2galaxy
- interactiveShiny : contains interactive shiny environment used by Galaxy
- tools : contains the tools used by Galaxy
- ReGaTE : the regate docker configuration files
- data-manager-hegp : the data-manager and analysismanager main script
- img : location of images used by this readme
- logs : contains Analysis Manager logs

## Exposed Port

### Docker port mapping association

Ports reads as:
```
host port:docker port
```

Ports | Usage
------|------
8123:80   | Galaxy Web app
9010:8000 | Analysismanager
5005:5000 | local registry connection (not connected)
8021:21   | transfert data  to galaxy via FTP protocol 
8800:8800 | handle Galaxy Interactive Environments
6379:6379 | Redis server
5432:5432 | Postgre Database

### <a name="ports"></a> Firewall ports opening

Ubuntu 14.04 check port states
```sh
ufw status
```

Open Galaxy ports

```sh
sudo ufw allow 5432 
sudo ufw allow 9010
sudo ufw allow 8123
sudo ufw allow 5005
sudo ufw allow 6379
sudo ufw allow 8800
sudo ufw allow 8021
```

# <a name="autoinstall"></a> Automated installation
## Local configuration

* All configuration files are located on the folder config. 

Start to edit the file 

```sh
vi ./config/configDataManager/GlobalVariables.py
```
and define all the main variables such as *http_proxy* and the *serverName*

* Go to the folder bin. It contains all the templates file Generator to 
automatize and faciliate as much as possible the Analysis Manager Deployment.

```sh
cd bin
```

* Run the following scripts

```sh
#to clean all configuration files 
sudo sh cleanAlldata.sh
#This script will build the image of two samtools galaxy tools and build the 
#tool.xml file associated 
sudo sh 0_generatestoolconfig.sh
#This script will build the generate the configuration file needed to Galaxy 
#and the Analysis Manager
sudo bash 1_GenerateConfiguration.sh
```

## Generating the containers

*  Go back to the main folder with the command and build the project with 
docker-compose. It will take a certain time.

```sh
cd ..
sudo docker-compose build
```

## Starting the system

* Before you start Galaxy, be sure that all the port are open (cf. the section related to the [port opening](#ports)).

Please note that the whole process takes around *ten minutes*. The regate container waits ***5 minutes*** after the 
launch of *webgalaxy container*. 

Run the application with:

```sh
#Start all the containers
sudo docker-compose up -d
#To see the logs run
sudo docker-compose logs -f

#to go  inside the container
docker exec -it galaxydocker_webgalaxy_1 bash 
#if a new build is performed to clean tmp files generated go to bin and run
cd bin
sudo sh cleanTmpdata.sh
```

# <a name="usage"></a> Using the platform

## Start Galaxy and the use the Analysis manager.

1. Follow the Installation section to know how to run Galaxy and the Analysis
manager. When the Galaxy Instance is ready, Register a new  Galaxy user in the login section

![LoginGalaxy](img/Galaxy_login.png)

2. To access the Analysis Manager in the tool panel performed a left click on the link
*Automatic Analysis*. You will be send to the Analysis Manager interface. 
*(It take 5 minutes more for the Analysis Manager to be ready.)*

![LoginTOAM](img/Galaxy_TOAM.png)

3. In the *Home page* you can directly run example. Just click on the start buttton.
In the *Downloads page*, you can update the number and backup a specific run.
Our work is able to connect to an Ion Torrent sequencer.

![AM](img/AM.png)

## How to use a Shiny environnemt

1. You need to be log in Galaxy.
2. Load a tabulate file and it will be available 
3. Make a left click on the *Vizualize" Button and select Shiny. *(The
first time it will appear after 2 min the download of the docker image takes some times)*
![shiny](img/shiny.png)

## Optaining the reproducibility logs

Log into postgresl
```sh
PGPASSWORD=postgres
psql  -h "yourservername" -p 5434 -d "analysismanager" -U "postgres"
```

Execute the following queries
```sql
-- first command
select  job_create_time, job_user_email_id,job_tool_id_id,job_params,job_inputs
from sequencer_usercommonjobs;
-- second command
SELECT *
FROM sequencer_workflowstools_inputlist as inpp, sequencer_supportedfiles as supp
WHERE inpp.supportedfiles_id = supp.id;
```

 id |                  workflowstools_id                  | supportedfiles_id | id | dataHandle |     dataDescription     |       dataFormatEdamOntology       
----|-----------------------------------------------------|-------------------|----|------------|-------------------------|-------------------------------------

the table of the genome was obtain by parsing the file hegpGenomes.loc
which contains our reference genome. it is the only file present on the tool_data_table_conf.xml.sample


# <a name="manualinstall"></a>(Optional section) Manual installation

## Build a galaxy xml with dockertools2galaxy


1. Download the image biocontainers/samtools:1.3.1 with 

```sh
sudo docker pull biocontainers/samtools:1.3.1
```

2. Go to the folder images/inspectTest and look at the Dockerfile.
We define some variables in order to directly generates the xml tool for
Galaxy from define environment Variable inside the Docherfile. Follow the 
instruction in the README.md file of dockertools2galaxy.
To go further, we build the image and save the configuration to a file with the
following command.

```sh
cd images/inspectTest
sudo sh build_image.sh
sudo docker inspect samtools_idxstats
```

3. In the folder dockertool2galaxy the python script will take as 
input the inspect.out and build a tool.xml file. Run the following command to perform 
this operation.

```sh
cd dockertools2galaxy/
python dockertools2galaxy.py -i ../images/inspectTest/inspect_samtools_idxstats.txt -o ../tools/samtools_docker/samtools_idxstats/samtools_idxstats.xml
python dockertools2galaxy.py -i ../images/multiInput/inspect_samtools_bedcov.txt -o ../tools/samtools_docker/samtools_bedcov/samtools_bedcov.xml
```

# Technical considerations
## <a name="kernelchange"></a>Change Linux Kernel
### Download a specific kernel version

```sh
#https://github.com/docker/docker/issues/18180
#due to generation of zombie process need to change the java kernel 
sudo apt-get update
sudo apt-get install software-properties-common -y
#sudo add-apt-repository ppa:chiluk/1533043
sudo apt-get update
sudo apt-get install -y linux-image-3.13.0-79-generic linux-image-extra-3.13.0-79-generic
```

### Set an “older” kernel as default grub entry (source: StakeOveflow)

```sh
#https://github.com/docker/docker/issues/18180
#due to generation of zombie process need to change the java kernel 
sudo cp /etc/default/grub /etc/default/grub.bak
```

Then edit the file using the text editor of your choice (ie. gedit, etc.).

```sh
sudo gedit /etc/default/grub
###examples:
##kernel 4.2.2 --> 0
#GRUB_DEFAULT="0"
##Kernel 3.13.0.79 --> 1>2 (the one you want)
GRUB_DEFAULT="1>2"
```

Finally update Grub and reboot your server/machine

```sh
sudo update-grub
sudo reboot
``` 
