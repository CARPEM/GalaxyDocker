############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################
# Set the base image to use to Ubuntu
FROM public-datamanager 
# Set the file maintainer (your name - the file's author)
MAINTAINER William Digan
#Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
#Local directory with project source
ENV DOCKYARD_SRC=analysismanager
#Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
#Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/analysismanager
#Update the default application repository sources list
#RUN apt-get update 
#RUN apt-get install -y python python-pip
# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media static logs
RUN mkdir /nas_backup

VOLUME [ "/nas_Dir","/nas_backup", "$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/", "/srv/"]
# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

# Install Python dependencies
RUN pip install django gunicorn
RUN apt-get update
RUN apt-get install -y sqlite3
RUN pip install django-celery redis psycopg2
RUN apt-get install -y ssmtp
RUN apt-get install -y python-dev libpq-dev postgresql postgresql-contrib 

COPY config/ssmtp.conf /etc/ssmtp/ssmtp.conf 
####
RUN apt-get install -y supervisor

COPY config/webmanagerCelery* /etc/supervisor/conf.d/
#COPY config/webmanagerRedisServer* /etc/supervisor/conf.d/
COPY config/GlobalVariables.py $DOCKYARD_SRVPROJ/sequencer/
COPY config/GlobalVariables.py $DOCKYARD_SRVPROJ/GlobalVariables.py
##install a postgres server

RUN touch /srv/logs/webmanagerCeleryWorker.log &&\
touch /srv/logs/webmanagerCelerybeat.log  

WORKDIR $DOCKYARD_SRVPROJ

#to start the server uncomment this
COPY config/entrypoint.sh $DOCKYARD_SRVPROJ
RUN chmod 777  $DOCKYARD_SRVPROJ/entrypoint.sh
RUN chmod 777  /etc/supervisor/conf.d/*
# Expose port 80 (webserver), 21 (FTP server)
EXPOSE :80
EXPOSE :8080
EXPOSE :8000
EXPOSE :21
EXPOSE :25
#WDGN to start the server uncomment this When the work is ready
CMD ["/srv/analysismanager/entrypoint.sh"]
