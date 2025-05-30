"""
This Python script is for simple tests to control the motor.
Not meant for actual usage, just testing this and that.
"""
import pigpio
import time

# Constants
MICROSTEP = 480  # Steps per revolution, set with serial port setup software isv57t
#SPEED = 51         # motor speed in RPM
PUL_PIN = 18         # PWM output pin
DIR_PIN = 23         # Direction pin
ALARM_PIN = 24       # Alarm input pin
MOTOR_PWR_PIN = 25   # Motor power pin

LIMIT_SWITCH_PIN_1 = 8
LIMIT_SWITCH_PIN_2 = 7

DIR_CW = 1
DIR_CCW = 0

GEAR_RATIO = 20
MAX_RPM = 2

TARGET_RPM = 5

REVERSE = False

# Callback functions for edge detection
def switch1_callback(gpio, level, tick):
    print(f"GPIO {gpio} changed to {level} at time {tick}")
    state = pi.read(gpio)
    print(f"GPIO {gpio} state: {state}")
    if level == 1:
        print("Limit switch 1 triggered!\n\n")
        set_dir(DIR_CW)  # Change direction when switch is triggered
        return
    print("Limit switch 1 OFF\n\n")
    
def switch2_callback(gpio, level, tick):
    if level == 1:
        print("Limit switch 2 triggered!\n\n")
        set_dir(DIR_CCW)  # Change direction when switch is triggered
        return
    print("Limit switch 2 OFF\n\n")

def calc_PWM_freq(microstep, speed) -> int:
    """
    Calculate the PWM frequency based on microstepping and speed.
    Formula: PWM frequency = (speed * microstep) / 60
    Args:
        microstep (int): Number of steps per revolution, defined with isv57t software
        speed (int): Speed in RPM.
    Returns:
        int: Calculated PWM frequency for the motor to run at the specified speed.
    """
    global GEAR_RATIO
    #return int(int(((speed * microstep) / 60) * GEAR_RATIO) / 60)
    return 60

def pulses_per_second(microsteps_per_rev, gearbox_ratio, output_rpm):
    """
    Calculate the number of pulses per second (Hz) to send to the ISV57T
    to achieve the desired output RPM from a gearbox.

    Parameters:
        microsteps_per_rev (int): Microsteps per motor revolution (e.g., 1600, 3200).
        gearbox_ratio (float): Gearbox reduction ratio (e.g., 20 for 20:1).
        output_rpm (float): Desired output RPM at the gearbox shaft.

    Returns:
        float: Pulses per second (Hz) to send to the motor.
    """
    motor_rpm = output_rpm * gearbox_ratio
    pulses_per_minute = motor_rpm * microsteps_per_rev
    pulses_per_second = pulses_per_minute / 60.0
    return int(pulses_per_second)

def set_dir(dir: int):
    pi.write(DIR_PIN, dir)  # Start clockwise

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Could not connect to pigpio daemon")

# Set MOTOR_PWR_PIN as output and turn it on
pi.set_mode(MOTOR_PWR_PIN, pigpio.OUTPUT)
pi.write(MOTOR_PWR_PIN, 0)  # Turn on motor power

# Set up direction pin
pi.set_mode(DIR_PIN, pigpio.OUTPUT)
set_dir(DIR_CW)


# Set up alarm pin
pi.set_mode(ALARM_PIN, pigpio.INPUT)
pi.set_pull_up_down(ALARM_PIN, pigpio.PUD_UP)  # Enable pull-up

# Set up PWM on PUL_PIN
DUTY_CYCLE = 500000  # 50% of 255 (range is 0–255)
#speed = calc_PWM_freq(MICROSTEP, TARGET_RPM)  # Calculate PWM frequency
speed = pulses_per_second(MICROSTEP, GEAR_RATIO, TARGET_RPM)  # Calculate pulses per second
print(f"Calculated PWM frequency: {speed} Hz")
pi.hardware_PWM(PUL_PIN, speed, DUTY_CYCLE)  # Set PWM frequency and duty cycle
#pi.set_PWM_frequency(PUL_PIN, SPEED)
#pi.set_PWM_range(PUL_PIN, 255)
#pi.set_PWM_dutycycle(PUL_PIN, DUTY_CYCLE)
pi.hardware_PWM(19, 16100, DUTY_CYCLE)

pi.set_mode(LIMIT_SWITCH_PIN_1, pigpio.INPUT)
pi.set_pull_up_down(LIMIT_SWITCH_PIN_1, pigpio.PUD_UP)
cb1 = pi.callback(LIMIT_SWITCH_PIN_1, pigpio.EITHER_EDGE, switch1_callback)

pi.set_mode(LIMIT_SWITCH_PIN_2, pigpio.INPUT)
pi.set_pull_up_down(LIMIT_SWITCH_PIN_2, pigpio.PUD_UP)
cb1 = pi.callback(LIMIT_SWITCH_PIN_2, pigpio.EITHER_EDGE, switch2_callback)

print(f"PWM running on GPIO{PUL_PIN} at {speed} Hz, 50% duty cycle. Press Ctrl+C to stop.")

actual_pwm_rate_18 = pi.get_PWM_frequency(18)
print(f"Actual PWM rate pin 18: {actual_pwm_rate_18} Hz")

count = 0
try:
    while True:
        time.sleep(1)
        count += 1
        
        actual_pwm_rate_18 = pi.get_PWM_frequency(18)
        #print(f"Actual PWM rate pin 18: {actual_pwm_rate_18} Hz")
        actual_pwm_rate_19 = pi.get_PWM_frequency(19)
        #print(f"Actual PWM rate pin 19: {actual_pwm_rate_19} Hz")

        # Reverse direction every 5 seconds
        if REVERSE and count % 5 == 0:
            current_dir = pi.read(DIR_PIN)
            pi.write(DIR_PIN, not current_dir)
            print("Direction changed")

        # Print current direction
        if pi.read(DIR_PIN) == 1:
            #print("Direction: Clockwise")
            pass
        else:
            #print("Direction: Counter-clockwise")
            pass

        # Read alarm pin
        alarm_state = pi.read(ALARM_PIN)
        if alarm_state == 0:
            #print("🚨 Alarm triggered!")
            pi.write(MOTOR_PWR_PIN, 1)
        else:
            #print("✅ Alarm not triggered.")
            pass

except KeyboardInterrupt:
    print("Stopping...")
    pi.set_PWM_dutycycle(PUL_PIN, 0)
    pi.stop()
    
finally:
    cb1.cancel()