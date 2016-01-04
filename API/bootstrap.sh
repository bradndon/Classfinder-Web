#!/usr/bin/env bash

apt-get update
apt-get install -y apache2
sudo apt-get install -y libssl-dev
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip
sudo apt-get install -y apache2-mpm-prefork
sudo apt-get install -y apache2-threaded-dev
pip install mod_wsgi
pip install bottle
sudo apt-get install libapache2-mod-wsgi
sudo a2enmod wsgi
sudo service apache2 restart


if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi
