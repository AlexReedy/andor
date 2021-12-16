import ctypes
import platform
from ctypes import *
import sys
import os
from astropy.io import fits
from datetime import datetime
import time
import numpy as np

ERROR_CODES = {'DRV_ERROR_CODES': 20001,
'DRV_SUCCESS': 20002,
'DRV_VXDNOTINSTALLED': 20003,
'DRV_ERROR_SCAN': 20004,
'DRV_ERROR_CHECK_SUM': 20005,
'DRV_ERROR_FILELOAD': 20006,
'DRV_UNKNOWN_FUNCTION': 20007,
'DRV_ERROR_VXD_INIT': 20008,
'DRV_ERROR_ADDRESS': 20009,
'DRV_ERROR_PAGELOCK': 20010,
'DRV_ERROR_PAGEUNLOCK': 20011,
'DRV_ERROR_BOARDTEST': 20012,
'DRV_ERROR_ACK': 20013,
'DRV_ERROR_UP_FIFO': 20014,
'DRV_ERROR_PATTERN': 20015,
'DRV_ACQUISITION_ERRORS': 20017,
'DRV_ACQ_BUFFER': 20018,
'DRV_ACQ_DOWNFIFO_FULL': 20019,
'DRV_PROC_UNKONWN_INSTRUCTION': 20020,
'DRV_ILLEGAL_OP_CODE': 20021,
'DRV_KINETIC_TIME_NOT_MET': 20022,
'DRV_ACCUM_TIME_NOT_MET': 20023,
'DRV_NO_NEW_DATA': 20024,
'KERN_MEM_ERROR': 20025,
'DRV_SPOOLERROR': 20026,
'DRV_SPOOLSETUPERROR': 20027,
'DRV_FILESIZELIMITERROR': 20028,
'DRV_ERROR_FILESAVE': 20029,
'DRV_TEMP_CODES': 20033,
'DRV_TEMP_OFF': 20034,
'DRV_TEMP_NOT_STABILIZED': 20035,
'DRV_TEMP_STABILIZED': 20036,
'DRV_TEMP_NOT_REACHED': 20037,
'DRV_TEMP_OUT_RANGE': 20038,
'DRV_TEMP_NOT_SUPPORTED': 20039,
'DRV_TEMP_DRIFT': 20040,
'DRV_GENERAL_ERRORS': 20049,
'DRV_INVALID_AUX': 20050,
'DRV_COF_NOTLOADED': 20051,
'DRV_FPGAPROG': 20052,
'DRV_FLEXERROR': 20053,
'DRV_GPIBERROR': 20054,
'DRV_EEPROMVERSIONERROR': 20055,
'DRV_DATATYPE': 20064,
'DRV_DRIVER_ERRORS': 20065,
'DRV_P1INVALID': 20066,
'DRV_P2INVALID': 20067,
'DRV_P3INVALID': 20068,
'DRV_P4INVALID': 20069,
'DRV_INIERROR': 20070,
'DRV_COFERROR': 20071,
'DRV_ACQUIRING': 20072,
'DRV_IDLE': 20073,
'DRV_TEMPCYCLE': 20074,
'DRV_NOT_INITIALIZED': 20075,
'DRV_P5INVALID': 20076,
'DRV_P6INVALID': 20077,
'DRV_INVALID_MODE': 20078,
'DRV_INVALID_FILTER': 20079,
'DRV_I2CERRORS': 20080,
'DRV_I2CDEVNOTFOUND': 20081,
'DRV_I2CTIMEOUT': 20082,
'DRV_P7INVALID': 20083,
'DRV_P8INVALID': 20084,
'DRV_P9INVALID': 20085,
'DRV_P10INVALID': 20086,
'DRV_P11INVALID': 20087,
'DRV_USBERROR': 20089,
'DRV_IOCERROR': 20090,
'DRV_VRMVERSIONERROR': 20091,
'DRV_GATESTEPERROR': 20092,
'DRV_USB_INTERRUPT_ENDPOINT_ERROR': 20093,
'DRV_RANDOM_TRACK_ERROR': 20094,
'DRV_INVALID_TRIGGER_MODE': 20095,
'DRV_LOAD_FIRMWARE_ERROR': 20096,
'DRV_DIVIDE_BY_ZERO_ERROR': 20097,
'DRV_INVALID_RINGEXPOSURES': 20098,
'DRV_BINNING_ERROR': 20099,
'DRV_INVALID_AMPLIFIER': 20100,
'DRV_INVALID_COUNTCONVERT_MODE': 20101,
'DRV_USB_INTERRUPT_ENDPOINT_TIMEOUT': 20102,
'DRV_ERROR_NOCAMERA': 20990,
'DRV_NOT_SUPPORTED': 20991,
'DRV_NOT_AVAILABLE': 20992,
'DRV_ERROR_MAP': 20115,
'DRV_ERROR_UNMAP': 20116,
'DRV_ERROR_MDL': 20117,
'DRV_ERROR_UNMDL': 20118,
'DRV_ERROR_BUFFSIZE': 20119,
'DRV_ERROR_NOHANDLE': 20121,
'DRV_GATING_NOT_AVAILABLE': 20130,
'DRV_FPGA_VOLTAGE_ERROR': 20131,
'DRV_OW_CMD_FAIL': 20150,
'DRV_OWMEMORY_BAD_ADDR': 20151,
'DRV_OWCMD_NOT_AVAILABLE': 20152,
'DRV_OW_NO_SLAVES': 20153,
'DRV_OW_NOT_INITIALIZED': 20154,
'DRV_OW_ERROR_SLAVE_NUM': 20155,
'DRV_MSTIMINGS_ERROR': 20156,
'DRV_OA_NULL_ERROR': 20173,
'DRV_OA_PARSE_DTD_ERROR': 20174,
'DRV_OA_DTD_VALIDATE_ERROR': 20175,
'DRV_OA_FILE_ACCESS_ERROR': 20176,
'DRV_OA_FILE_DOES_NOT_EXIST': 20177,
'DRV_OA_XML_INVALID_OR_NOT_FOUND_ERROR': 20178,
'DRV_OA_PRESET_FILE_NOT_LOADED': 20179,
'DRV_OA_USER_FILE_NOT_LOADED': 20180,
'DRV_OA_PRESET_AND_USER_FILE_NOT_LOADED': 20181,
'DRV_OA_INVALID_FILE': 20182,
'DRV_OA_FILE_HAS_BEEN_MODIFIED': 20183,
'DRV_OA_BUFFER_FULL': 20184,
'DRV_OA_INVALID_STRING_LENGTH': 20185,
'DRV_OA_INVALID_CHARS_IN_NAME': 20186,
'DRV_OA_INVALID_NAMING': 20187,
'DRV_OA_GET_CAMERA_ERROR': 20188,
'DRV_OA_MODE_ALREADY_EXISTS': 20189,
'DRV_OA_STRINGS_NOT_EQUAL': 20190,
'DRV_OA_NO_USER_DATA': 20191,
'DRV_OA_VALUE_NOT_SUPPORTED': 20192,
'DRV_OA_MODE_DOES_NOT_EXIST': 20193,
'DRV_OA_CAMERA_NOT_SUPPORTED': 20194,
'DRV_OA_FAILED_TO_GET_MODE': 20195,
'DRV_OA_CAMERA_NOT_AVAILABLE': 20196,
'DRV_PROCESSING_FAILED': 20211,
}


