/*
 * pwm.c:
 *	This tests the hardware PWM channel.
 *
 * Copyright (c) 2012-2013 Gordon Henderson.
 ***********************************************************************
 * This file is part of wiringPi:
 *      https://github.com/WiringPi/WiringPi
 *
 *    wiringPi is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Lesser General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    wiringPi is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public License
 *    along with wiringPi.  If not, see <http://www.gnu.org/licenses/>.
 ***********************************************************************
 */

#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define PWM_PIN 1

int wpSetupAlready = 0;
#define PWM_CLOCK_FREQ_HZ 19.2e6
#define PWM_RANGE 1024


/**
 * Setup wiringPi
 * Calls wiringPiSetup() if it hasn't been called yet.
 */
void wpSetup() {
  if (wpSetupAlready) {
    return;
  }
  if (wiringPiSetup () == -1)
    exit (1) ;
  wpSetupAlready = 1;
}

void wpSetupForPWM() {
  wpSetup();
  pinMode (PWM_PIN, PWM_MS_OUTPUT) ;
}

void setPWMFreq(int freq, int duty_cycle) {
  // Set the PWM clock divider to adjust the frequency range
    // PWM frequency = 19.2 MHz / (PWM_CLOCK * PWM_RANGE)
    // So, PWM_CLOCK should be set in such a way that it gives the correct frequency

    // Set the PWM clock divisor based on the input frequency
    int pwmClock = 19200000 / (1024 * freq);
    pwmSetClock(pwmClock);  // Set the PWM clock divider

    printf("Generating PWM signal on GPIO 18 (Pin 1) at %d Hz\n", freq);

    // Generate a 50% duty cycle PWM signal (you can modify the duty cycle if needed)
    pwmWrite(PWM_PIN, (int)((float)PWM_RANGE*(float)(duty_cycle)/100.0));  // Set duty cycle to 50% (half of 1024)

}

int main (int c, char *argv[])
{
//#int bright ;

  printf ("Raspberry Pi wiringPi PWM test program\n") ;
  if(c < 3) {
    printf("Usage: %s <frequency> <duty_cycle>\n", argv[0]);
    return 1;
  }

  wpSetupForPWM();
  setPWMFreq(atoi(argv[1]), atoi(argv[2]));

  /*
  for (;;)
  {
    for (bright = 0 ; bright < 1024 ; ++bright)
    {
      pwmWrite (1, bright) ;
      delay (1) ;
    }

    for (bright = 1023 ; bright >= 0 ; --bright)
    {
      pwmWrite (1, bright) ;
      delay (1) ;
    }
  }
  */
/*
  for(;;) {
	  delay(100);
   }
   */

  return 0 ;
}
