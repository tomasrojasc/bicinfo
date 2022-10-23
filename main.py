"""
Circuit connections

SD card:
module side -> ESP32 side
GND -> GND
VCC -> 5V
MISO -> Pin 13
MOSI -> Pin 12
SCK -> Pin 14
CS -> Pin 27

GPS
module side -> ESP32 side
GND -> GND
TX -> Pin 16
RX -> Pin 17
VCC -> 3V3

BMP280
module side -> ESP32 side
VIN -> 3V3
GND -> GND
SCL -> Pin 5
SDA -> Pin 4
"""
"""
from machine import SoftI2C, Pin, SoftSPI, UART, SPI, SDCard
import utime
from utils.micropyGPS import MicropyGPS
from drivers.bmp280 import *
from utils.bmp280 import calculate_altitude_from_pressure
from drivers.mpu6050 import accel
from utils.writeSD import read_values

# I2C bus
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

# MPU6050 preliminar statements
mpu = accel(i2c)

# BMP280 preliminar statements
bmp = BMP280(i2c)

# GPS preliminar statements
gpsModule = UART(2, baudrate=9600)
gps_parser = MicropyGPS(location_formatting="dd")



# SD card preliminar statements
#spi_sd = SoftSPI(-1, miso=Pin(13), mosi=Pin(12), sck=Pin(14))
#sd = SDCard(spi_sd, Pin(27))
while True:
    line = gpsModule.readline()
    utime.sleep(0.1)
    gps_parser.update_from_line(line)
    print(read_values(gps_parser, mpu, bmp))
   # print(mpu.get_values()["GyZ"])
"""
import machine
import os
from machine import SoftSPI, Pin
from sdcard import SDCard

spi_sd = SoftSPI(-1, miso=Pin(13), mosi=Pin(12), sck=Pin(14))
sd = SDCard(spi_sd, Pin(27))
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")