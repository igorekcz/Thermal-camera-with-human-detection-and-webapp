##########################################
# MLX90640 Thermal Camera w Raspberry Pi
# -- 8-16Hz Sampling with Simple Routine
##########################################
#
#kod działa z szybkościa zależną od sprzętu(czyt. od własnego komputera), przydało by się jednak go ograniczyć poprzez kod
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
#rozmiar jednej ramki z kamery to 24X32
mlx_shape = (24,32)

#tutaj zaczyna się tworzenie plota
plt.ion() # enables interactive plotting
fig,ax = plt.subplots(figsize=(12,7)) #rozmiar okna, jak komuś działa za wolno to można zmienić na mniejszy, albo na większy jak kto woli
therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
cbar = fig.colorbar(therm1) # setup colorbar for temps
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label


frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
t_array = []
file = sys.argv[1]
frames2 = np.loadtxt(file)
frame_size = frames2.shape#pobiera wielkość całego pliku txt, dzięki temu otrzymujemy liczbę wierszy danego pliku(liczba kolumn to stałe 32)

x = 0
i = 0
while (x<frame_size[0]):
    #funkcja czasu, jak działa? nie wiem
    t1 = time.monotonic()
    try:

        frame = frames2[x:x + 24, 0:32]#ramka to 24x32 więc bierzemy 24 linijki i je wyświetlamy
        data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
        #wyświetlanie wskaźnika koloru
        therm1.set_data(np.fliplr(data_array)) # flip left to right
        therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
        #funkcja poniżej nie działa bo nie ma już takiej metody, może trzeba naprawić
        #cbar.on_mappable_changed(therm1) # update colorbar range
        plt.pause(0.001) # required
        t_array.append(time.monotonic()-t1)
        x = x + 24
        i += 1
        #wyświetla fps, chyba poprawnie, dzięki temu widać jak szybko i czy działa
        #print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
    except ValueError:
        continue # if error, just read again
plt.close("all")