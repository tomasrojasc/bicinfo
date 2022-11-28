import time
import os

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
    speed = gps_parser.speed[2]  # km/h
    return [date, timestamp, latitude, longitude, speed]


def read_acc(mpu_obj):
    values_of_interest = ["GyX", "GyY", "GyZ"]
    mpu_values = mpu_obj.get_values()
    return [mpu_values[i] for i in values_of_interest]
   

def read_values(gps_parser, mpu_obj, bmp):
    """
    This function reads all the important values to save to a SD
    card or to display to the user
    """
    gps_data = read_gps(gps_parser)
    acc_data = read_acc(mpu_obj)
    pressure_data = calculate_altitude_from_pressure(bmp.pressure)
    values = gps_data + acc_data + [pressure_data]
    return values


def write_header(file_path):
    """
    This function writes the header of the csv file
    :param file_path:
    :return:
    """
    header = "datetime,latitude,longitude,speed,GyX,GyY,GyZ,altitude"
    f = open(file_path, 'w')
    f.write(header + "\n")  # python will convert \n to os.linesep
    f.close()
    return


def format_hour(hour):
    """
    This function recieves an hour as a list with numbers corresponfing to [H, M, S]
    :param hour: list with time as 3 numbers
    :return: string with the time formated as H_M_S
    """
    time = [str(i) for i in hour]
    return "_".join(time)


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
    file = path2 + "/paseito.txt"
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
    print(line_to_write)
    # write the line
    with open(file, "a") as f:
        f.write(line_to_write)
    return values
