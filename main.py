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
import time
from machine import SoftI2C, Pin, SoftSPI, UART
import utime
from utils.micropyGPS import MicropyGPS
from drivers.bmp280 import *
from utils.bmp280 import calculate_altitude_from_pressure
from drivers.mpu6050 import accel
from utils.writeSD import read_values, create_file_sd_card, write_data_to_file
import os
from drivers.sdcard import SDCard


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
spi_sd = SoftSPI(-1, miso=Pin(13), mosi=Pin(12), sck=Pin(14))
sd = SDCard(spi_sd, Pin(27))
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

# I/O
green_led = Pin(23, Pin.OUT)
red_led = Pin(22, Pin.OUT)
start_end_trip_button = Pin(2, Pin.IN)

green_led.value(0)
red_led.value(0)

start_trip_state = 0

while True:
    time.sleep(0.2)
    if start_end_trip_button.value() == 1:
        print("trip started")
        start_trip_state = 1
        file = create_file_sd_card(gpsModule, gps_parser, mpu, bmp, green_led, red_led)

    while start_trip_state == 1:
        time.sleep(0.2)
        write_data_to_file(file, gpsModule, gps_parser, mpu, bmp)
        if start_end_trip_button.value() == 1:
            print("trip finished")
            start_trip_state = 0
            green_led.value(0)
            red_led.value(0)

# print(mpu.get_values()["GyZ"])


