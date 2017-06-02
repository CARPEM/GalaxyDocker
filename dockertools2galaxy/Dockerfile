FROM python:2.7

MAINTAINER William Digan Hector Countouris, william.digan@aphp.fr  hector.countouris@aphp.fr 

ENV GALAXY_USER=galaxy \
GALAXY_UID=1000 \
GALAXY_GID=1000 \
GALAXY_HOME=/home/datamanagerpkg 

RUN mkdir /home/dockertools2galaxy
COPY argparse2tool /home/argparse2tool
#RUN pip install --upgrade pip


RUN pip install bioblend
RUN mkdir /nas_Dir
RUN python setup.py install
WORKDIR /home/dockertools2galaxy


WORKDIR /data


VOLUME ["/tmp", "/data","/nas_Dir"]
