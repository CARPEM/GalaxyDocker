![Carpem](http://www.carpem.fr/wp-content/themes/carpem/img/logo.gif)
![Docker](http://blog.cloudera.com/wp-content/uploads/2015/12/docker-logo.png)

Description
=============

This docker images is connected to a galaxy docker image [bgruening/docker-galaxy-stable:15.04](https://github.com/bgruening/docker-galaxy-stable)
For the HEGP Hospital. This docker allow to perform one click analysis.
It is based on the data-manager python package which is a wrapper around
Bioblend 0.8 and the ION proton API.

This git folder contains 2 parts

1) datamanagerpkg
2) analysisManager

* datamanagerpkg is a python package which allow you to query either the proton or
the galaxy instance

* analysisManager is the user interfaces which allow you to communicate without using 
the hard coding way. the template used is called sb Admin and can be found [here](https://blackrockdigital.github.io/startbootstrap-sb-admin/index.html#)


Usage
=========== 

see the documentation which will be ready soon
The analysis manager require:
1) First connect to the galaxy instance
2) run the Analysis-Manager.

* use Galaxy-hegp in production 

In order to use this galaxy instance in production,
we created a special git repository which will provide you instructions
to install this docker image.
To do so, clone the following git repository and follows the instruction:



data-manager
===========

docker run -d  -p 1025:1025 -p 6379:6379 -p 9000:8000  data-manager:1.0


analysismanager
===========

Port Explaination
=================

# 9000:8000 analysis manager
# 6379:6379 REDIS port
# 1025:1025 celery
start Module


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


* if any change in datamanagerpkg python package

please do 

```sh
docker build -t data-manager .
``` 
and update the docs and the web images 

* docs images do 
* When the sphinx image is ready
	1) run your container with the command
	
		```sh
		docker build -t sphinx-hegp .
		``` 
	
	2) run your container with the command
	
		```sh
		docker run -it -v pathtoTheHomeFolder:/data sphinx-hegp bash
		```

		example:
		
		```sh
		docker run -it -v /home/galaxy/Documents/git/repo/data-manager-hegp/:/data sphinx-hegp bash
		
		```
			go in docs/datamanagerpkgdoc
			do make html or latexpdf copy the doc to your home directory
			
inside the docker images run

```sh
 python manage.py makemigrations
 python manage.py migrate
 python manage.py migrate --fake-initial
``` 
To start the app please do :
```sh
exec gunicorn webmanager.wsgi:application \
    --name webdatamanager \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log
```

History
=======

- 1.0: Initial release!
	1. [CNV] communication data-manager Galaxy 
	2. [CNV] communication data-manager Proton
	3. write the datamanagerpkg as a python package
	4. ADMIN and users: set up the css, java script and font
	5. Add startbootstrap  templates
	

DONE
=====	
		
	- Make a website which display information to all current run 	
	- allow user to run some job
	- add the sphinx doc to the tool
	- DONE: display run in a table 
	- DONE automatically :allow users to refresh the run list
		a.4 DONE :add on the table a button  to run CNV analysis
		a.5 DONE : get the current user to run the job for this guy a proton GAlaxy function
		a.6 DONE : (but not check)if the run ftpstatus == '' or the user is not selected disable the button	
		D) ProtonProjects Handle Plasma:
			d.1 DONE : display the galaxy history name where the data are stored
			d.2 DONE : display the name of the file
			d.3 DONE : display the bed file name

