#!/bin/sh
#WDN
echo "build the public-datamanager "
echo "Run 'buildDataManagerPKG.sh -h' in order to print a Usage() message"
HTTPPROXY="Noproxy"
HTTPSPROXY="Noproxy"
while getopts p:s:h option
do
	case "${option}"
	in
			p) HTTPPROXY=${OPTARG};;
			s) HTTPSPROXY=${OPTARG};;
			h)	echo "#####################"
				echo "use this script to build the images and define the proxy\n"
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
	docker build -t public-datamanager ../.

elif [ "$HTTPPROXY" != "Noproxy" ] && [ "$HTTPSPROXY" = "Noproxy" ] ; then
	echo "case 2"
	 docker build -t public-datamanager \
	--build-arg http_proxy="$HTTPPROXY" ../.
	   
elif [ "$HTTPPROXY" = "Noproxy" ] && [ "$HTTPSPROXY" != "Noproxy" ] ; then
	echo "case 3"
	docker build -t public-datamanager \
	--build-arg https_proxy="$HTTPSPROXY" ../.
else
	echo "case 4"
	docker build -t public-datamanager \
	--build-arg http_proxy="$HTTPPROXY" --build-arg https_proxy="$HTTPSPROXY" ../.
	
fi
