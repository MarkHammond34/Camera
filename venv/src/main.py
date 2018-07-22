import socket
import logging as logger
import time
import datetime
import configparser

# Read in pi configurations
parser = configparser.RawConfigParser()
parser.read(r'C:\Users\Mark\PycharmProjects\CameraPi\venv\pi-config.ini')

# Set log configuration
logger.basicConfig(filename='central.log', level=logger.DEBUG)