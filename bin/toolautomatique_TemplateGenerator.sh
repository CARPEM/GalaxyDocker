#!/bin/sh
#WDN
#define parameters which are passed in.
analysisManagerAccessionAdress=$1

cat  << EOF
 <inputs action="http://$analysisManagerAccessionAdress:9010/projects/" check_values="false" method="get">
EOF

