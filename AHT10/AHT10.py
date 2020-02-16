import time
import math
import machine

WATER_VAPOR         = 17.62
BAROMETRIC_PRESSURE = 243.5

eSensorCalibrateCmd = [0xE1, 0x08, 0x00] # 0b11100001
eSensorNormalCmd    = [0xA8, 0x00, 0x00] # 0b10101000
eSensorMeasureCmd   = [0xAC, 0x33, 0x00] # 0b10101100
eSensorResetCmd     = 0xBA
GetRHumidityCmd     = True
GetTempCmd          = False
AHT10_address       = 0x38
class AHT10():

    def __init__(self, i2c):
        self.i2c = i2c
        self.i2c.start()
        self.i2c.writeto(AHT10_address, bytes(eSensorCalibrateCmd))
        self.i2c.stop()
        #time.sleep_ms(500)

        if self.i2c.readfrom(AHT10_address, 1)[0] & 0x68 == 0x08: #read status
            print('AHT10 calibrated')
        else:
            print('Error while AHT10 calibration')

    def readSensor(self, GetDataCmd):
        temp = []
        self.i2c.start()
        self.i2c.writeto(AHT10_address, bytes(eSensorMeasureCmd))
        self.i2c.stop()
        time.sleep_ms(75)
        dataFromSensor  = self.i2c.readfrom(AHT10_address, 6)
        if GetDataCmd:
            return ((dataFromSensor[1] << 16) | (dataFromSensor[2] << 8) | dataFromSensor[3]) >> 4
        else:
            return ((dataFromSensor[3] & 0x0F) << 16) | (dataFromSensor[4] << 8) | dataFromSensor[5]

    def GetHumidity(self):
        value = self.readSensor(GetRHumidityCmd)
        if value == 0:
            return 0        #Some unrealistic value
        return value * 100 / 1048576

    def GetTemperature(self):
        value = self.readSensor(GetTempCmd)
        return ((200 * value) / 1048576) - 50

    def GetDewPoint(self):
        humidity = self.GetHumidity()
        temperature = self.GetTemperature()
        #Calculate the intermediate value 'gamma'
        gamma = math.log(humidity / 100) + WATER_VAPOR * temperature / (BAROMETRIC_PRESSURE + temperature)
        #Calculate dew point in Celsius
        dewPoint = BAROMETRIC_PRESSURE * gamma / (WATER_VAPOR - gamma)
        return dewPoint

    def Reset(self):
        self.i2c.start()
        self.i2c.writeto(AHT10_address, bytes(eSensorResetCmd))
        self.i2c.stop()
        time.sleep_ms(20)
