import board
import time
import adafruit_mpu6050
import digitalio
import adafruit_bmp280
i2c = board.I2C()
imu = adafruit_mpu6050.MPU6050(i2c,address=0x68)


switch = digitalio.DigitalInOut(board.D10)
switch.switch_to_input(pull=digitalio.Pull.UP)


acceleration_calibration = [0,0,0]
gyro_calibration = [0,0,0]

def calibrate():
    acceleration_calibration.append(0-imu.acceleration[0])
    acceleration_calibration.append(0-imu.acceleration[1])
    acceleration_calibration.append(9.82-imu.acceleration[2])
    
    
    for i in range(3):
        gyro_calibration.append(0-imu.gyro[i])

    print(acceleration_calibration,gyro_calibration)

BUTTON_HOLD_TIME = 1
started_holding = 0

while True:
    time.sleep(0.1)
    if not switch.value and time.time()-started_holding > BUTTON_HOLD_TIME:
        print("calibrating")
        acceleration_calibration = []
        gyro_calibration = []
        calibrate()
        started_holding = time.time()
    else:
        print(f"Acceleration x: {imu.acceleration[0]+acceleration_calibration[0]} m/s^2, Acceleration y:{imu.acceleration[1]+acceleration_calibration[1]} m/s^2, Acceleration z: {imu.acceleration[2]+acceleration_calibration[2]} m/s^2")
        print(f"Gyro x: {imu.gyro[0]+gyro_calibration[0]} rad/s, Gyro y:{imu.gyro[1]+gyro_calibration[1]} rad/s, Gyro z: {imu.gyro[2]+gyro_calibration[2]} rad/s \n")

#X = Left/Right Y=Forward/Back Z = Up/Down
#Gyro 1 = Pitch 2 = Roll 3 = Yaw
