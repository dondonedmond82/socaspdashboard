#!/bin/bash
# ODK Aggregate install script for Ubuntu 24.04
# Tested for MySQL backend

set -e

echo "=== Updating packages ==="
sudo apt update && sudo apt upgrade -y

echo "=== Installing Java 11 ==="
sudo apt install -y openjdk-11-jdk

echo "=== Installing Tomcat 9 ==="
sudo apt install -y tomcat10 tomcat10-admin tomcat10-common tomcat10-user

echo "=== Installing MySQL Server ==="
sudo apt install -y mysql-server

echo "=== Securing MySQL Installation ==="
sudo mysql_secure_installation

echo "=== Creating ODK MySQL Database and User ==="
DB_NAME=odk_leon
DB_USER=odk_dondonleon
DB_PASS=IRCb@ngu12025

sudo mysql -e "CREATE DATABASE ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';"
sudo mysql -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

echo "=== Downloading ODK Aggregate WAR file ==="
# You can change the version here; last stable was 2.0.5
wget https://github.com/getodk/aggregate/releases/download/v2.0.5/ODK-Aggregate-v2.0.5.war -O /tmp/ODKAggregate.war

echo "=== Downloading MySQL JDBC Connector ==="
wget https://downloads.mysql.com/archives/get/p/3/file/mysql-connector-j-8.3.0.tar.gz -O /tmp/mysql-connector.tar.gz
tar -xzf /tmp/mysql-connector.tar.gz -C /tmp
JAR_PATH=$(find /tmp -name "mysql-connector-java-*.jar" | head -n 1)
sudo cp "$JAR_PATH" /usr/share/tomcat10/lib/

echo "=== Deploying ODK Aggregate WAR to Tomcat ==="
sudo cp /tmp/ODKAggregate.war /var/lib/tomcat10/webapps/

echo "=== Restarting Tomcat ==="
sudo systemctl restart tomcat10

echo "=== Installation Complete ==="
echo "Access ODK Aggregate at: http://<server-ip>:8080/ODKAggregate"
