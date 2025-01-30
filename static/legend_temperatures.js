document.addEventListener('DOMContentLoaded', () => {
    const legendDiv = document.getElementById('legend');

    const startTemp = 36.3;
    const endTemp = 37.9;
    const step = 0.1;

    for (let temp = startTemp; temp <= endTemp; temp += step) {
        const tick = document.createElement('div');
        tick.classList.add('tick');

        if ((temp * 10) % 2 === 0) {
            // Create a label for every 0.2 increment
            const label = document.createElement('div');
            label.classList.add('label');
            label.innerText = temp.toFixed(1);
            tick.appendChild(label);
        } else {
            tick.classList.add('small');
        }

        legendDiv.appendChild(tick);
    }
});