#!/bin/sh

#autologin
brew tap xfreebird/utils
brew install kcpassword
enable_autologin "vagrant" "vagrant"

# disable screensaver
defaults -currentHost write com.apple.screensaver idleTime 0

# Turn Off System/Display/HDD Sleep
sudo systemsetup -setcomputersleep Never
sudo systemsetup -setdisplaysleep Never
sudo systemsetup -setharddisksleep Never

#https://github.com/ponty/PyVirtualDisplay/issues/42
echo  "@reboot /bin/sh -c 'mkdir /tmp/.X11-unix;sudo chmod 1777 /tmp/.X11-unix;sudo chown root /tmp/.X11-unix/'" > mycron
sudo crontab mycron

brew install python3 mc pidof
brew cask install xquartz
python3 -m pip install --user pillow  pytest path.py tox

#   su - vagrant -c 'brew cask install xquartz'
#   su - vagrant -c 'python3 -m pip install --user pygame==2.0.0.dev6 pillow qtpy wxpython pyobjc-framework-Quartz pyobjc-framework-LaunchServices nose path.py'

sudo chown -R vagrant /vagrant
