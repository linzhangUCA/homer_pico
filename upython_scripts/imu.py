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
        MPU6050 uses 2 bytes to represent values of an entity.
        Acc_X, Acc_Y, Acc_Z, Temp, Gyro_X, Gyro_Y, Gyro_Z are stored in contiguous registers.
        To read'em all, grab 14 bytes starting at the ACCEL_XOUT_H register: 0x3B.
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
