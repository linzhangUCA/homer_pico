from machine import Pin, I2C


class MPU6050:
    def __init__(self, scl_id=9, sda_id=8, i2c_addr=0x68):
        self.i2c = I2C(0, scl=Pin(scl_id), sda=Pin(sda_id), freq=400_000)
        self.i2c_addr = i2c_addr
        self.i2c.writeto_mem(
            self.i2c_addr,
            0x6B,  # PWR_MGMT_1 register address
            bytes([0x00]),  # data
        )  # wake up sensor
        # TODO: DHPF configuration

    def read_data(self):
        """
        MPU6050 uses 2 bytes to represent values of an entity
        Acc_X, Acc_Y, Acc_Z, Temp, Gyro_X, Gyro_Y, Gyro_Z are contiguous registers.
        To read'em all, grab 14 bytes starting at the first Acc_X register: 0x3B.
        """
        words = self.i2c.readfrom_mem(
            self.i2c_addr,
            0x3B,  # ACCEL_XOUT_H register address
            14,  # number of bytes
        )  # retrieve raw sensor data in bytes

        data = [words[i] << 8 | words[i + 1] for i in range(0, len(words), 2)]
        lin_acc_x = (data[0] - 65535) / 16384 if data[0] > 32767 else data[0] / 16384
        lin_acc_y = (data[1] - 65535) / 16384 if data[1] > 32767 else data[1] / 16384
        lin_acc_z = (data[2] - 65535) / 16384 if data[2] > 32767 else data[2] / 16384
        ang_vel_x = (data[4] - 65535) / 16384 if data[4] > 32767 else data[4] / 16384
        ang_vel_y = (data[5] - 65535) / 16384 if data[5] > 32767 else data[5] / 16384
        ang_vel_z = (data[6] - 65535) / 16384 if data[6] > 32767 else data[6] / 16384

        return {
            "lin_acc_x": lin_acc_x,
            "lin_acc_y": lin_acc_y,
            "lin_acc_z": lin_acc_z,
            "ang_vel_x": ang_vel_x,
            "ang_vel_y": ang_vel_y,
            "ang_vel_z": ang_vel_z,
        }

    # def get_values(self):
    #     # Raw readings for 6 axes
    #     # AcX, AcY, AcZ, Temp, GyX, GyY, GyZ are contiguous registers
    #     # For simplicity in this assignment, we read them individually
    #     # or you can read block 14 bytes for speed (advanced).
    #
    #     # Accelerometer
    #     ac_x = self.read_data(0x3B)
    #     ac_y = self.read_data(0x3D)
    #     ac_z = self.read_data(0x3F)
    #
    #     # Gyroscope
    #     gy_x = self.read_data(0x43)
    #     gy_y = self.read_data(0x45)
    #     gy_z = self.read_data(0x47)
    #
    #     # Scaling (Default ranges: Accel +/- 2g, Gyro +/- 250 deg/s)
    #     # 16384.0 is the scale factor for 2g
    #     # 131.0 is the scale factor for 250 deg/s
    #     return {
    #         "AcX": ac_x / 16384.0,
    #         "AcY": ac_y / 16384.0,
    #         "AcZ": ac_z / 16384.0,
    #         "GyX": gy_x / 131.0,
    #         "GyY": gy_y / 131.0,
    #         "GyZ": gy_z / 131.0,
    #     }
    #


if __name__ == "__main__":
    from utime import ticks_ms, sleep_ms

    # SETUP
    try:
        sensor = MPU6050()
        print("IMU Connected!")
    except OSError:
        print("IMU Not Found - Check Wiring!")

    # LOOP
    while True:
        stamp = ticks_ms()
        # data = sensor.get_values()
        #
        # # Extract values for cleaner code
        # ax = data["AcX"]
        # ay = data["AcY"]
        # az = data["AcZ"]
        # gx = data["GyX"]
        # gy = data["GyY"]
        # gz = data["GyZ"]
        #
        # Structure: [Header]: Ax, Ay, Az, Gx, Gy, Gz
        # msg = f"[Pico, {stamp}]: {ax:.2f}, {ay:.2f}, {az:.2f}, {gx:.2f}, {gy:.2f}, {gz:.2f}"
        data = sensor.read_data()

        print(f"[Pico, {stamp}]:")
        print("---")
        print(
            f"acc_x={data['lin_acc_x']} m/s^2, acc_y={data['lin_acc_y']} m/s^2, acc_z={data['lin_acc_z']} m/s^2"
        )
        print(
            f"angv_x={data['ang_vel_x']} deg/s, angv_y={data['ang_vel_y']} deg/s, angv_z={data['ang_vel_z']} deg/s"
        )

        sleep_ms(16)  # Approx 60Hz
