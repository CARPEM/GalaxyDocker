echo "$(date): executed script" >> /var/log/cron.log 2>&1
echo "delete docker container" >> /var/log/cron.log 2>&1
docker ps -a |grep "rocker/shiny"|awk '{print "python /usr/local/bin/checkContainerTime.py "$1}' | bash  >> /var/log/cron.log 2>&1
