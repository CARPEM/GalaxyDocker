#!/bin/sh
#######################
#check if everithing is complete and put them all in script a par named cleanAlldata.sh
#######################
#delete files path with specific annotations
rm ../data-manager-hegp/datamanagerpkg/datamanagerpkg/GlobalVariables.py
rm ../data-manager-hegp/analysisManager/config/*
touch ../data-manager-hegp/analysisManager/config/./notemptyfolder
rm ../data-manager-hegp/analysisManager/analysismanager/sequencer/GlobalVariables.py
rm ../data-manager-hegp/analysisManager/analysismanager/GlobalVariables.py
#~ #######################
#~ #generate Templates for sequencer apps
#~ #######################
rm ../data-manager-hegp/analysisManager/analysismanager/sequencer/templates/sequencer/navigation_top.html
rm ../data-manager-hegp/analysisManager/analysismanager/sequencer/templates/sequencer/plasma_Main.html
rm ../data-manager-hegp/analysisManager/analysismanager/analysismanager/settings.py
#~ #######################
#~ #Generates the docker-compose frm the template file
#~ #######################
rm ../docker-compose.yml
#~ #######################
#~ #delete tmp files used to
#~ #order the container orchestration 
#~ #######################
rm ../data/results/galaxyReady.txt
rm ../data/results/regateDone.txt
rm -r ../data/INPUT/*
rm -r ../data/RESULTS/*
rm ../logs/*
rm ../regate/configReGaTE/regate.ini
#~ #######################
#~ #delete all *inspect *tar and galaxy tool *xml
#~ #for samtools_idxstats and samtools_bedcov
#~ #######################
rm ../images/inspectTest/inspect_samtools_idxstats.txt
rm ../images/inspectTest/samtools_idxstats.tar
rm ../images/multiInput/inspect_samtools_bedcov.txt
rm ../images/multiInput/samtools_bedcov.tar 
rm ../tools/samtools_docker/samtools_idxstats/samtools_idxstats.xml
rm ../tools/samtools_docker/samtools_bedcov/samtools_bedcov.xml
rm ../tools/automatique/automatique.xml 
rm ../dockertools2galaxy/*xml

