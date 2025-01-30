import socket as udps
import pickle
import datetime
import os
import sys
import json
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
class socketThread(threading.Thread):
    def __init__(self, threadID, name, UDP_HOST, UDP_PORT, opmode, textFilePath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.UDP_HOST = UDP_HOST
        self.UDP_PORT = UDP_PORT
        self.opmode = opmode
        self.textFilePath = textFilePath

        # Open server socket
        try:
            self.serverSocket = udps.socket(udps.AF_INET, udps.SOCK_DGRAM)
            if opmode == "receive":
                self.serverSocket.bind(('', self.UDP_PORT))
        except Exception as e:
            print("Problem with setting up socket.")
            print(e)

    def receive(self):
        #Otrzymywany datagram udp zawierający jedną ramkę w formacie numpy array
        serviceComms, serviceAddr = self.serverSocket.recvfrom(16384)
        return serviceComms


if __name__ == "__main__":
    # Read json
    try:
        with open(os.path.join(sys.path[0], "configReceiver.json"), "r") as configFile:
            configData = json.load(configFile)
        print("JSON config read.")
    except Exception as e:
        print("Problem with json file.")
        print(e)

    # Timestamp
    tsepoch = time.time()
    timeStampNow = datetime.datetime.fromtimestamp(tsepoch).strftime('%Y%m%d_%H%M%S')

    # Address list
    try:
        UDP_HOST = configData["UDP_HOST"]
        print("UDP_HOST read.")
    except Exception as e:
        print("Problem with reading UDP_HOST.")
        print(e)

    # Port
    try:
        UDP_PORT_LISTEN_DATA = configData["UDP_PORT_LISTEN_SERVICE"]
        print("UDP_PORT_LISTEN_SERVICE read.")
    except Exception as e:
        print("Problem with reading UDP_PORT_LISTEN_SERVICE.")
        print(e)

    # TXT File with service data
    try:
        textFileServiceComm = configData["textFilePath"] + "serviceComm" + timeStampNow + ".txt"
        print("Service text file created.")
    except Exception as e:
        print("Problem with reading one of the paths.")
        print(e)





    
    # Start server
    serverThreadReceive = socketThread(1, "SocketThread", UDP_HOST, UDP_PORT_LISTEN_DATA, "receive", textFileServiceComm)
    serverThreadReceive.daemon = True
    serverThreadReceive.start()




    while True:
        try:
            #Odkodowanie do właściwego formatu frame

            data = serverThreadReceive.receive()
            data_array = pickle.loads(data)



        except ValueError:
            continue