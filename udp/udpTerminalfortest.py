import socket as udps
import time
import pickle
import datetime
import os
import sys
import json
import threading
import time #board #busio
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
        serviceComms, serviceAddr = self.serverSocket.recvfrom(16384)
        # serviceCommsStr = str(serviceComms, 'utf-8')
        # serviceCommsStr = serviceCommsStr.strip()
        # with open(self.textFilePath, "a") as textFile:
        #     tsepoch = time.time()
        #     timeStampNow = datetime.datetime.fromtimestamp(tsepoch).strftime('%Y.%m.%d %H:%M:%S:%f')
        #     #serviceCommsStrTS = str(timeStampNow) + '\t' + serviceCommsStr + '\t' + str(serviceAddr[0])
        #     serviceCommsStrTS = serviceCommsStr
        #     textFile.write(serviceCommsStrTS + "\n")
        return serviceComms


    def transmit(self):
        tsepoch = time.time()
        self.serverSocket.sendto("Text ".encode('utf-8') + str(datetime.datetime.fromtimestamp(tsepoch).strftime('%Y.%m.%d %H:%M:%S:%f')).encode('utf-8'), (self.UDP_HOST, self.UDP_PORT))
        print("Data sent at " + str(datetime.datetime.fromtimestamp(tsepoch).strftime('%Y.%m.%d %H:%M:%S:%f')))
        time.sleep(1)

    # def run(self):
    #     print("Starting socket thread.")
    #     try:
    #         while True:
    #             if self.opmode == "receive":
    #                 self.receive()
    #             elif self.opmode == "transmit":
    #                 self.transmit()
    #
    #     except Exception as e:
    #         print("Problem with main loop - reading/sending data from socket, printing them in the terminal or saving to file.")
    #         print(e)

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
    mlx_shape = (24, 32)
    # setup the figure for plotting
    plt.ion() # enables interactive plotting
    fig,ax = plt.subplots(figsize=(12,7))
    therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
    cbar = fig.colorbar(therm1) # setup colorbar for temps
    cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label
    frame = np.zeros((24 * 32,))  # setup array for storing all 768 temperatures
    t_array = []
    # Start server
    serverThreadReceive = socketThread(1, "SocketThread", UDP_HOST, UDP_PORT_LISTEN_DATA, "receive", textFileServiceComm)
    serverThreadReceive.daemon = True
    serverThreadReceive.start()

    # serverThreadTransmit = socketThread(1, "SocketThread", UDP_HOST, UDP_PORT_LISTEN_DATA, "transmit", textFileServiceComm)
    # serverThreadTransmit.daemon = True
    # serverThreadTransmit.start()


    while True:
        t1 = time.monotonic()
        try:
            #mlx.getFrame(frame)  # read MLX temperatures into frame var
            data = serverThreadReceive.receive()
            data_array = pickle.loads(data)
            therm1.set_data(np.fliplr(data_array)) # flip left to right
            therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
            t_array.append(time.monotonic() - t1)
            #print('Sample Rate: {0:2.1f}fps'.format(len(t_array) / np.sum(t_array)))
            #cbar.on_mappable_changed(therm1) # update colorbar range
            plt.pause(0.001) # required

        except ValueError:
            continue