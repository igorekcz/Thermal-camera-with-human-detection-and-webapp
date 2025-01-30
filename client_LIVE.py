import socketio
import time
import base64
from frame import Frame
from udp import udpTerminalReceiver
import pickle

#socket.io client
sio = socketio.Client()

class autoConfig:
    def __init__(self, configFCount) -> None:
        self.configFCount = configFCount
        self.avgTemps = []
        self.running = True
    
    def addTemperature(self, temp):
        self.avgTemps.append(temp)
        if len(self.avgTemps) == self.configFCount:
            self.running = False
            return self.returnParameter()
        return None
    
    def returnParameter(self):
        avgTemp = sum(self.avgTemps) / len(self.avgTemps)
        return avgTemp
    
    def startNewConfig(self, configFCount):
        self.__init__(configFCount)
    
def startConfig(amountOfFrames = 15):
    global config
    config.startNewConfig(amountOfFrames)

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

def send_image(image_data, frame_id):
    sio.emit('frame_image', {'image': base64.b64encode(image_data).decode('utf-8'), 'frameID': frame_id})

def send_detection_info(detection_info):
    sio.emit('detection_info', {'detection': detection_info})

def get_detection_summary(frame):
    detection_str = str(frame)
    words = detection_str.split()
    if words[0] == "Detected":
        return f"{words[0]} {words[1]} {words[2]}"
    else:
        return "No humans detected"

def send_temperature_info(human_temp, isBackground):
    sio.emit('temperature_info', {'temperature': human_temp, 'isBackground': isBackground})

def get_temperature_summary(human_temperature):
    if human_temperature == []:
        return None
    else:
        return ', '.join(f"{temp}°C" for temp in human_temperature)
    

video_height = 24
video_width = 32
human_temp_min = 23
human_temp_max = 38
min_human_area = 80
config = autoConfig(15)
        
sio.connect('http://127.0.0.1:5000')


i = 0

while True:
    try:
        #Odkodowanie do właściwego formatu frame

        data = udpTerminalReceiver.serverThreadReceive.receive()
        data_array = pickle.loads(data)

        flattened = [item for sublist in data_array for item in sublist]

        frame = Frame(i, video_width, video_height, human_temp_min, human_temp_max, min_human_area, flattened)
        i += 1

        img = frame.getJpeg(50)
        send_image(img, frame.frameID)

        detection_info = get_detection_summary(frame)
        send_detection_info(detection_info)

        human_temperature = frame.getMaxTemps()
        background_temperature = frame.getAvgTemp()
        temperature_info = get_temperature_summary(human_temperature)
        if temperature_info is None:
            send_temperature_info(f"{background_temperature}" + "°C", True)
        else:
            send_temperature_info(temperature_info, False)

        if config.running:
            configRes = config.addTemperature(frame.getAvgTemp())
            if configRes is not None:
                human_temp_min = configRes * 1.1 # Można zmienić na cokolwiek innego jeśli to nie działa dobrze (np. Dodawać jakąś stałą zamiast mnożyć)
                print(f'Configured new threshold temperature to {human_temp_min} Celsius.')

    except ValueError:
        continue