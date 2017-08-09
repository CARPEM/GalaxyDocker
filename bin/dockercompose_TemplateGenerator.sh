#!/bin/sh
#WDN
#define parameters which are passed in.
POSTGRES_PASSWORD=$1
#DEBUGVALUE=False
http_proxy=$2
https_proxy=$3
GALAXY_BRAND=$4
apiKey=$5
genomes_PATH=$6
registry_PATH=$7
images_PATH=$8
REALDATA_PATH=$9
REALRESULTS_PATH=$10
REALLOGS_PATH=$11
REALRESULTS_PATH=$12
DB_port=$13
DB_redis_port=$14

cat  << EOF
version: '2'
services:
  redisam:
    image: "redis:alpine"   
    ports:
     - "$DB_redis_port:6379"   
  amdatabase:
    image: "postgres:9.3"   
    ports:
     - "$DB_port:5432"   
    environment:
     - POSTGRES_PASSWORD=$POSTGRES_PASSWORD
     - http_proxy=$http_proxy
     - https_proxy=$https_proxy
  webgalaxy:
    build:
      context: .
      args:
        - http_proxy=$http_proxy
        - https_proxy=$https_proxy
    image: prtcarpem/galaxydockerpublic
    privileged: true
    environment:
     - http_proxy=$http_proxy
     - https_proxy=$https_proxy 
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
      context: regate/.
      args:
        - http_proxy=$http_proxy
        - https_proxy=$https_proxy         
    image: public-regate
    depends_on:
      - "amdatabase"
      - "webgalaxy"
    environment:
     - http_proxy=$http_proxy
     - https_proxy=$https_proxy
    volumes:
     - $REALDATA_PATH/results:/results
    command: ["bash","startRegate.sh"] 
  publicdatamanager:
    build:
      context: data-manager-hegp/.
      args:
        - http_proxy=$http_proxy
        - https_proxy=$https_proxy 
    image: public-datamanager
  publicanalysismanager:
    build:
      context: data-manager-hegp/analysisManager/.
      args:
        - http_proxy=$http_proxy
        - https_proxy=$https_proxy          
    image: public-analysismanager
    depends_on:
      - "amdatabase"
      - "regate"
    environment:
     - http_proxy=$http_proxy
     - https_proxy=$https_proxy
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

