#!/usr/bin/env python3


from gpiozero import PWMOutputDevice
from time import sleep

def set_pwm_parameters(pin: int, frequency: float, duty_cycle: float):
    """
    Set parameters for a hardware PWM pin using the GPIO Zero library.
    
    Args:
        pin (int): The GPIO pin number to use for PWM.
        frequency (float): The frequency in hertz (Hz).
        duty_cycle (float): The duty cycle as a percentage (0 to 100).
        
    Raises:
        ValueError: If the duty cycle is not in the range 0-100.
    """
    if not (0 <= duty_cycle <= 100):
        raise ValueError("Duty cycle must be becdtween 0 and 100.")
    
    # Initialize the PWMOutputDevice
    pwm = PWMOutputDevice(pin, frequency=frequency)
    
    # Set the duty cycle
    pwm.value = duty_cycle / 100.0  # Convert percentage to a ratio
    
    print(f"PWM set on pin {pin} with frequency {frequency} Hz and duty cycle {duty_cycle}%")
    
    # Keep the PWM running
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Stopping PWM...")
        pwm.close()

# Example usage:
# set_pwm_parameters(pin=18, frequency=1000, duty_cycle=50)
if __name__ == "__main__":
    set_pwm_parameters(pin=18, frequency=400, duty_cycle=20)