import socket
import logging as logger
import time
import datetime
import configparser

# Read in pi configurations
parser = configparser.RawConfigParser()
parser.read(r'/home/pi/Dev/Camera/venv/src/pi-config.ini')

# Set log configuration
logger.basicConfig(filename='camera.log', level=logger.DEBUG)

# Set up tcp socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def logEvent( eventType, eventMessage, functionName ):
    if eventType == 'SUCCESS':
        logger.info(' -- ' + datetime.datetime.fromtimestamp(time.time()).strftime(
            '%Y-%m-%d %H:%M:%S') + ' --> ' + eventMessage + ' Function -> ' + functionName)
    elif eventType == 'ERROR':
        logger.debug(' -- ' + datetime.datetime.fromtimestamp(time.time()).strftime(
            '%Y-%m-%d %H:%M:%S') + ' --> ' + eventMessage + ' Function -> ' + functionName)
    elif eventType == 'WARNING':
        logger.warning(' -- ' + datetime.datetime.fromtimestamp(time.time()).strftime(
            '%Y-%m-%d %H:%M:%S') + ' --> ' + eventMessage + ' Function -> ' + functionName)

# Returns the port of the raspberry pi by name
def getTcpPort( piName ):
    section = 'Pi TCP Ports'
    if piName in parser.options(section):
        # log info event -> TCP PORT FOUND FOR ' + piName + '
        return (parser.get(section, piName))
    else:
        # log warning event -> TCP PORT NOT FOUND FOR + \'piName\'
        return 'NULL'

# Returns the ip address of the raspberry pi by name
def getIpAddress( piName ):
    section = 'Pi IP Addresses'
    if piName in parser.options(section):
        logEvent('SUCCESS', 'IP ADDRESS FOUND FOR \'' + piName + '\'', 'getIpAddress')
        return (parser.get(section, piName))
    else:
        logEvent('ERROR', 'IP ADDRESS NOT FOUND FOR \'' + piName + '\'', 'getIpAddress')
        return 'NULL'

# Returns the name of the pi from the ip address
def getPiName( ip ):
    section = 'Pi IP Addresses'
    for piName in parser.options(section):
        # if name ip matches return name
        if ip == getIpAddress(piName):
            logEvent('SUCCESS', 'PI NAME FOUND FOR \'' + ip + '\'', 'getPiName')
            return piName

    logEvent('ERROR', 'PI NAME NOT FOUND FOR \'' + ip + '\'', 'getPiName')
    return 'NULL'

def tcpListener():
    client.listen(99)
    logEvent('SUCCESS', 'LISTENING FOR TCP CONNECTIONS','tcpListener')

    while True:
        # waiting for a connection
        connection, client_address = client.accept()

        # if connection is created
        if connection:
            try:
                # try to get name from ip
                piName = getPiName(client_address)
                if piName != 'NULL':
                    logEvent('SUCCESS', 'CONNECTION ESTABLISHED FROM ' + piName + ' (' + client_address + ')', 'tcpListener')
                else:
                    logEvent('SUCCESS', 'CONNECTION ESTABLISHED FROM ' + client_address, 'tcpListener')

                while True:
                    data = connection.recv(16)
                    if data:
                        print(data)
                    else:
                        # send confirmation back
                        logEvent('SUCCESS', 'CONFIRMATION RESPONSE SENT', 'tcpListener')
                        break

            # close connection
            finally:
                logEvent('SUCCESS', 'CONNECTION CLOSED', 'tcpListener')
                connection.close()