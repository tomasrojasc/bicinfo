
def write_lcd(lcd_i2c, string_to_display):
    lcd_i2c.clear()
    lcd_i2c.putstr(string_to_display)
    return

# header del csv: "datetime,latitude,longitude,speed,GyX,GyY,GyZ,altitude"
"datetime,latitude,longitude,speed,pitch,roll,yaw,altitude"

def display_menu(lcd_i2c, current_menu_value, values, inclination_0):
    pitch_0, roll_0, yaw_0 = inclination_0
    speed = values[3]
    pitch, roll, yaw = values[4:7]   # esto debe ser modificado para mostrar la inclinación real
    altitude = values[7]

    pitch -= pitch_0
    roll -= roll_0
    yaw -= yaw_0

    if current_menu_value == 0:
        msg = f"Tu velocidad es:\n {speed}km/h"
    elif current_menu_value == 1:
        msg = f"La inclinación es:\n {pitch}%, {roll}%, {yaw}%"
    elif current_menu_value == 2:
        msg = f"Tu altitud es:\n {altitude}msnm"
    write_lcd(lcd_i2c, msg)
