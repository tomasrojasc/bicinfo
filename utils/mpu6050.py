import math


def get_inclination(acx, acy, acz):
    """
    This function takes the acc in the different axes and returns the inclinations pitch, roll, yaw
    :param acx: AcX from accelerometer
    :param acy: AcY from accelerometer
    :param acz: AcZ from accelerometer
    :return: return angles pitch, roll, yaw in percentage
    """
    pitch = round(math.atan2(-acx, math.sqrt(acy ** 2 + acz ** 2)) * 57.3 * 100 / 45)  # +'%'
    roll = round(math.atan2(-acy, math.sqrt(acx ** 2 + acz ** 2)) * 57.3 * 100 / 45)  # +'%'
    yaw = round(math.atan2(-acz, math.sqrt(acx ** 2 + acy ** 2)) * 57.3 * 100 / 45)  # +'%'
    return [pitch, roll, yaw]
