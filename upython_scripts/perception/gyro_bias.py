""" Set the robot (MPU6050) still then run this script.
Vibration:
    If your robot's cooling fan is running or if it's on a vibrating table during calibration, the bias will be inaccurate.
Temperature:
    The MPU6050 is sensitive to heat.
    If you calibrate it immediately after turning it on, the bias might shift as the chip warms up. 
    For high precision, wait 60 seconds after power-up before calibrating.

"""
from perception.inertial_sensor import MPU6050
from utime import sleep

def calibrate_gyro(mpu, samples=500):
    print("Calibrating Gyro... DO NOT MOVE ROBOT")
    gyro_z_accumulator = 0
    for i in range(samples):
        # Read raw gyro data from your MPU6050 library
        # This usually returns Degrees Per Second (DPS)
        data = mpu.get_gyro_data() 
        gyro_z_accumulator += data['z']
        # Small delay to let the sensor refresh
        sleep(0.005) 
        # Optional: Blink an onboard LED to show calibration is in progress
        if i % 50 == 0:
            print(".", end="")
    bias = gyro_z_accumulator / samples
    print(f"\nCalibration Complete! Z-Bias: {bias:.4f}")
    return bias

# --- Usage in your Main Loop ---
gyro_z_bias = calibrate_gyro(my_mpu)

# Later, when calculating heading:
# actual_rate = measured_rate - gyro_z_bias
