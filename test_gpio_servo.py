# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 11:00:00 2023

@author: jhutchison

"""

# %% Packages
""" Third party and local imports """

import RPi.GPIO as GPIO
import time

# %% Functions
""" Define functions """


# Function to convert angle to duty cycle
def angle_to_duty_cycle(angle):
    """
    Convert servo angle (0-270 degrees) to duty cycle (2.5-12.5)
    for ANNIMOS 20KG servos with 270° range
    """
    # Map angle from 0-270 to 2.5-12.5 duty cycle
    duty = 2.5 + (angle / 270) * 10
    return duty


# %% Variables
""" Set script (global) variables """

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for servo control
SERVO_1_PIN = 18  # Glass Tipper (Effect 1)
SERVO_2_PIN = 19  # Release for Jumping Mechanism (Effect 2)

# Set up GPIO pins as outputs
GPIO.setup(SERVO_1_PIN, GPIO.OUT)
GPIO.setup(SERVO_2_PIN, GPIO.OUT)

# Create PWM objects for each servo (50Hz PWM frequency)
servo1 = GPIO.PWM(SERVO_1_PIN, 50)
servo2 = GPIO.PWM(SERVO_2_PIN, 50)

# Start PWM with 0 duty cycle (servo centered)
servo1.start(0)
servo2.start(0)


# %% Main
""" Display task data """

if __name__ == "__main__":

    try:
        while True:
            # Test Servo 1 (Glass Tipper)
            print("Moving Servo 1 (Glass Tipper)")

            # Starting position
            servo1.ChangeDutyCycle(angle_to_duty_cycle(0))
            time.sleep(1)

            # Quick tip motion
            servo1.ChangeDutyCycle(angle_to_duty_cycle(90))
            time.sleep(0.5)

            # Return to starting position
            servo1.ChangeDutyCycle(angle_to_duty_cycle(0))
            time.sleep(2)

            # Test Servo 2 (Release Mechanism)
            print("Moving Servo 2 (Release Mechanism)")

            # Starting position (locked)
            servo2.ChangeDutyCycle(angle_to_duty_cycle(0))
            time.sleep(1)

            # Quick release motion
            servo2.ChangeDutyCycle(angle_to_duty_cycle(90))
            time.sleep(1)

            # Return to starting position
            servo2.ChangeDutyCycle(angle_to_duty_cycle(0))
            time.sleep(3)

            # Ask user if they want to continue
            choice = input("Press ENTER to test again, or 'q' to quit: ")
            if choice.lower() == "q":
                break

    finally:
        # Clean up and release resources
        servo1.stop()
        servo2.stop()
        GPIO.cleanup()
        print("Program ended safely")

    print("logger update here, main complete")
# %%
