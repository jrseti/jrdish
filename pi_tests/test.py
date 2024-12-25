from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory

# Set the pin factory
LED.pin_factory = PiGPIOFactory()

# Test with an LED
led = LED(17)
led.on()
