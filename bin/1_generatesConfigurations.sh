#!/bin/bqsh
#WDN
#templates generations

#######################
#load variables from the
#GlobalVariables.py file definition
#######################
. ../config/configDataManager/GlobalVariables.py
echo "show first variables.."
echo $sequencer_base_url
echo $sequencer_user

#######################
#copy Analysismanager 
#configuration files
#######################
cp ../config/configDataManager/GlobalVariables.py ../data-manager-hegp/datamanagerpkg/datamanagerpkg
cp ../config/configDataManager/* ../data-manager-hegp/analysisManager/config
cp ../config/configDataManager/GlobalVariables.py ../data-manager-hegp/analysisManager/analysismanager/sequencer/
cp ../config/configDataManager/GlobalVariables.py ../data-manager-hegp/analysisManager/analysismanager/

#######################
#generate Templates for sequencer apps
#######################
#html
sh navigationtop_TemplateGenerator.sh  $galaxy_base_url > ../data-manager-hegp/analysisManager/analysismanager/sequencer/templates/sequencer/navigation_top.html
sh plasmamain_TemplateGenerator.sh  $galaxy_base_url > ../data-manager-hegp/analysisManager/analysismanager/sequencer/templates/sequencer/plasma_Main.html
cat ../templates/plasma_Main_endFile.html >> ../data-manager-hegp/analysisManager/analysismanager/sequencer/templates/sequencer/plasma_Main.html
#settings.py
sh settings_TemplateGenerator.sh  $analysisManagerAccessionAdress $DEBUG_AnalysisManager $DB_redis $DB_server $DB_port $DB_Name $DB_USER $DB_password $DB_redis_port> ../data-manager-hegp/analysisManager/analysismanager/analysismanager/settings.py
#entrypoint.sh
sh entrypoint_TemplateGenerator.sh $POSTGRES_PASSWORD $DB_server $DB_port > ../data-manager-hegp/analysisManager/config/entrypoint.sh
cat ../templates/entrypoint_endFile.txt >> ../data-manager-hegp/analysisManager/config/entrypoint.sh
chmod +x ../data-manager-hegp/analysisManager/config/entrypoint.sh
#ssmtp.conf
sh ssmtp_TemplateGenerator.sh $fromAddrOfficial $smtpServerAphp > ../data-manager-hegp/analysisManager/config/ssmtp.conf
#regate.ini
sh regate_TemplateGenerator.sh $galaxy_base_url $apiKey $fromAddrOfficial $toolsInformation > ../regate/configReGaTE/regate.ini
#automatique.xml
cat ../templates/begin_automatique.xml >../tools/automatique/automatique.xml
sh toolautomatique_TemplateGenerator.sh $analysisManagerAccessionAdress >> ../tools/automatique/automatique.xml
cat ../templates/end_automatique.xml >>../tools/automatique/automatique.xml
#######################
#Generates the docker-compose from the template file
#######################
if [ -z "$http_proxy" ]; then
echo "htttp proxy is not defined"
sh dockercomposeNoProxy_TemplateGenerator.sh $POSTGRES_PASSWORD $DB_redis_port $DB_port $GALAXY_BRAND $apiKey $genomes_PATH $registry_PATH $images_PATH $REALDATA_PATH $REALRESULTS_PATH $REALLOGS_PATH $REALRESULTS_PATH > ../docker-compose.yml

else
echo "http proxy is defined"
sh dockercompose_TemplateGenerator.sh $POSTGRES_PASSWORD $http_proxy $https_proxy $GALAXY_BRAND $apiKey $genomes_PATH $registry_PATH $images_PATH $REALDATA_PATH $REALRESULTS_PATH $REALLOGS_PATH $REALRESULTS_PATH $DB_port $DB_redis_port > ../docker-compose.yml

fi
echo "#######################"
echo "Go back to the project home directory. "
echo "The docker-compose.yml file is generated based on your configuration"
echo "in the  config/configDataManager/GlobalVariables.py file"
echo "run the following command"
echo "docker-compose build : build the image "
echo "docker-compose up -d : start the container" 

#######################
#BUILD images done from docker compose now
#######################
#~ sh buildGalaxy.sh -p $http_proxy -s $https_proxy
#~ sh runGalaxy.sh -p $http_proxy -s $https_proxy

#~ cd ../data-manager-hegp/bin/
#~ sh buildDataManagerPKG.sh  -p $http_proxy -s $https_proxy
#~ sh buildAnalysisManager.sh  -p $http_proxy -s $https_proxy



