FROM bgruening/galaxy-stable:16.04
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
#    mkdir /etc/systemd/system/docker.service.d

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
