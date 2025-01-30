// js script for transporting frames to the server

const video = document.getElementById('video');
const detectDiv = document.getElementById('infoDiv1');
const temperatureDiv = document.getElementById('infoDiv2');
const socket = io();

socket.on('connect', () => {
    console.log('Connected to server');
    socket.emit('request_video');
});

socket.on('frame_image', (frame) => {
    video.src = 'data:image/jpeg;base64,' + frame.image;
});

socket.on('detection', (data) => {
    detectDiv.innerText = data.data;
});

socket.on('temperature', (data) => {
    temperatureDiv.innerHTML = '';
    const colors = ['green', 'red', 'blue']; 
    const temperatures = data.data.split(', ');
    const isBackground = data.isBackground;

    temperatures.forEach((temp, index) => {
        const span = document.createElement('span');
        span.textContent = temp.trim(); 

        // set font color based on index
        if (isBackground) {
            span.style.color = 'black';
        }
        else if (index < colors.length) {
            span.style.color = colors[index];
        } else {
            span.style.color = 'green';  
        }

        temperatureDiv.appendChild(span);
        temperatureDiv.appendChild(document.createTextNode(',  ')); 
    });

    if (temperatureDiv.lastChild) {
        temperatureDiv.removeChild(temperatureDiv.lastChild);
    }
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});
