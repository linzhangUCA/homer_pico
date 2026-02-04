from machine import Pin, I2C


class MPU6050:
    def __init__(self, scl_id=9, sda_id=8, i2c_addr=0x68) -> None:
        self.iic = I2C(0, scl=Pin(scl_id), sda=Pin(sda_id), freq=400_000)
        self.addr = i2c_addr
        self.iic.writeto(
            self.addr,
            bytes(107),  # PWR_MGMT_1 register
            bytes(0),
        )  # wake up sensor

    def _read_raw_data(self, reg_addr):
        # Read two bytes (high and low) and combine them
        val = self.iic.readfrom_mem(self.addr, reg_addr, 2)
        y = (val[0] << 8) | val[1]
        if y > 32768:
            y = y - 65536
        return y

    def get_values(self):
        # Raw readings for 6 axes
        # AcX, AcY, AcZ, Temp, GyX, GyY, GyZ are contiguous registers
        # For simplicity in this assignment, we read them individually
        # or you can read block 14 bytes for speed (advanced).
        # Accelerometer
        ac_x = self._read_raw_data(0x3B)
        ac_y = self._read_raw_data(0x3D)
        ac_z = self._read_raw_data(0x3F)

        # Gyroscope
        gy_x = self._read_raw_data(0x43)
        gy_y = self._read_raw_data(0x45)
        gy_z = self._read_raw_data(0x47)

        # Scaling (Default ranges: Accel +/- 2g, Gyro +/- 250 deg/s)
        # 16384.0 is the scale factor for 2g
        # 131.0 is the scale factor for 250 deg/s
        return {
            "AcX": ac_x / 16384.0,
            "AcY": ac_y / 16384.0,
            "AcZ": ac_z / 16384.0,
            "GyX": gy_x / 131.0,
            "GyY": gy_y / 131.0,
            "GyZ": gy_z / 131.0,
        }


if __name__ == "__main__":
    from utime import ticks_ms, sleep

    # SETUP
    try:
        imu = MPU6050()
        print("IMU Connected!")
    except OSError:
        print("IMU Not Found - Check Wiring!")

    # LOOP
    while True:
        loop_start = ticks_ms()

        # 1. Read IMU
        # The library returns a dictionary
        data = imu.get_values()

        # Extract values for cleaner code
        ax = data["AcX"]
        ay = data["AcY"]
        az = data["AcZ"]
        gx = data["GyX"]
        gy = data["GyY"]
        gz = data["GyZ"]

        # 2. Your Existing Sensors (Mock example)
        current_enc = 100  # Replace with encoder.read()
        current_dist = 25.5  # Replace with sonar variable

        # 3. Format the "State Vector" Message
        # Structure: [Header]: Dist, Enc, Ax, Ay, Az, Gx, Gy, Gz
        msg = "[Pico, {}]: {:.1f}, {}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(
            loop_start, current_dist, current_enc, ax, ay, az, gx, gy, gz
        )

        print(msg)

        sleep(0.016)  # Approx 60Hz
