import matplotlib.pyplot as plt
from andorLib import *
import time

def space():
    print("\n")
    time.sleep(1)

fig, ax = plt.subplots(nrows=1, ncols=1)
ax.set_ylabel('Detector Temperature [Celsius]')
ax.set_xlabel('Time [Sec]')
ax.set_ylim(ymax=35, ymin=-35)


print('-------------------------------------------------------------------------------')
print('                         ANDOR IKON L-936 TESTING')
print('-------------------------------------------------------------------------------')

run_command = input('Begin Initialization? [y/n]: ')
if run_command == 'y':
    space()

    andor = Andor()
    andor.loadLibrary()

    print("[DETECTING OPERATING SYSTEM]")
    if platform.system() == 'Linux':
        print(f"  -> OS INFORMATION = {andor.loadLibrary()} ")

    space()

    print(f"[DETERMINING NUMBER OF CONNECTED CAMERAS]")
    connected_cams = andor.GetAvailableCameras()
    print(f" -> STATUS = [{connected_cams[0]}]")
    print(f" -> CONNECTED CAMERAS = {connected_cams[1]}")

    space()

    print(f"[DETERMINING CAMERA HANDLE]")
    cam_handle = andor.GetCameraHandle(connected_cams[1] - 1)
    print(f" -> STATUS = [{cam_handle[0]}]")
    print(f" -> CAMERA HANDLE = {cam_handle[1]}")

    space()

    print(f"[SETTING ACTIVE CAMERA TO HANDLE]")
    cam_set = andor.SetCurrentCamera(cam_handle[1])
    print(f" -> STATUS = [{cam_set}]")

    space()

    initialize_command = input('Initialize Camera? [y/n]: ')

    space()

    if initialize_command == 'y':
        print(f"[INITIALIZING CAMERA]")
        initialize = andor.Initialize()
        print(f" -> STATUS = [{initialize}]")

        space()

        temp_set_point = -30

        print(f'[SETTING DETECTOR COOLING TEMPERATURE]')
        set_t = andor.SetTemperature(temp_set_point)
        print(f' -> STATUS = {set_t[0]}')
        print(f' -> TEMP SET POINT = {temp_set_point}')

        space()

        coolerOn_prompt = input('Turn Cooler On? [y/n]: ')

        space()

        if coolerOn_prompt == 'y':
            andor.CoolerON()

            get_temp = andor.GetTemperature()
            temp = get_temp[1]
            lock = get_temp[0]


            cooldow_counter = 0

            print(f'[COOLING DETECTOR TO {temp_set_point} C]')
            while lock != 'DRV_TEMP_STABILIZED':
                cooldow_counter = cooldow_counter + 1
                print(f' -> Interval: {cooldow_counter}')
                print(f' -> CURRENT TEMP: {temp} C')
                print(f' -> COOLING STATUS: {lock}')
                ax.errorbar(cooldow_counter, temp, linestyle='none', marker='s', ms=2, color='black')
                ax.axhline(temp_set_point, linestyle='--', linewidth=1, color='black')
                plt.pause(1)
                #time.sleep(1)
                get_temp = andor.GetTemperature()
                temp = get_temp[1]
                lock = get_temp[0]


            '''
            while lock != 'DRV_TEMP_STABILIZED':
                print(f' -> CURRENT TEMP: {temp} C')
                print(f' -> COOLING STATUS: {lock}')
                time.sleep(1)
                get_temp = andor.GetTemperatureF()
                lock = get_temp[0]
            '''


            hold_command = input('Turn Cooler Off? [y/n]: ')



            while hold_command == 'n':
                print(f' -> CURRENT TEMP: {temp} C')
                print(f' -> COOLING STATUS: {lock}')
                time.sleep(10)
                get_temp = andor.GetTemperature()
                temp = get_temp[1]
                lock = get_temp[0]
                hold_command = input('Turn Cooler Off? [y/n]: ')

            get_temp = andor.GetTemperature()
            temp = get_temp[1]
            lock = get_temp[0]

            print('[WAITING FOR DETECTOR TEMP TO REACH < -10 C]')
            andor.CoolerOFF()
            coolup_counter = 0

            while temp <= -20:
                coolup_counter = coolup_counter + 1
                print(f'Interval: {coolup_counter}')
                print(f' -> CURRENT TEMP: {temp} C')
                print(f' -> COOLING STATUS: {lock}')
                time.sleep(1)
                get_temp = andor.GetTemperature()
                temp = get_temp[1]
                lock = get_temp[0]
            print(' -> Detector Warmed to -20 C')
            print('[SHUTTING DOWN CAMERA]')
            andor.ShutDown()
        if coolerOn_prompt == 'n':
            print('Shutting Down')
            andor.ShutDown()
            exit()

    if initialize_command == 'n':
        print('Shutting Down')
        andor.ShutDown()
        exit()

if run_command == 'n':
    print('Shutting Down')
    exit()

plt.show(block=False)
