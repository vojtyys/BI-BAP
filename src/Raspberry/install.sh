#!/bin/bash
echo "Installing python3, pip3"
sudo apt install python3 python3-pip
echo "Installing setuptools"
sudo pip3 install setuptools
echo "Installing API"
sudo pip3 install ./pyhouse/
