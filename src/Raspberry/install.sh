#!/bin/bash
echo
echo "Installing python3, pip3"
echo
sudo apt install python3 python3-pip
echo
echo "Installing setuptools"
echo
sudo pip3 install setuptools
echo
echo "Installing API"
echo
sudo pip3 install ./pyhouse/
echo
echo "Install finished"
