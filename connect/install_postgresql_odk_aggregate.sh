#!/bin/bash
# ODK Aggregate installation script using PostgreSQL
# Tested on Ubuntu 20.04/22.04/24.04

# --- CONFIGURABLE VARIABLES ---
ODK_VERSION="2.0.5"   # Change to desired ODK Aggregate version
#ODK_WAR_URL="https://github.com/getodk/aggregate/releases/download/v${ODK_VERSION}/ODKAggregate.war"
ODK_WAR_URL="https://github.com/getodk/aggregate/releases/download/v2.0.5/ODK-Aggregate-v2.0.5.war"
DB_NAME="odk"
DB_USER="dondonedmond"
DB_PASS="IRCb@ngu12025"
PG_VERSION="14" # Change if your Ubuntu version uses another PostgreSQL version
TOMCAT_USER="tomcat"
TOMCAT_WEBAPPS="/var/lib/tomcat10/webapps"

# --- UPDATE & INSTALL DEPENDENCIES ---
sudo apt update
sudo apt install -y openjdk-11-jdk tomcat10 postgresql postgresql-contrib unzip wget

# --- CONFIGURE POSTGRESQL ---
sudo -u postgres psql <<EOF
CREATE DATABASE ${DB_NAME} WITH ENCODING 'UTF8';
CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
EOF

# --- ALLOW REMOTE CONNECTIONS IF NEEDED ---
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/${PG_VERSION}/main/postgresql.conf
echo "host    all             all             0.0.0.0/0            md5" | sudo tee -a /etc/postgresql/${PG_VERSION}/main/pg_hba.conf

sudo systemctl restart postgresql

# --- DOWNLOAD ODK Aggregate WAR ---
wget -O /tmp/ODKAggregate.war "${ODK_WAR_URL}"

# --- DEPLOY TO TOMCAT ---
sudo systemctl stop tomcat10
sudo rm -rf ${TOMCAT_WEBAPPS}/ODKAggregate*
sudo cp /tmp/ODKAggregate.war ${TOMCAT_WEBAPPS}/ODKAggregate.war
sudo chown ${TOMCAT_USER}:${TOMCAT_USER} ${TOMCAT_WEBAPPS}/ODKAggregate.war

# --- RESTART TOMCAT ---
sudo systemctl start tomcat10

echo "=================================================="
echo "ODK Aggregate installed."
echo "Access via: http://<server-ip>:8080/ODKAggregate"
echo "Database: ${DB_NAME}, User: ${DB_USER}"
echo "=================================================="
