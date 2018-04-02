#!/usr/bin/python3

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pyhouse
dev = pyhouse.Device(1)
