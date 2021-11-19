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


class Andor():
    def __init__(self):
        self.lib = None
        self.totalCameras = None
        self.cameraHandle = None
        self.serial = None
        self.detector_width = None
        self.detector_height = None
        self.VS_Speeds = None
        self.VS_Speed = None
        self.VS_Index = None
        self.HS_Speeds = None
        self.HS_Speed = None
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
        self.telescope = '60'
        self.readmode = None


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


    def GetNumberVSSpeeds(self):
        VS_Speeds = c_int()
        status = check_call(self.lib.GetNumberVSSpeeds(byref(VS_Speeds)))
        self.VS_Speeds = VS_Speeds.value
        return ERROR_STRING[status], self.VS_Speeds


    def GetVSSpeed(self, VS_Index):
        VS_Speed = c_float()
        status = check_call(self.lib.GetVSSpeed(c_int(VS_Index), byref(VS_Speed)))
        self.VS_Speed = VS_Speed.value
        return ERROR_STRING[status], self.VS_Speed


    def GetNumberHSSpeeds(self, HS_Channel, HS_Type):
        HS_Speeds = c_int()
        status = check_call(self.lib.GetNumberHSSpeeds(c_int(HS_Channel), c_int(HS_Type), byref(HS_Speeds)))
        self.HS_Speeds = HS_Speeds.value
        return ERROR_STRING[status], self.HS_Speeds


    def GetHSSpeed(self, HS_Channel, HS_Type, HS_Index):
        HS_Speed = c_float()
        status = check_call(self.lib.GetHSSpeed(c_int(HS_Channel), c_int(HS_Type), c_int(HS_Index), byref(HS_Speed)))
        self.HS_Speed = HS_Speed.value
        return ERROR_STRING[status], self.HS_Speed

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

    def SetHSSpeed(self, typ, index):
        status = check_call(self.lib.SetHSSpeed(c_int(typ), c_int(index)))
        return ERROR_STRING[status]

    def SetVSSpeed(self, index):
        status = check_call(self.lib.SetVSSpeed(c_int(index)))
        return ERROR_STRING[status]

    def SetPreAmpGain(self, index):
        status = check_call(self.lib.SetPreAmpGain(c_int(index)))
        return ERROR_STRING[status]

    def StartAcquisition(self):
        status = check_call(self.lib.StartAcquisition())
        self.lib.WaitForAcquisition()
        return ERROR_STRING[status]

    def GetAcquiredData(self, imageArray):
        dim = int(self.detector_height * self.detector_width / 1 / 1)
        print(f'dim = {dim}')
        cimageArray = c_int * dim
        print(f'cimage = {cimageArray}')
        cimage = cimageArray()
        print(f'cimage = {cimage}')

        status = check_call(self.lib.GetAcquiredData(pointer(cimage), dim))

        for i in range(len(cimage)):
            imageArray.append(cimage[i])

        self.imageArray = imageArray

        return ERROR_STRING[status]

    def GetAcquiredData16(self, imageArray):
        #dim = np.zeros((self.detector_height*self.detector_width), dtype='uint16')
        dim = int(self.detector_height * self.detector_width / 1 / 1)
        cimageArray = c_int * dim
        cimage = cimageArray()

        status = check_call(self.lib.GetAcquiredData16(pointer(cimage),dim))
        for i in range(len(cimage)):
            imageArray.append(cimage[i])

        print(f'Len of imageArray from GetAcquiredData16: {len(imageArray)}')
        self.imageArray = imageArray

        return ERROR_STRING[status]

    def SaveAsFITS(self, FileTitle, typ):
        status = check_call(self.lib.SaveAsFITS(FileTitle, c_int(typ)))
        return ERROR_STRING[status]

    def saveFits(self, data):
        # array = np.zeros((self.detector_width, self.detector_height), dtype='uint16')
        print(f'Len of Image Array: {len(self.imageArray)}')
        print(type(self.imageArray[10]))
        imdata = np.asarray(self.imageArray, dtype=np.uint16)
        print(type(imdata[10]))

        array = np.reshape(imdata, (self.detector_height, self.detector_width))
        print(type(array[10, 10]))

        # row = 0
        # for i in range(self.detector_width):
        #    for j in range(self.detector_height):
        #        array[i][j] = imdata[row]
        #        row = row + 1

        print(f'Array size: {array.shape}')


        #datetimestr = self.start_time.isoformat()
        #datestr, timestr = datetimestr.split('T')

        date = datetime.today().strftime('%Y%m%d')
        timestamp = f'{date}_{time.strftime("%I")}{time.strftime("%M")}'
        hdul = fits.PrimaryHDU(array, uint=True)
        hdul.scale('int16', bzero=32768)
        hdul.header.set("EXPTIME", float(self.exp_time), "Exposure Time in seconds")
        hdul.header.set("ADCSPEED", self.readmode, "Readout speed in MHz")
        #hdul.header.set("TEMP", self.opt.getParameter("SensorTemperatureReading"), "Detector temp in deg C")
        hdul.header.set("GAIN_SET", 2, "Gain mode")
        hdul.header.set("ADC", 1, "ADC Quality")
        hdul.header.set("MODEL", 22, "Instrument Mode Number")
        hdul.header.set("INTERFC", "USB", "Instrument Interface")
        hdul.header.set("SNSR_NM", "E2V 2048 x 2048 (CCD 42-40)(B)", "Sensor Name")
        hdul.header.set("SER_NO", self.serial, "Serial Number")
        hdul.header.set("TELESCOP", self.telescope, "Telescope ID")
        # hdul.header.set("GAIN", self.gain, "Gain")
        #hdul.header.set("CAM_NAME", "%s Cam" % self.camPrefix.upper(), "Camera Name")
        hdul.header.set("INSTRUME", "SEDM-P60", "Camera Name")
        # hdul.header.set("UTC", start_time.isoformat(), "UT-Shutter Open")
        # hdul.header.set("END_SHUT", datetime.datetime.utcnow().isoformat(), "Shutter Close Time")
        # hdul.header.set("OBSDATE", datestr, "UT Start Date")
        # hdul.header.set("OBSTIME", timestr, "UT Start Time")
        # hdul.header.set("CRPIX1", self.crpix1, "Center X pixel")
        # hdul.header.set("CRPIX2", self.crpix2, "Center Y pixel")
        # hdul.header.set("CDELT1", self.cdelt1, self.cdelt1_comment)
        # hdul.header.set("CDELT2", self.cdelt2, self.cdelt2_comment)
        # hdul.header.set("CTYPE1", self.ctype1)
        # hdul.header.set("CTYPE2", self.ctype2)
        hdul.writeto(f'/home/alex/fits_images/savefits_tests/test_{timestamp}.fits')



    # SHOULD MAKE THOSE SO IT WON'T SHUT DOWN UNTIL DETECTOR TEMP HAS REACHED A SPECIFIED LEVEL
    def ShutDown(self):
        status = check_call(self.lib.ShutDown())
        print(f"{ERROR_STRING[status]}")
        return ERROR_STRING[status]


