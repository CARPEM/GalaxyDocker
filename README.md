# GalaxyDockerPublic
===========

![Carpem](http://www.carpem.fr/wp-content/themes/carpem/img/logo.gif)![Docker](http://blog.cloudera.com/wp-content/uploads/2015/12/docker-logo.png)

This docker image was based on the [bgruening/docker-galaxy-stable:16.04](https://github.com/bgruening/docker-galaxy-stable) and was developed for HEGP. This project is based on docker-compose and on the docker in docker deployment facility. 
This project used 7 docker containers :
- Galaxy : A web interface for NGS analysis
- DataManager/analysisManager a web interface to faciliate an automatize NGS analysis
- Database (Postgre) which contains the analysis manager database
- Regate : to generate EDAM ontology
- Redis server : use by the analysis manager to generate cron job
- DockerTools2Galaxy: to generate galaxy xml file from a docker image.
 

The following instructions will describe you what are the prerequisites,
 how to install the project and how to run it.

1.A : Prerequisites
===========

This work was performed on a Linux server 


1.B Port Explaination
===========
-          8123:80     -  Galaxy Web app
-          9010:8000 - Analysismanager
-          5005:5000 - local registry connection (not connected)
-          8021:21     - transfert data  to galaxy via FTP protocol 
-          8800:8800 - handle Galaxy Interactive Environments
-          6379:6379 - Redis server
-          5432:5432 - Postgre Database

1.C Requirements
===========

- Ubuntu 14.04
- Kernel 3.13.0-79-generic (if not generates java defunc also called Java zombie process)
- [Docker](https://www.docker.io/gettingstarted/#h_installation)


1.D : Installing
===========
1)      All configuration files are located on the folder config. 
		First start to edit the file config/configDataManager/GlobalVariables.py and define all the main variables such as http_proxy and the serverName
2)      Go to the folder : cd bin
3)      Run the script 1_GenerateConfiguration.sh
4)      Go back to the main folder with the command  cd ..
5)      Build all the project images with : docker-compose build
6)      Before you start galaxy, be sured that all the port are open cf (FAQ 4.2)
7)      Build all the container with         : docker-compose up -d
8)      To see the logs run docker-compose logs -f

1.E : Tutorial
===========

1) how to use the analysis manager
To use the Analysis manager you need first to create a count to the galaxy interface.
 Secondly, you click on the link "Analyse Automatique"
  You can update the number of run .
   this is working with a ion Torrent proton sequence.
   
2)     generate the xml tool from a docker image

inside the folder image you will found a samtools.tar image.
(i) You will need to rebuild this image with the Dockerfile in the inspecFile folder..
(ii) Run the docker inspect command and save the output to a file inspect.out
(iii) In the folder dockertool2galaxy the python script will take as input the inspect.out and build a tool.xml file

3) how to use a shiny environnemt

	(i) You need to be log in Galaxy.(ii) Load a text file and it will be available 
	from the interactive environmment menu 
	
4) the sql command to obtain the same table

PGPASSWORD=postgres psql  -h "yourservername" -p 5434 -d "analysismanager" -U "postgres"

-- first command
select  job_create_time, job_user_email_id,job_tool_id_id,job_params,job_inputs
from sequencer_usercommonjobs;

-- second command
SELECT *
FROM sequencer_workflowstools_inputlist as inpp, sequencer_supportedfiles as supp
WHERE inpp.supportedfiles_id = supp.id;
 id |                  workflowstools_id                  | supportedfiles_id | id | dataHandle |     dataDescription     |       dataFormatEdamOntology       
----+-----------------------------------------------------+-------------------+----+------------+-------------------------+-------------------------------------

the table of the genome was obtain by parsing the file hegpGenomes.loc
which contains our reference genome. it is the only file present on the tool_data_table_conf.xml.sample

3) License

This project is licensed under the MIT License
 
The MIT License (MIT)
Copyright (c) <2017> <APHP-HEGP>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 


4) FAQ

4.1 : Go inside the container

```sh
docker exec -it galaxy_hegp bash 
```

4.2 : Check port status if problem

Ubuntu 14.04 check port states
```sh
ufw status
```
Allow the galaxy ports
```sh
sudo ufw allow 8021 
sudo ufw allow 8800
sudo ufw allow 8123
```
Do the same for all the following ports
#9000 5005 6379 5434 1026 25 9011

4.3 : Download a specific kernel version

```sh
#https://github.com/docker/docker/issues/18180
#due to generation of zombie process need to change the java kernel 
sudo apt-get update
sudo apt-get install software-properties-common -y
#sudo add-apt-repository ppa:chiluk/1533043
sudo apt-get update
sudo apt-get install linux-image-3.13.0-79-generic \
sudo apt-get linux-image-extra-3.13.0-79-generic -y
```


4.4 :Set “older” kernel as default grub entry from StakeOveflow
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

Finally update the Grub. and reboot your machine

```sh
sudo update-grub
sudo reboot
``` 
