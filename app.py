##########################################
# MLX90640 Thermal Camera w Raspberry Pi
# -- 2Hz Sampling with Simple Routine
##########################################
#
import time,board
import numpy as np
import matplotlib.pyplot as plt

mlx_shape = (24,32)


plt.ion() # enables interactive plotting
fig,ax = plt.subplots(figsize=(12,7))
therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
cbar = fig.colorbar(therm1) # setup colorbar for temps
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
t_array = []
f = open("test.txt", "r")
while True:
    t1 = time.monotonic()
    try:


        #mlx.getFrame(frame) # read MLX temperatures into frame var
        data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
        therm1.set_data(np.fliplr(data_array)) # flip left to right
        therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
        cbar.on_mappable_changed(therm1) # update colorbar range
        plt.pause(0.001) # required
        #fig.savefig('mlx90640_test_fliplr.png',dpi=300,facecolor='#FCFCFC',bbox_inches='tight') # comment out to speed up
        t_array.append(time.monotonic()-t1)
        print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
    except ValueError:
        continue # if error, just read again