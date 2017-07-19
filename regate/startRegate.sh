#!/bin/sh

file=/results/galaxyReady.txt

while [ ! -f "$file" ]
do
  echo "Galaxy instance not ready"
  sleep 30
done
ls -l /results/galaxyReady.txt
echo "in this version galaxy is not part of the docker compose we wait 40 seconds and will run the regate data generation"
sleep 360
/usr/local/bin/regate --config_file /data/regate.ini
touch /results/regateDone.txt

exit 1

