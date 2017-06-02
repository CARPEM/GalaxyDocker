#!/bin/sh
#WDN
#define parameters which are passed in.
POSTGRES_PASSWORD=$1
DB_server=$2
DB_port=$3
#define the template.
cat  << EOF
#!/bin/bash

############################
#Set environment variables
############################
set -e

############################
#Collect Static Files
############################
python manage.py collectstatic --noinput  # Collect static files

############################
#Check postgres and construct
#the analysismanager DB
############################
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_server" -p $DB_port  -d "postgres" -U "postgres" -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 10
done
>&2 echo "Postgres is up:  executing command to construct the DB"

if PGPASSWORD=$POSTGRES_PASSWORD  psql  -h "$DB_server" -p $DB_port -d "postgres" -U "postgres" -lqt | cut -d \| -f 1 | grep -qw analysismanager; then
    >&2 echo "DATABASE ALREADY EXIST, ONLY UPDATE THE DATABASE"
    >&2 echo "Delete celery.pid files"
    rm /srv/webmanager/celerybeat*
    # database exists
    # $? is 0
else
    PGPASSWORD=$POSTGRES_PASSWORD psql  -h "$DB_server" -p $DB_port -d "postgres" -U "postgres" -c """CREATE DATABASE analysismanager;"""
    PGPASSWORD=$POSTGRES_PASSWORD psql  -h "$DB_server" -p $DB_port -d "postgres" -U "postgres" -c """CREATE USER analysismanageruser WITH PASSWORD 'analysismanager';ALTER ROLE analysismanageruser SET client_encoding TO 'utf8';ALTER ROLE analysismanageruser SET default_transaction_isolation TO 'read committed';GRANT ALL PRIVILEGES ON DATABASE analysismanager TO analysismanageruser;"""
    # ruh-roh
    # $? is 1
fi

############################
#migrate the analysismanager DB
#to the postgre container
############################
python manage.py makemigrations # Apply database migrations
python manage.py migrate        # Apply database migrations

############################
#wait until the regate container 
#is up.  wait until  the file
#below is generated
############################
file=/results/regateDone.txt

EOF
