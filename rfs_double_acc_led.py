import time
import board
import adafruit_mpu6050
import busio
import digitalio
import adafruit_bmp280
import pwmio

#RGB Light
red = pwmio.PWMOut(board.D11)
green = pwmio.PWMOut(board.D12)
blue = pwmio.PWMOut(board.D13)

RED         = (65535,     0,     0)
ORANGE      = (65535, 32768,     0)
YELLOW      = (65535, 65535,     0)
LIME        = (32768, 65535,     0)
GREEN       = (    0, 65535,     0)
TURQUOISE   = (    0, 65535, 32768)
CYAN        = (    0, 65535, 65535)
SKY_BLUE    = (15000, 45000, 65535)
BLUE        = (    0,     0, 65535)
PURPLE      = (32768,     0, 65535)
MAGENTA     = (65535,     0, 65535)
PINK        = (65535, 15000, 35000)

def set_color(color):
    red.duty_cycle = color[0]
    green.duty_cycle = color[1]
    blue.duty_cycle = color[2]

#Device setup
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
accelerometer1 = adafruit_mpu6050.MPU6050(i2c)
accelerometer2 = adafruit_mpu6050.MPU6050(i2c,address=0x68)
set_color(BLUE)
time.sleep(3)

#Calibration button
switch = digitalio.DigitalInOut(board.D10)
switch.switch_to_input(pull=digitalio.Pull.UP)


#Calibrations
acceleration_calibration_1 = [0,0,0]
acceleration_calibration_2 = [0,0,0]
gyro_calibration_1 = [0,0,0]
gyro_calibration_2 = [0,0,0]
altitude_calibration = 0

BUTTON_HOLD_TIME = 1
started_holding = 0


def get_averaged_acceleration(position):
    return ((accelerometer1.acceleration[position]+acceleration_calibration_1[position])+(accelerometer2.acceleration[position]+acceleration_calibration_2[position]))/2

def get_averaged_gyro(position):
    return ((accelerometer1.gyro[position]+gyro_calibration_1[position])+(accelerometer2.gyro[position]+gyro_calibration_2[position]))/2

def calibrate(imu,acceleration_calibration,gyro_calibration):
    acceleration_calibration.append(0-imu.acceleration[0])
    acceleration_calibration.append(0-imu.acceleration[1])
    acceleration_calibration.append(9.82-imu.acceleration[2])

    for i in range(3):
        gyro_calibration.append(0-imu.gyro[i])

    print(acceleration_calibration,gyro_calibration)



set_color(YELLOW)
while True:

    time.sleep(1)

    #Calibrate
    if not switch.value and time.time()-started_holding > BUTTON_HOLD_TIME:
        print("calibrating")
        set_color(PURPLE)
        time.sleep(2)

        acceleration_calibration_1 = []
        acceleration_calibration_2 = []
        gyro_calibration_1 = []
        gyro_calibration_2 = []

        calibrate(accelerometer1,acceleration_calibration_1,gyro_calibration_1)
        calibrate(accelerometer2,acceleration_calibration_2,gyro_calibration_2)

        altitude_calibration = 0-bmp.altitude

        started_holding = time.time()
        set_color(GREEN)

    else:
        #Barometer stuff
        print(f"Altitude: {bmp.altitude+altitude_calibration}")
        #Acceleration/gyro
        print(f"Acceleration x: {get_averaged_acceleration(0)} m/s^2, Acceleration y:{get_averaged_acceleration(1)} m/s^2, Acceleration z: {get_averaged_acceleration(2)} m/s^2")
        print(f"Gyro x: {get_averaged_gyro(0)} rad/s, Gyro y:{get_averaged_gyro(1)} rad/s, Gyro z: {get_averaged_gyro(2)} rad/s \n")

#X = Left/Right Y=Forward/Back Z = Up/Down
#Gyro 1 = Pitch 2 = Roll 3 = Yaw