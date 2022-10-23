sea_level_pressure = 101325  # Pa

def bmp_config(bmp):
    bmp.use_case(BMP280_CASE_INDOOR)
    bmp.oversample(BMP280_OS_STANDARD)
    bmp.temp_os = BMP280_TEMP_OS_8
    bmp.press_os = BMP280_PRES_OS_4
    bmp.standby = BMP280_STANDBY_250
    bmp.iir = BMP280_IIR_FILTER_2
    bmp.spi3w = BMP280_SPI3W_ON
    bmp.power_mode = BMP280_POWER_FORCED
    return

def calculate_altitude_from_pressure(pressure):
    try:
        return 50 + 44330 * (1 - (pressure / sea_level_pressure) ** (1/5.255))
    except:
        return -1
