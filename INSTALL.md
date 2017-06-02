 APACHE INSTALLATION OVERVIEW

Quick Start - Unix
------------------

1) Build your image

sh buildGalaxy.sh -p "http://myproxy.example.com:8080" -s  "https://myproxy.example.com:8080"

create an image named galaxydockerpublic. 

sudo docker build -t galaxydockerpublic \
            --build-arg http_proxy="http://myproxy.example.com:8080" \
            --build-arg https_proxy="https://myproxy.example.com:8080" \
            .
            
2) Run the image
(if you are under an http or jttpsproxy do )
sh runGalaxy.sh -p "http://myproxy.example.com:8080" -s  "https://myproxy.example.com:8080"



Port Explaination
=================

```sh
#8123:80 Galaxy Web app
#9000:9000 DockerUI in order to manage galaxy container
#5005:5000 local Registry connection
#8021:21 transfer data via the FTP protocol 
#8800:8800 handle Interactive Environments
```
Requirements
============

- Ubuntu 14.04
- Kernel 3.13.0-79-generic (if not generates java defunc)
- [Docker](https://www.docker.io/gettingstarted/#h_installation)
- Access to the NasCarpem folder
  1. nas_registry
  2. nas_genomes
  3. nas_NGSbackup (not present at this time)


FAQ
=====


1) Clone Git repository
-------------------

the git repo IP can change from a run to an other.
To adjust the git remote use the command:

```sh
git remote set-url origin git@gitlabIP:galaxy/galaxy-hegp.git 
```


2) Go inside the container
---------------------------

```sh
docker exec -it galaxy_hegp bash 
```

3) check port status if problem
-------------------------------
   
- Ubuntu 14.04
Check port states

```sh
ufw status
```
Allow the galaxy ports
```sh
sudo ufw allow 8021 
sudo ufw allow 8800
sudo ufw allow 8123
sudo ufw allow 9000
sudo ufw allow 5005
```

- Centos

```sh
iptables -A INPUT -p tcp -m tcp --dport 8123 -j ACCEPT
...
```

4) change the kernel version
-------------------------------

```sh
#https://github.com/docker/docker/issues/18180
#due to generation of zombie process need to change the java kernel 
sudo apt-get update
sudo apt-get install software-properties-common -y
#sudo add-apt-repository ppa:chiluk/1533043
sudo apt-get update
sudo apt-get install linux-image-3.13.0-79-generic \
                       linux-image-extra-3.13.0-79-generic -y
```


5) Set “older” kernel as default grub entry from StakeOveflow
--------------------------------------------------------------

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

6) Python path inside the docker-galaxy-hegp container
------------------------------------------------------
```sh
/galaxy-central/.venv/
``` 

7) Galaxy supervisor conf file
------------------------------

```sh
/etc/supervisor/conf.d/galaxy.conf
``` 


Quick Start - Mac
---------------------


Quick Start - Windows
---------------------
