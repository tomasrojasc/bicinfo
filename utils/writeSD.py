import time
import os

from utils.mpu6050 import get_inclination
from utils.bmp280 import calculate_altitude_from_pressure


def get_latitude(latitude_from_gps):
    latitude, sign = latitude_from_gps
    if sign=="S":
        latitude *= -1
    return latitude
 

def get_longitude(longitude_from_gps):
    longitude, sign = longitude_from_gps
    if sign == "W":
        longitude *= -1
    return longitude


def read_gps(gps_parser):
    """This function gives a list of important
    GPS data, it returns a list with the following content
    
    - date: done
    - time: done
    - longitude in decimal format: done
    - latitude in decimal format: done
    - altitude
    - speed    
    """
    date = gps_parser.date_string()
    timestamp = gps_parser.timestamp
    latitude = get_latitude(gps_parser.latitude)
    longitude = get_longitude(gps_parser.longitude)
    altitude = gps_parser.altitude
    speed = round(gps_parser.speed[2])  # km/h
    return [date, timestamp, latitude, longitude, speed, altitude]


def read_acc(mpu_obj):
    values_of_interest = ["AcX", "AcY", "AcZ"]
    mpu_values = mpu_obj.get_values()
    AcXYZ = [mpu_values[i] for i in values_of_interest]
    return [round(get_inclination(*AcXYZ)[2])]

def read_values(gps_parser, mpu_obj, bmp):
    """
    This function reads all the important values to save to a SD
    card or to display to the user
    """
    gps_data = read_gps(gps_parser)[:-1]
    acc_data = read_acc(mpu_obj)
    pressure_data = calculate_altitude_from_pressure(bmp.pressure)
    pressure_data = [read_gps(gps_parser)[-1]]
    values = gps_data + acc_data + [pressure_data]
    return values


def write_header(file_path):
    """
    This function writes the header of the gpx file
    :param file_path:
    :return:
    """
    header = "datetime,latitude,longitude,speed,pitch,roll,yaw,altitude"
    header = """<?xml version="1.0" encoding="UTF-8"?>

    <gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="BicInfo">
        <metadata>
            <link href="https://github.com/tomasrojasc/bicinfo">
                <text>BicInfo</text>
            </link>
            <time>2022-12-03T17:39:00-03:00</time>
        </metadata>
        <trk>
            <name>Tu ruta</name>
        <trkseg>"""
    f = open(file_path, 'w')
    f.write(header + "\n")  # python will convert \n to os.linesep
    f.close()
    return

def end_gpx_file(file_path):
    ending = """        </trkseg>
        </trk>
    </gpx>
    """
    f = open(file_path, 'a')
    f.write(ending + "\n")  # python will convert \n to os.linesep
    f.close()
    return
def format_hour(hour):
    """
    This function recieves an hour as a list with numbers corresponfing to [H, M, S]
    :param hour: list with time as 3 numbers
    :return: string with the time formated as H_M_S
    """
    time_ = [str(i) for i in hour]
    return "_".join(time_)


def create_file_sd_card(gpsModule, gps_parser, mpu_obj, bmp, green_led, red_led):
    """
    This function creates the folder and the file to save data
    :param gps_parser:
    :param mpu_obj:
    :param bmp:
    :param green_led:
    :param red_led:
    :return: file path to where to start writing the trip
    """

    while read_values(gps_parser, mpu_obj, bmp)[0] == "00/00/00":
        line = gpsModule.readline()
        time.sleep(0.1)
        print(gps_parser.satellites_in_view)
        gps_parser.update_from_line(line)
        red_led.value(1)
        print(read_values(gps_parser, mpu_obj, bmp))
        time.sleep(0.1)

    date, hour = read_values(gps_parser, mpu_obj, bmp)[:2]
    date = date.replace("/", "-")
    red_led.value(0)
    green_led.value(1)
    path1 = "sd/" + date
    path2 = path1 + "/" + format_hour(hour)
    try:
        os.mkdir(path1)
    except:
        pass
    os.mkdir(path2)
    file = path2 + "/paseito.gpx"
    fp = open(file, "x")
    fp.close()
    write_header(file)
    return file


def formate_datetime(date, time_):
    """
    This function recieves the date as mm/dd/yy and the time as a list [H, M, S]
    and converts it to a string %Y-%m-%d %H:%M:%S
    :param date: date as mm/dd/yy
    :param time_: time as a list [H, M, S]
    :return: datetime as string %Y-%m-%d %H:%M:%S
    """
    month, day, year = date.split("/")
    date_ = "-".join([year, month, day])
    time_local_ = ":".join([str(i) for i in time_])
    datetime = " ".join([date_, time_local_])
    return datetime


def create_line_to_write(gps_parser, mpu, bmp):
    line = read_values(gps_parser, mpu, bmp)
    date_, time_ = line[:2]
    line = [formate_datetime(date_, time_)] + line[2:]
    line_ = ",".join([str(i) for i in line])
    line_ += "\n"
    return line_, line


def write_data_to_file(file, gpsModule, gps_parser, mpu, bmp):
    """
    This function takes a file and starts writing information to it
    :param file:
    :param gpsModule:
    :param gps_parser:
    :param mpu:
    :param bmp:
    :param green_led:
    :param red_led:
    :return:
    """

    # first we update the gps info:
    line_gps = gpsModule.readline()
    time.sleep(0.1)
    gps_parser.update_from_line(line_gps)
    # obtain the line
    line_to_write, values = create_line_to_write(gps_parser, mpu, bmp)
    date = line_to_write.split(",")[0]
    print(line_to_write)
    print(values)
    if "00/00/00" in date:
        return None, None

    if float(values[1]) == 0:
        return None, None

    print(line_to_write)
    # write the line

    return values, line_to_write

def get_minute_from_values(values):
    datetime = values[0]
    date, time_ = datetime.split(" ")
    hr, min, sec = time_.split(":")
    return min



def get_average(buffer):
    datetime = buffer[0][0]
    buffer_to_avg = [[float(j) for j in i[1:]] for i in buffer]
    n = len(buffer_to_avg[0])
    avg = []
    for i in range(n):
        current_avg = []
        for list_of_values in buffer_to_avg:
            current_avg.append(list_of_values[i])
        avg.append(sum(current_avg)/len(current_avg))
    averaged_values_to_write = [datetime] + avg
    return averaged_values_to_write



def write_gpx_point(averaged_values_to_write, file_path):
    datetime, lat, lon, speed, yaw, altitude = averaged_values_to_write
    print(f"\n{altitude}\n")
    date, time_ = datetime.split(" ")
    line = f"""      <trkpt lat="{lat}" lon="{lon}">
                <desc>"inclinación {yaw}%, velocidad calculada: {speed}km/h"</desc>
                <speed>{speed}</speed>
                <ele>{altitude[0]}</ele>
                <time>{date}T{time_}-03:00</time>
            </trkpt>"""
    f = open(file_path, 'a')
    f.write(line + "\n")
    f.close()
    return
