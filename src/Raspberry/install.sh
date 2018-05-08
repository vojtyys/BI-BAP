#!/bin/bash
echo "Installing python3, pip3\n"
sudo apt install python3 python3-pip
echo "Installing setuptools\n"
sudo pip3 install setuptools
echo "Installing API\n"
sudo pip3 install ./pyhouse/
echo "Install finished"