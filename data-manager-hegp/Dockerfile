FROM python:2.7

MAINTAINER William Digan Hector Countouris, william.digan@aphp.fr  hector.countouris@aphp.fr 

ENV GALAXY_USER=galaxy \
GALAXY_UID=1000 \
GALAXY_GID=1000 \
GALAXY_HOME=/home/datamanagerpkg 

RUN mkdir /home/datamanagerpkg
COPY datamanagerpkg /home/datamanagerpkg

RUN pip install --upgrade pip

RUN pip install paramiko 
RUN pip install scp
RUN pip install requests
RUN pip install bioblend
RUN mkdir /nas_Dir
WORKDIR /home/datamanagerpkg
RUN python setup.py install
WORKDIR /home/


WORKDIR /data


VOLUME ["/tmp", "/data","/nas_Dir"]
