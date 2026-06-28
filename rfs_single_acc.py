import time
import board
import adafruit_mpu6050
import busio
import digitalio
import adafruit_bmp280

#Device setup
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
imu = adafruit_mpu6050.MPU6050(i2c)

#Calibration button
switch = digitalio.DigitalInOut(board.D10)
switch.switch_to_input(pull=digitalio.Pull.UP)

#Calibrations
acceleration_calibration = [0,0,0]
gyro_calibration = [0,0,0]
altitude_calibration = 0

BUTTON_HOLD_TIME = 1
started_holding = 0


def get_acceleration(position):
    return (imu.acceleration[position]+acceleration_calibration[position])
def get_gyro(position):
    return (imu.gyro[position]+acceleration_calibration[position])

def calibrate():    
    acceleration_calibration.append(0-imu.acceleration[0])
    acceleration_calibration.append(0-imu.acceleration[1])
    acceleration_calibration.append(9.82-imu.acceleration[2])

    for i in range(3):
        gyro_calibration.append(0-imu.gyro[i])
    
    print(f"Acceleration offset {acceleration_calibration}, Gyro offset: {gyro_calibration}")




while True:
    time.sleep(1)
    #Calibrate
    if not switch.value and time.time()-started_holding > BUTTON_HOLD_TIME:
        print("calibrating")

        acceleration_calibration = []
        gyro_calibration = []
        altitude_calibration = 0-bmp.altitude
        calibrate()
        
        started_holding = time.time()

    else:
        #Barometer stuff
        print(f"Altitude: {bmp.altitude+altitude_calibration}")
        #Acceleration/gyro
        print(f"Acceleration x: {get_acceleration(0)} m/s^2, Acceleration y:{get_acceleration(1)} m/s^2, Acceleration z: {get_acceleration(2)} m/s^2")
        print(f"Gyro x: {get_gyro(0)} rad/s, Gyro y:{get_gyro(1)} rad/s, Gyro z: {get_gyro(2)} rad/s \n")

#X = Left/Right Y=Forward/Back Z = Up/Down
#Gyro 1 = Pitch 2 = Roll 3 = Yaw
