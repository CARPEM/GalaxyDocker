#!/bin/sh
#WDN
#define parameters which are passed in.
POSTGRES_PASSWORD=$1
#DEBUGVALUE=False
DB_redis_port=$2
DB_port=$3
GALAXY_BRAND=$4
apiKey=$5
genomes_PATH=$6
registry_PATH=$7
images_PATH=$8
REALDATA_PATH=$9
REALRESULTS_PATH=$10
REALLOGS_PATH=$11
REALRESULTS_PATH=$12

cat  << EOF
version: '2'
services:
  redis:
    image: "redis:alpine"   
    ports:
     - "$DB_redis_port:6379"   
  database:
    image: "postgres:9.3"   
    ports:
     - "$DB_port:5432"   
    environment:
     - POSTGRES_PASSWORD=$POSTGRES_PASSWORD
  webgalaxy:
    build:
      context: .
    image: prtcarpem/galaxydockerpublic
    privileged: true
    environment:
     - GALAXY_CONFIG_BRAND=$GALAXY_BRAND 
     - GALAXY_CONFIG_MASTER_API_KEY=$apiKey
    volumes:
     - $genomes_PATH:/genomes
     - $registry_PATH:/registry
     - $images_PATH:/images
     - $REALDATA_PATH:/nas_Dir 
     - $REALDATA_PATH/results:/results 
    ports:
     - "8123:80"
     - "5005:5000"
     - "8021:21"
     - "8800:8800" 
  regate:
    build:
      context: regate
    image: public-regate
    depends_on:
      - "database"
      - "webgalaxy"
    volumes:
     - $REALDATA_PATH/results:/results
    command: ["bash","startRegate.sh"] 
  publicdatamanager:
    build:
      context: data-manager-hegp/.
    image: public-datamanager
  publicanalysismanager:
    build:
      context: data-manager-hegp/analysisManager/.
    image: public-analysismanager
    depends_on:
      - "database"
      - "regate"
    volumes:
     - $REALLOGS_PATH:/srv/logs 
     - $REALRESULTS_PATH:/nas_backup
     - $REALDATA_PATH:/nas_Dir 
     - $REALDATA_PATH/results:/results     
    ports:
     - "26:25"
     - "1026:1025"
     - "9010:8000" 

EOF

