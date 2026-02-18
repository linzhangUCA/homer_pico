from machine import UART, Pin
from time import time, ticks_us, ticks_diff
from diff_drive_controller import DiffDriveController


# SETUP
uart_msngr = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
mobile_base = DiffDriveController(
    left_wheel_ids=((16, 17, 18), (19, 20)),
    right_wheel_ids=((15, 14, 13), (12, 11)),
)
mobile_base.awaken()

# Variables
tx_period_us = 16_667  # 60Hz
targ_lin_vel, targ_ang_vel = 0.0, 0.0
last_us = ticks_us()
# print("UART0 is ready...")  # debug

while True:
    # Transmit data (TX)
    now_us = ticks_us()
    if ticks_diff(now_us, last_us) >= tx_period_us:
        meas_lin_vel, meas_ang_vel = mobile_base.get_vels()
        out_msg = f"{meas_lin_vel:.4f},{meas_ang_vel:.4f}\n".encode("utf-8")
        uart_msngr.write(out_msg)  # main.py will send this to computer
        last_us = now_us  # update last time stamp
    # Receive data (RX)
    if uart_msngr.any():
        # Read all available bytes
        in_data = uart_msngr.readline()
        in_msg = in_data.decode("utf-8").strip()  # strip whitespace
        targ_vels = in_msg.split(",")  # get a list
        print(targ_vels)
        if len(targ_vels) == 2:
            targ_lin_vel = float(targ_vels[0])
            targ_ang_vel = float(targ_vels[1])
            mobile_base.set_vels(targ_lin_vel, targ_ang_vel)
