import time
from andorLib import *

def space():
    print("\n")
    time.sleep(1)

andor = Andor()
andor.loadLibrary()

print("[DETECTING OPERATING SYSTEM]")
if platform.system() == 'Linux':
    print(f"  -> OS INFORMATION = {andor.loadLibrary()} ")

connected_cams = andor.GetAvailableCameras()
print(f"[DETERMINING NUMBER OF CONNECTED CAMERAS]")
print(f" -> STATUS = [{connected_cams[0]}]")
print(f" -> CONNECTED CAMERAS = {connected_cams[1]}")

space()

cam_handle = andor.GetCameraHandle(connected_cams[1]-1)
print(f"[DETERMINING CAMERA HANDLE]")
print(f" -> STATUS = [{cam_handle[0]}]")
print(f" -> CAMERA HANDLE = {cam_handle[1]}")

space()

cam_set = andor.SetCurrentCamera(cam_handle[1])
print(f"[SETTING ACTIVE CAMERA TO HANDLE]")
print(f" -> STATUS = [{cam_set}]")

space()

initialize = andor.Initialize()
print(f"[INITIALIZING CAMERA]")
print(f" -> STATUS = [{initialize}]")


space()

serial = andor.GetCameraSerialNumber()
print(f"[DETERMINING CAMERA SERIAL NUMBER]")
print(f" -> STATUS = [{serial[0]}]")
print(f" -> CAMERA SERIAL NUMBER = {serial[1]}")

space()

numVSSpeeds = andor.GetNumberVSSpeeds()
print(f"[DETERMINING NUMBER OF AVAILABLE VERTICAL SHIFT SPEEDS]")
print(f" -> STATUS = [{numVSSpeeds[0]}]")
print(f" -> AVAILABLE VERTICAL SHIFT SPEEDS = {numVSSpeeds[1]}")

space()

print(f"[DETERMINING VALUES FOR VERTICAL SHIFT SPEEDS]")
for idx in range(len(numVSSpeeds)):
    vs_speed = andor.GetVSSpeed(idx)
    print(f"  -> FOR VSS INDEX [{idx}]")
    print(f"   -> STATUS = [{vs_speed[0]}]")
    print(f"   -> VERTICAL SHIFT SPEED VALUE = [{vs_speed[1]}]")

space()

numHSSpeeds = andor.GetNumberHSSpeeds(0, 0)
print(f"[DETERMINING NUMBER OF AVAILABLE HORIZONTAL SHIFT SPEEDS]")
print(f" -> STATUS = [{numHSSpeeds[0]}]")
print(f" -> AVAILABLE HORIZONTAL SHIFT SPEEDS = {numHSSpeeds[1]}")

space()

print(f"[DETERMINING VALUES FOR HORIZONTAL SHIFT SPEEDS]")
print(f"!! NOTE !!")
print(f" AD CHANNEL = 0 and OUTPUT AMPLIFICATION = 0 (FOR EMM/CONVENTIONAL) ARE CURRENTLY HARDCODED")
for idx in range(len(numHSSpeeds)):
    hs_speed = andor.GetHSSpeed(0, 0, idx)
    print(f"  -> FOR HSS INDEX [{idx}]")
    print(f"   -> STATUS = [{hs_speed[0]}]")
    print(f"   -> VERTICAL SHIFT SPEED VALUE = [{hs_speed[1]}]")

space()

temp_range = andor.GetTemperatureRange()
print(f"[DETERMINING VALID TEMPERATURE RANGE]")
print(f" -> STATUS = [{temp_range[0]}]")
print(f" -> TEMP RANGE = [{temp_range[1]},{temp_range[2]}]")

temp = andor.GetTemperatureF()
print(f" -> STATUS = [{temp[0]}]")
print(f' -> TEMP: {temp[1]}')













































