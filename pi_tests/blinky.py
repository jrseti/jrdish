#!/usr/bin/env python3
from gpiozero import LED, Button
from time import sleep
import getpass

username = getpass.getuser()
print(username)

led = LED(18)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)

