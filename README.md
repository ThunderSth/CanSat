The code meant for a simpler cansat

It is supposed to measure the forces acting on it after being dropped using an IMU and a barometer, using a Feather RP 2040 

v1 is just for reading a single accelerometer and can be calibrated by shorting D10 with ground

double_acc is for when 2 accelerometers are used to find the average between them, single_acc is for when 1 accelerometer is used

X = Left/Right Y=Forward/Back Z = Up/Down
Gyro 1 = Pitch 2 = Roll 3 = Yaw
