"""
values_now = []
while True:
    
    t0 = read_timestamp()
    tf = t0+T
    while read_timestamp()< tf:
        values_now.append(values_read())
        sleep(t)
    average_values_now()
    show_values_now()
    write_values_now()
    values_now = []
     """   
      
from utils.bmp280 import calculate_altitude_from_pressure

def get_latitude(latitude_from_gps):
    latitude, sign = latitude_from_gps
    if sign=="S":
        latitude *= -1
    return latitude
 

def get_longitude(longitude_from_gps):
    longitude, sign = longitude_from_gps
    if sign=="W":
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
    return [date, timestamp, latitude, longitude]

def read_acc(mpu_obj):
    return list(mpu_obj.get_values().values())
    
   

def read_values(gps_parser, mpu_obj, bmp):
    """
    This function reads all the mportant values to save to a SD 
    card or to display to the user
    """
    gps_data = read_gps(gps_parser)
    acc_data = read_acc(mpu_obj)
    pressure_data = calculate_altitude_from_pressure(bmp.pressure)
    values = gps_data + acc_data + [pressure_data]
    return values