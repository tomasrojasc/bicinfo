import time
from machine import SoftI2C, Pin, SoftSPI, UART
from utils.micropyGPS import MicropyGPS
from drivers.bmp280 import *
from drivers.mpu6050 import accel
from utils.lcd import write_lcd, display_menu
from drivers.i2c_lcd import I2cLcd
from utils.writeSD import create_file_sd_card, write_data_to_file
import os
from drivers.sdcard import SDCard
from utils.mpu6050 import get_inclination

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

# LCD
lcd = I2cLcd(i2c, 0x27, 2, 16)

# I/O
green_led = Pin(23, Pin.OUT)
red_led = Pin(22, Pin.OUT)
start_end_trip_button = Pin(2, Pin.IN)
shift_menu_button = Pin(18, Pin.IN)

green_led.value(0)
red_led.value(0)

start_trip_state = 0
shift_menu_state = 0  # esto puede tomar valores 0, 1 y 2 para
                      # tener velocidad, inclinación y altitud, respectivamente
                      # por defecto comenzamos con la velocidad

while True:
    time.sleep(0.2)
    if start_end_trip_button.value() == 1:
        write_lcd(lcd, "Empezando viaje")
        start_trip_state = 1
        file = create_file_sd_card(gpsModule, gps_parser, mpu, bmp, green_led, red_led)

    while start_trip_state == 1:
        time.sleep(0.2)
        values = write_data_to_file(file, gpsModule, gps_parser, mpu, bmp)

        if shift_menu_button.value() == 1:
            shift_menu_state += 1
            shift_menu_state %= 3

        display_menu(lcd, shift_menu_state, values)

        print(values, "holi")
        if start_end_trip_button.value() == 1:
            write_lcd(lcd, "viaje finalizado")
            time.sleep(2)
            write_lcd(lcd, "")
            start_trip_state = 0
            green_led.value(0)
            red_led.value(0)


