FROM bgruening/galaxy-stable:19.0119
MAINTAINER  William Digan william.digan@aphp.fr, Hector Countouris  hector.countouris@aphp.fr 

########################
#####GALAXY CONFIG######
########################
###copy our tools to galaxy-central
COPY tools/ /galaxy-central/tools/

COPY interactiveShiny /galaxy-central/config/plugins/interactive_environments/interactiveShiny
ADD config/configGalaxy/tool_conf.xml.sample /galaxy-central/config/tool_conf.xml
ADD config/configGalaxy/job_conf.xml /galaxy-central/config/job_conf.xml
COPY config/configGalaxy/startup /usr/bin/startup
RUN chmod 777 /usr/bin/startup

RUN cat /etc/sudoers |awk '{print $0}END{print "galaxy  ALL = (root) NOPASSWD: SETENV: /usr/bin/docker \nroot  ALL = (root) NOPASSWD: SETENV: /usr/bin/docker \ngalaxy ALL = NOPASSWD : ALL"}' > /etc/sudoers 



#Add to Delete shiny container which are not automatically deleted
# Install cron
RUN apt-get update
RUN apt-get install cron

###FOR SHINY ENVIRONMENT from
# Add crontab file in the cron directory FROM https://github.com/cheyer/docker-cron.git
ADD config/configShinyApp/crontab /etc/cron.d/simple-cron

# Add shell script and grant execution rights
ADD config/configShinyApp/cronShinyTask.sh /usr/local/bin/cronShinyTask.sh
RUN chmod +x /usr/local/bin/cronShinyTask.sh
ADD config/configShinyApp/checkContainerTime.py /usr/local/bin/checkContainerTime.py
RUN chmod +x /usr/local/bin/checkContainerTime.py

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log


RUN mkdir /images
WORKDIR /galaxy-central/
VOLUME ["/export/", "/data/", "/registry/", "/genomes", "/images"]

EXPOSE :80
EXPOSE :21
EXPOSE :8800
###registry port
EXPOSE :5000
#dockerui for the galaxy container
EXPOSE :9000

# Autostart script that is invoked during container start
#CMD ["/usr/bin/startup"]
