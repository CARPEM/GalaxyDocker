FROM python:2.7

MAINTAINER Olivia Doppelt-Azeroual , William Digan william.digan@aphp.fr
#Build image ReGaTE
WORKDIR /home/
RUN git clone https://github.com/C3BI-pasteur-fr/ReGaTE.git
WORKDIR /home/ReGaTE
RUN pip install -r requirements.txt

RUN python setup.py install

RUN mkdir /results
RUN mkdir /data
WORKDIR /data
COPY configReGaTE /data
COPY startRegate.sh /data
RUN chmod +x /usr/local/bin/regate
RUN chmod +x /home/ReGaTE/*
RUN chmod +x /home/ReGaTE/regate/*
RUN chmod +x /data
CMD ["bash startRegate.sh"]

