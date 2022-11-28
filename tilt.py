import math

#Obtiene los parametros de acceleracion
Acx = mpu.get_values()['AcX']
AcY = mpu.get_values()['AcY']
AcZ = mpu.get_values()['AcZ']
#obtiene el amgulo pitch en % de inclinacion (45° = 100%)
pitch = round(math.atan2(-Acx,math.sqrt(AcY**2 + AcZ**2))*57.3*100/45) # +'%'