ERROR_STRING = dict([(ERROR_CODES[key], key) for key in ERROR_CODES])


def check_call(status):
    if status != ERROR_CODES['DRV_SUCCESS']:
        raise ValueError(f'Driver return {status} ({ERROR_STRING[status]})')
    return status

class AndorCapabilities(Structure):
    _fields_ = [
        ("Size", c_uint),
        ("AcqModes", c_uint),
        ("ReadModes", c_uint),
        ("TriggerModes", c_uint),
        ("CameraType", c_uint),
        ("PixelMode", c_uint),
        ("SetFunctions", c_uint),
        ("GetFunctions", c_uint),
        ("Features", c_uint),
        ("PCICard", c_uint),
        ("EMGainCapability", c_uint),
        ("FTReadModes", c_uint),
    ]


class Andor():
    def __init__(self):
        self.lib = None
        self.totalCameras = None
        self.cameraHandle = None

        self.caps = None

        self.serial = 26265

        self.detector_width = None
        self.detector_height = None

        self.capacity_state = None

        self.adc_channels = None
        self.adc_idx = None

        self.num_amps = None

        self.num_preamp_gains = None
        self.pre_amp_gain = None

        self.num_vss = None
        self.vs_speed = None
        self.vs_index = None

        self.num_hss = None
        self.hs_speed = None
        self.hs_index = None

        self.current_temp = None
        self.mintemp = None
        self.maxtemp = None

        self.hbin = 1
        self.vbin = 1
        self.hstart = 1
        self.hend = None
        self.vstart = 1
        self.vend = None

        self.readmode = None
        self.acquisitionmode = None
        self.exp_time = None

        self.readout_time = None

        self.telescope = '60'
        self.imageArray = None


    def loadLibrary(self):
        if platform.system() == "Linux":
            pathToLib = "/usr/local/lib/libandor.so"
            self.lib = cdll.LoadLibrary(pathToLib)
            return platform.platform()
        else:
            quit()

    def GetAvailableCameras(self):
        totalCameras = c_long()
        status = check_call(self.lib.GetAvailableCameras(byref(totalCameras)))
        self.totalCameras = totalCameras.value
        return ERROR_STRING[status], self.totalCameras


    def GetCameraHandle(self, cameraIndex):
        cameraHandle = c_long()
        status = check_call(self.lib.GetCameraHandle(cameraIndex, byref(cameraHandle)))
        self.cameraHandle = cameraHandle.value
        return ERROR_STRING[status], self.cameraHandle


    def SetCurrentCamera(self, cameraHandle):
        status = check_call(self.lib.SetCurrentCamera(c_long(cameraHandle)))
        return ERROR_STRING[status]


    def Initialize(self):
        pathToDir = c_char()
        status = check_call(self.lib.Initialize(pathToDir))
        return ERROR_STRING[status]

    def GetCapabilities(self):
        caps = AndorCapabilities()
        caps.size = sizeof(caps)
        status = check_call(self.lib.GetCapabilities(byref(caps)))
        self.caps = caps
        print()
        return ERROR_STRING[status], self.caps

    def GetCameraSerialNumber(self):
        serial = c_int()
        status = check_call(self.lib.GetCameraSerialNumber(byref(serial)))
        self.serial = serial.value
        return ERROR_STRING[status], self.serial


    def GetDetector(self):
        detector_width = c_int()
        detector_height = c_int()
        status = check_call(self.lib.GetDetector(byref(detector_width), byref(detector_height)))
        self.detector_width = detector_width.value
        self.detector_height = detector_height.value
        return ERROR_STRING[status], self.detector_width, self.detector_height

    def GetNumberADChannels(self):
        adc_channels = c_int()
        status = check_call(self.lib.GetNumberADChannels(byref(adc_channels)))
        self.adc_channels = adc_channels.value
        return ERROR_STRING[status], self.adc_channels

    def GetNumberAmp(self):
        num_amps = c_int()
        status = check_call(self.lib.GetNumberAmp(byref(num_amps)))
        self.num_amps = num_amps.value
        return ERROR_STRING[status], self.num_amps


    def GetNumberPreAmpGains(self):
        num_preamp_gains = c_int()
        status = check_call(self.lib.GetNumberPreAmpGains(byref(num_preamp_gains)))
        self.num_preamp_gains = num_preamp_gains.value
        return ERROR_STRING[status], self.num_preamp_gains

    def GetPreAmpGain(self, pre_amp_gain_index):
        pre_amp_gain = c_float()
        status = check_call(self.lib.GetPreAmpGain(c_int(pre_amp_gain_index), byref(pre_amp_gain)))
        self.pre_amp_gain = pre_amp_gain.value
        return ERROR_STRING[status], self.pre_amp_gain

    def GetNumberVSSpeeds(self):
        num_vss = c_int()
        status = check_call(self.lib.GetNumberVSSpeeds(byref(num_vss)))
        self.VS_Speeds = num_vss.value
        return ERROR_STRING[status], self.VS_Speeds


    def GetVSSpeed(self, vss_index):
        vs_speed = c_float()
        status = check_call(self.lib.GetVSSpeed(c_int(vss_index), byref(vs_speed)))
        self.vs_speed = vs_speed.value
        return ERROR_STRING[status], self.vs_speed


    def GetNumberHSSpeeds(self, adc_channel, output_amp):
        num_hss = c_int()
        status = check_call(self.lib.GetNumberHSSpeeds(c_int(adc_channel), c_int(output_amp), byref(num_hss)))
        self.num_hss = num_hss.value
        return ERROR_STRING[status], self.num_hss


    def GetHSSpeed(self, adc_channel, output_amp, hss_index):
        hs_speed = c_float()
        status = check_call(self.lib.GetHSSpeed(c_int(adc_channel), c_int(output_amp), c_int(hss_index), byref(hs_speed)))
        self.hs_speed = hs_speed.value
        return ERROR_STRING[status], self.hs_speed

    def GetTemperatureRange(self):
        mintemp = c_int()
        maxtemp = c_int()
        status = check_call(self.lib.GetTemperatureRange(byref(mintemp), byref(maxtemp)))
        self.mintemp = mintemp.value
        self.maxtemp = maxtemp.value
        return ERROR_STRING[status], self.mintemp, self.maxtemp

    def GetTemperature(self):
        current_temp = c_int()
        #status = check_call(self.lib.GetTemperatureF(byref(current_temp)))
        status = self.lib.GetTemperature(byref(current_temp))
        self.current_temp = current_temp.value
        return ERROR_STRING[status], self.current_temp

    def GetReadOutTime(self):
        readout_time = c_int()
        status = check_call(self.lib.GetReadOutTime(byref(readout_time)))
        self.readout_time = readout_time.value
        return ERROR_STRING[status], self.readout_time

    def SetTemperature(self, temperature):
        status = check_call(self.lib.SetTemperature(c_int(temperature)))
        return ERROR_STRING[status]

    def CoolerON(self):
        status = check_call(self.lib.CoolerON())
        return ERROR_STRING[status]

    def CoolerOFF(self):
        status = check_call(self.lib.CoolerOFF())
        return ERROR_STRING[status]

    def SetImage(self, hbin, vbin, hstart, hend, vstart, vend):
        status = check_call(self.lib.SetImage(c_int(hbin),
                                              c_int(vbin),
                                              c_int(hstart),
                                              c_int(hend),
                                              c_int(vstart),
                                              c_int(vend)))

        return ERROR_STRING[status]


    def SetHighCapacity(self, state):
        self.capacity_state = state
        status = check_call(self.lib.SetHighCapacity(c_int(state)))
        return ERROR_STRING[status]

    def SetAcquisitionMode(self, mode):
        status = check_call(self.lib.SetAcquisitionMode(c_int(mode)))
        return ERROR_STRING[status]

    def SetReadMode(self, mode):
        self.readmode = mode
        status = check_call(self.lib.SetReadMode(c_int(mode)))
        return ERROR_STRING[status]

    def SetShutter(self, typ, mode, closingtime, openingtime):
        status = check_call(self.lib.SetShutter(c_int(typ), c_int(mode),c_int(closingtime), c_int(openingtime)))
        return ERROR_STRING[status]

    def SetExposureTime(self, time):
        self.exp_time = time
        status = check_call(self.lib.SetExposureTime(c_float(time)))
        return ERROR_STRING[status]

    def SetADChannel(self, channel):
        self.adc_idx = channel
        status = check_call(self.lib.SetADChannel(c_int(channel)))
        return ERROR_STRING[status]

    def SetHSSpeed(self, typ, index):
        self.hs_index = index
        status = check_call(self.lib.SetHSSpeed(c_int(typ), c_int(index)))
        return ERROR_STRING[status]

    def SetVSSpeed(self, index):
        self.vs_index = index
        status = check_call(self.lib.SetVSSpeed(c_int(index)))
        return ERROR_STRING[status]

    def SetPreAmpGain(self, index):
        self.pre_amp_gain_idx = index
        status = check_call(self.lib.SetPreAmpGain(c_int(index)))
        return ERROR_STRING[status]

    def StartAcquisition(self):
        status = check_call(self.lib.StartAcquisition())
        self.lib.WaitForAcquisition()
        return ERROR_STRING[status]

    def GetAcquiredData16(self, imageArray):
        dim = int(self.detector_height * self.detector_width / 1 / 1)

        cimageArray = c_int16 * dim
        cimage = cimageArray()

        status = check_call(self.lib.GetAcquiredData16(pointer(cimage), dim))

        for i in range(len(cimage)):
            imageArray.append(cimage[i])
        self.imageArray = imageArray


        return ERROR_STRING[status]

    def SaveAsTxt(self, path):
        file = open(path, 'w')

        for line in self.imageArray:
            file.write("%g\n" % line)

        file.close()

    def saveFits(self):
        self.imageArray = np.reshape(self.imageArray, (self.detector_height, self.detector_width))

        date = datetime.today().strftime('%Y%m%d')
        timestamp = f'{date}_{time.strftime("%I")}{time.strftime("%M")}'

        hdul = fits.PrimaryHDU(self.imageArray, uint=True)
        hdul.scale('int16', bzero=32768)
        hdul.header.set("EXPTIME", float(self.exp_time), "Exposure Time in seconds")
        hdul.header.set("ADCHANNEL", self.adc_idx, "A-D Channel")
        hdul.header.set("HSSPEED", self.GetHSSpeed(0, 0, self.hs_index)[1], "HS speed in MHz")
        hdul.header.set("VSSPEED", self.GetVSSpeed(self.vs_index)[1], "VS Speed in microseconds")
        hdul.header.set("TEMP", self.GetTemperature()[1], "Detector temp in deg C")
        hdul.header.set("INTERFC", "USB", "Instrument Interface")
        hdul.header.set("SNSR_NM", "E2V 2088 x 2048 (CCD 42-40)(B)", "Sensor Name")
        hdul.header.set("SER_NO", self.serial, "Serial Number")
        hdul.header.set("TELESCOP", self.telescope, "Telescope ID")
        hdul.header.set("GAIN", self.GetPreAmpGain(self.pre_amp_gain_idx)[1], "Gain")
        hdul.header.set("INSTRUME", "SEDM-P60", "Camera Name")
        hdul.writeto(f'/home/alex/fits_images/savefits_tests/andortest_{self.pre_amp_gain_idx}{self.vs_index}'
                     f'{self.hs_index}_{timestamp}.fits')



    # SHOULD MAKE THOSE SO IT WON'T SHUT DOWN UNTIL DETECTOR TEMP HAS REACHED A SPECIFIED LEVEL
    def ShutDown(self):
        status = check_call(self.lib.ShutDown())
        print(f"{ERROR_STRING[status]}")
        return ERROR_STRING[status]


