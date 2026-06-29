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

elapsed_time = 0

time_delay = 0.1

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

def write_data(message):
    with open("/data.csv", "a") as file:
        file.write(message)
        file.write("\n")

write_data("time,acc_x_1,acc_y_1,acc_z_1_1,acc_x_2,acc_y_2,acc_z_1_2,gyro_1_1,gyro_2_1,gyro_3_1,gyro_1_2,gyro_2_2,gyro_3_2,altitude,temperature")


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

#time,acc_x,acc_y,acc_z,gyro_1,gyro_2,gyro_3,altitue,temperature

while True:

    time.sleep(time_delay)
    elapsed_time+=time_delay
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


        acc_x_1 = accelerometer1.acceleration[0]+acceleration_calibration_1[0]
        acc_y_1 = accelerometer1.acceleration[1]+acceleration_calibration_1[1]
        acc_z_1 = accelerometer1.acceleration[2]+acceleration_calibration_1[2]

        acc_x_2 = accelerometer2.acceleration[0]+acceleration_calibration_2[0]
        acc_y_2 = accelerometer2.acceleration[1]+acceleration_calibration_2[1]
        acc_z_2 = accelerometer2.acceleration[2]+acceleration_calibration_2[2]

        gyro_x_1 = accelerometer1.gyro[0]+gyro_calibration_1[0]
        gyro_y_1 = accelerometer1.gyro[1]+gyro_calibration_1[1]
        gyro_z_1 = accelerometer1.gyro[2]+gyro_calibration_1[2]

        gyro_x_2 = accelerometer2.gyro[0]+gyro_calibration_2[0]
        gyro_y_2 = accelerometer2.gyro[1]+gyro_calibration_2[1]
        gyro_z_2 = accelerometer2.gyro[2]+gyro_calibration_2[2]


        write_data(f"{elapsed_time},{acc_x_1},{acc_y_1},{acc_z_1},{acc_x_2},{acc_y_2},{acc_z_2},{gyro_x_1},{gyro_x_1},{gyro_z_1},{gyro_x_2},{gyro_x_2},{gyro_z_2},{bmp.altitude},{bmp.temperature}")
        #print(f"Acceleration x: {get_averaged_acceleration(0)} m/s^2, Acceleration y:{get_averaged_acceleration(1)} m/s^2, Acceleration z: {get_averaged_acceleration(2)} m/s^2")
        #print(f"Gyro x: {get_averaged_gyro(0)} rad/s, Gyro y:{get_averaged_gyro(1)} rad/s, Gyro z: {get_averaged_gyro(2)} rad/s \n")

#X = Left/Right Y=Forward/Back Z = Up/Down
#Gyro 1 = Pitch 2 = Roll 3 = Yaw
