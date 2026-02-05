from machine import Pin, PWM, reset
from time import ticks_us


class HCSR04:
    def __init__(self, echo_id, trig_id):
        self.echo_pin = Pin(echo_id, Pin.IN, Pin.PULL_DOWN)
        self.echo_pin.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._echo_handler
        )
        self.trig_pin = PWM(Pin(trig_id), freq=15, duty_ns=10_000)  # 10ms pulse @ 15Hz
        # Variables
        self.distance = 0.0
        self.start_time = None

    def _echo_handler(self, pin):
        if pin.value():
            self.start_time = ticks_us()
        else:
            dt = ticks_us() - self.start_time
            if 100 <= dt < 38000:
                self.distance = dt / 58 / 100
            else:  # dt < 0.1 ms or dt > 38 ms
                self.distance = 0.0  # no detection


if __name__ == "__main__":
    from time import sleep_ms

    sensor = HCSR04(echo_id=21, trig_id=22)

    try:
        while True:
            print(f"Distance: {sensor.distance} m")
            sleep_ms(200)
    except KeyboardInterrupt:
        reset()
