#!/bin/sh
#WDN
echo "build the galaxydockerpublic from Bgruning and  local sources"
echo "Run 'buildGalaxy.sh -h' in order to print a Usage() message"
HTTPPROXY="Noproxy"
HTTPSPROXY="Noproxy"
while getopts p:s:h option
do
	case "${option}"
	in
			p) HTTPPROXY=${OPTARG};;
			s) HTTPSPROXY=${OPTARG};;
			h)	echo "#####################"
				echo "use this script to run  the galaxydockerpublic image and define the proxy\n"
				echo "-p http_proxy"
				echo "-p https_proxy"
				echo "-h Display this message"
				echo "#####################"
				exit 1;;

	esac
done
 
echo $HTTPPROXY
echo $HTTPSPROXY

#~ if [ "$HTTPPROXY" == "Noproxy" and "$HTTPSPROXY" == "Noproxy"]; then
if [ "$HTTPPROXY" = "Noproxy" ] && [ "$HTTPSPROXY" = "Noproxy" ] ; then
	echo "case 1"
	docker run -d -p 8080:80   -p 5005:5000  -p 8021:21  -p 8800:8800 --privileged=true \
	-e DOCKER_PARENT=True \
	-e "GALAXY_CONFIG_BRAND=HEGP" galaxydockerpublic
	
elif [ "$HTTPPROXY" != "Noproxy" ] && [ "$HTTPSPROXY" = "Noproxy" ] ; then
	echo "case 2"
	docker run -d -p 8080:80   -p 5005:5000  -p 8021:21  -p 8800:8800 --privileged=true \
	-e DOCKER_PARENT=True \
	-e "http_proxy=$HTTPPROXY" \
	-e "GALAXY_CONFIG_BRAND=HEGP" galaxydockerpublic
	   
elif [ "$HTTPPROXY" = "Noproxy" ] && [ "$HTTPSPROXY" != "Noproxy" ] ; then
	echo "case 3"
	docker run -d -p 8080:80   -p 5005:5000  -p 8021:21  -p 8800:8800 --privileged=true \
	-e DOCKER_PARENT=True \
	-e "http_proxy=$HTTPSPROXY" \
	-e "GALAXY_CONFIG_BRAND=HEGP" galaxydockerpublic
else
	echo "case 4"
	docker run -d -p 8080:80   -p 5005:5000  -p 8021:21  -p 8800:8800 --privileged=true \
	-e DOCKER_PARENT=True \
	-e "http_proxy=$HTTPPROXY" \
	-e "http_proxy=$HTTPSPROXY" \
	-e "GALAXY_CONFIG_BRAND=HEGP" galaxydockerpublic
fi
