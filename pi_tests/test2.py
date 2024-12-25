import pigpio

pi = pigpio.pi()  # Connect to the pigpiod daemon
if not pi.connected:
    print("Unable to connect to pigpio daemon.")
else:
    print("Connected to pigpio daemon!")
    pi.stop()
