#!/bin/sh

# https://chocolatey.org/blog/remove-support-for-old-tls-versions
PowerShell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12"
# https://chocolatey.org/courses/installation/installing?method=install-from-powershell-v3
PowerShell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex"

choco install python -y
choco install fsviewer -y
# choco install imagemagick -y
# choco install wxpython -y 
# choco install gtk-runtime -y
# choco install pyqt4 -y
# choco install pyqt5 -y

python -m pip install -U pip
python -m pip install tox

# cd /cygdrive/c/vagrant
# tox -e py38-win