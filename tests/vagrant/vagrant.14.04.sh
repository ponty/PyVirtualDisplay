#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
sudo update-locale LANG=en_US.UTF-8 LANGUAGE=en.UTF-8
# echo 'export export LC_ALL=C' >> /home/vagrant/.profile

# install python versions
sudo add-apt-repository --yes ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.6-dev
sudo apt-get install -y python3.7-dev
# sudo apt-get install -y python3.8-dev
# sudo apt-get install -y python3-distutils

# tools
sudo apt-get install -y mc xvfb curl

# for pillow source install
#  sudo apt-get install -y libjpeg-dev zlib1g-dev

# project dependencies
sudo apt-get install -y xvfb xserver-xephyr vnc4server

# test dependencies
sudo apt-get install -y gnumeric
sudo apt-get install -y x11-utils #   for: xmessage
sudo apt-get install -y x11-apps  #   for: xlogo
sudo curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
sudo python3.6 /tmp/get-pip.py
sudo python3.6 -m pip install tox

# doc dependencies
#  sudo apt-get install -y imagemagick graphviz
#  sudo pip install -r /vagrant/requirements-doc.txt
