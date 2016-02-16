#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y apache2
sudo apt-get install -y libssl-dev
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip
sudo apt-get install -y apache2-mpm-prefork
sudo apt-get install -y apache2-threaded-dev
sudo pip install mod_wsgi
sudo pip install bottle
sudo apt-get install libapache2-mod-wsgi
sudo a2enmod wsgi
sudo a2enmod headers
sudo pip install pymysql
sudo echo '
<VirtualHost *:80>
  ServerName sub.localhost
  DocumentRoot /var/www/html
</VirtualHost>
<VirtualHost *:80>
    Header set Access-Control-Allow-Origin "*"
    ServerName localhost

    ServerAdmin webmaster@localhost
    WSGIDaemonProcess API user=www-data group=www-data
    WSGIScriptAlias / /var/www/API/app.wsgi

    <Directory /var/www/API>
           WSGIProcessGroup API
           WSGIApplicationGroup %{GLOBAL}
           Order deny,allow
           Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet' > /etc/apache2/sites-enabled/000-default.conf
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password 7rebrahuxetrewuc'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 7rebrahuxetrewuc'
sudo apt-get -y install mysql-server
sudo pip install bottle-sqlalchemy
mysql -u root -p7rebrahuxetrewuc -Bse "drop database apidb;"
mysql -u root -p7rebrahuxetrewuc -Bse "create database apidb;"
python /vagrant/backend/sql_ex.py
sudo service apache2 restart

if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi
