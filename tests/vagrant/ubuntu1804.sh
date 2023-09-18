#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
sudo update-locale LANG=en_US.UTF-8 LANGUAGE=en.UTF-8
# echo 'export export LC_ALL=C' >> /home/vagrant/.profile

# install python versions
# sudo add-apt-repository --yes ppa:deadsnakes/ppa
sudo apt-get update

# tools
sudo apt-get install -y mc python3-pip xvfb

# for pillow source install
#  sudo apt-get install -y libjpeg-dev zlib1g-dev

# project dependencies
sudo apt-get install -y xvfb xserver-xephyr tigervnc-standalone-server tightvncserver

# test dependencies
sudo apt-get install -y gnumeric
sudo apt-get install -y x11-utils #   for: xmessage
# sudo apt-get install -y x11-apps  #   for: xlogo
sudo pip3 install tox

# doc dependencies
sudo apt-get install -y npm xtightvncviewer
sudo npm install --global embedme
#  sudo pip install -r /vagrant/requirements-doc.txt
