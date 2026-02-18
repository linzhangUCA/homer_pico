from machine import UART, Pin
from time import time, ticks_ms, ticks_diff

uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# txData = b"hello world\n\r"
# uart0.write(txData)
# time.sleep(0.1)
# rxData = bytes()
# while uart0.any() > 0:
#     rxData += uart0.read(1)
#
# print(rxData.decode("utf-8"))

# Variables
tx_interval_ms = 100  # 10Hz
last_ms = ticks_ms()
msg_id = 0
print("UART0 is ready...")

while True:
    # Transmit data (TX)
    now_ms = ticks_ms()
    if ticks_diff(now_ms, last_ms) >= tx_interval_ms:
        out_msg = f"[Pico, {now_ms}]: Hello, {msg_id}\n\r".encode("utf-8")
        uart0.write(out_msg)  # main.py will send this to computer
        msg_id += 1
        last_ms = now_ms  # update last time stamp
    # Receive data (RX)
    if uart0.any():
        # Read all available bytes
        in_data = uart0.readline()
        try:
            # Decode bytes to string and strip whitespace/newlines
            in_msg = in_data.decode("utf-8").strip()
            if in_msg:
                print(f"Received: {in_msg}")
        except UnicodeError:
            print("Received non-UTF-8 data")
