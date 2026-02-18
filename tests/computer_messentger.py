import serial
from time import time, sleep
import struct

# SETUP
# Linux example: '/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyAMA0'
# Mac example: '/dev/cu.usbmodem1413301''
# Windows example: 'COM3', 'COM4'
# SERIAL_PORT = "/dev/ttyACM0" # USB
SERIAL_PORT = "/dev/ttyAMA0"  # UART
BAUD_RATE = 115200
# BAUD_RATE = 921600
ser_messenger = serial.Serial(
    SERIAL_PORT, BAUD_RATE, timeout=0.01
)  # set error recovery duration half the pico talker's period
print(f"Connected to {SERIAL_PORT}")
# Variables
tlvs_pos = [0.00, 0.10, 0.20, 0.30, 0.40]
tlvs_neg = [0.00, -0.10, -0.20, -0.30, -0.40]
targ_lin_vels = (
    tlvs_pos + list(reversed(tlvs_pos)) + tlvs_neg + list(reversed(tlvs_neg))
)
msg_id = 0
sleep(3)  # Wait briefly for the connection to stabilize
print("Starting communication... Press Ctrl+C to stop.")
last_stamp = time()

# LOOP
try:
    while True:
        # Transmit data (TX)
        current_stamp = time()
        if (current_stamp - last_stamp) >= 0.2:  # 5Hz TX
            # msg = f"{targ_lin_vels[msg_id % 20]:.2f},0.00\n"
            # ser_messenger.write(msg.encode("utf-8"))  # encode string to bytes and send
            out_packet = struct.pack(
                "<Bff", 0xAA, targ_lin_vels[msg_id % 20], 0.00
            )  # 4 bytes total
            print(out_packet)  # debug
            ser_messenger.write(out_packet)
            msg_id += 1
            last_stamp = current_stamp

        # Receive data (RX)
        if ser_messenger.in_waiting > 0:
            try:
                # Read line, decode bytes to string, and strip whitespace
                in_packet = ser_messenger.read()
                in_msg = in_packet.decode("utf-8").strip()
                if in_msg:
                    print(f"Computer heard: {in_msg}")
                else:
                    print("No message received.")
            except UnicodeDecodeError:
                pass

except KeyboardInterrupt:
    print("\nCommunication stopped by user.")
    ser_messenger.close()
