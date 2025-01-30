from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index_test.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('frame_image')
def handle_video_frame(data):
    emit('frame_image', data, broadcast=True)

@socketio.on('detection_info')
def handle_detection_info(data):
    socketio.emit('detection', {'data': data['detection']})

@socketio.on('temperature_info')
def handle_temperature_info(data):
    socketio.emit('temperature', {'data': data['temperature'], 'isBackground': data['isBackground']})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

