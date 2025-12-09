#!/usr/bin/env python
# coding: latin-1
# Keyboard Control for BTS7960B Motor Driver Robot Car
# Fixed for left drift issue

import RPi.GPIO as io
import sys
import tty
import termios

# Set GPIO mode to BCM
io.setmode(io.BCM)

# PWM_MAX defines the maximum motor speed (in percent)
PWM_MAX = 100

# Disable RPi.GPIO warnings
io.setwarnings(False)

# --- GPIO CONFIGURATION ---

# Left motor driver
L_L_EN = 16
L_R_EN = 12
L_L_PWM = 21
L_R_PWM = 20

# Right motor driver
R_L_EN = 7
R_R_EN = 1
R_L_PWM = 25
R_R_PWM = 8

# Motor pins
leftmotor_in1_pin = L_L_EN
leftmotor_in2_pin = L_R_EN
rightmotor_in1_pin = R_L_EN
rightmotor_in2_pin = R_R_EN

# Set motor pins as output
io.setup(leftmotor_in1_pin, io.OUT)
io.setup(leftmotor_in2_pin, io.OUT)
io.setup(rightmotor_in1_pin, io.OUT)
io.setup(rightmotor_in2_pin, io.OUT)

# Initialize GPIO pins safely
io.output(leftmotor_in1_pin, True)
io.output(leftmotor_in2_pin, True)
io.output(rightmotor_in1_pin, True)
io.output(rightmotor_in2_pin, True)

# PWM pins
leftmotorpwm_pin_l = L_L_PWM
leftmotorpwm_pin_r = L_R_PWM
rightmotorpwm_pin_l = R_L_PWM
rightmotorpwm_pin_r = R_R_PWM

# Set PWM pins as output
io.setup(leftmotorpwm_pin_l, io.OUT)
io.setup(leftmotorpwm_pin_r, io.OUT)
io.setup(rightmotorpwm_pin_l, io.OUT)
io.setup(rightmotorpwm_pin_r, io.OUT)

# Create PWM objects
leftmotorpwm_l = io.PWM(leftmotorpwm_pin_l, 100)
leftmotorpwm_r = io.PWM(leftmotorpwm_pin_r, 100)
rightmotorpwm_l = io.PWM(rightmotorpwm_pin_l, 100)
rightmotorpwm_r = io.PWM(rightmotorpwm_pin_r, 100)

# Start PWM with 0% duty cycle
leftmotorpwm_l.start(0)
leftmotorpwm_r.start(0)
rightmotorpwm_l.start(0)
rightmotorpwm_r.start(0)

# Default speed
speed = 0.5

# --- MOTOR CORRECTION FACTORS ---
# Adjust to fix left drift
LEFT_FACTOR = 1.0
RIGHT_FACTOR = 0.90  # Reduce right motor slightly

# --- MOTOR CONTROL FUNCTIONS ---

def setMotorLeft(power):
    pwm = min(abs(power) * PWM_MAX, PWM_MAX)
    if power > 0:
        leftmotorpwm_l.ChangeDutyCycle(0)
        leftmotorpwm_r.ChangeDutyCycle(pwm)
    elif power < 0:
        leftmotorpwm_l.ChangeDutyCycle(pwm)
        leftmotorpwm_r.ChangeDutyCycle(0)
    else:
        leftmotorpwm_l.ChangeDutyCycle(0)
        leftmotorpwm_r.ChangeDutyCycle(0)

def setMotorRight(power):
    pwm = min(abs(power) * PWM_MAX, PWM_MAX)
    if power > 0:
        rightmotorpwm_l.ChangeDutyCycle(0)
        rightmotorpwm_r.ChangeDutyCycle(pwm)
    elif power < 0:
        rightmotorpwm_l.ChangeDutyCycle(pwm)
        rightmotorpwm_r.ChangeDutyCycle(0)
    else:
        rightmotorpwm_l.ChangeDutyCycle(0)
        rightmotorpwm_r.ChangeDutyCycle(0)

def stopMotors():
    setMotorLeft(0)
    setMotorRight(0)

# --- MOVEMENT FUNCTIONS WITH CORRECTION ---

def moveForward():
    setMotorLeft(speed * LEFT_FACTOR)
    setMotorRight(speed * RIGHT_FACTOR)
    print(f"Forward - Speed: {int(speed*100)}%")

def moveBackward():
    setMotorLeft(-speed * LEFT_FACTOR)
    setMotorRight(-speed * RIGHT_FACTOR)
    print(f"Backward - Speed: {int(speed*100)}%")

def turnLeft():
    setMotorLeft(-speed * 0.5 * LEFT_FACTOR)
    setMotorRight(speed * RIGHT_FACTOR)
    print(f"Turn left - Speed: {int(speed*100)}%")

def turnRight():
    setMotorLeft(speed * LEFT_FACTOR)
    setMotorRight(-speed * 0.5 * RIGHT_FACTOR)
    print(f"Turn right - Speed: {int(speed*100)}%")

# --- CLEANUP FUNCTION ---

def cleanup():
    stopMotors()
    io.output(leftmotor_in1_pin, False)
    io.output(leftmotor_in2_pin, False)
    io.output(rightmotor_in1_pin, False)
    io.output(rightmotor_in2_pin, False)
    leftmotorpwm_l.stop()
    leftmotorpwm_r.stop()
    rightmotorpwm_l.stop()
    rightmotorpwm_r.stop()
    io.cleanup()
    print("\nGPIO cleaned up. Program terminated.")

# --- KEYBOARD INPUT FUNCTION ---

def getKey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# --- MAIN PROGRAM ---

def main():
    global speed

    print("=" * 50)
    print("Robot Car Keyboard Control")
    print("=" * 50)
    print("\nControls:")
    print("  W or Up Arrow      = Forward")
    print("  S or Down Arrow    = Backward")
    print("  A or Left Arrow    = Turn left")
    print("  D or Right Arrow   = Turn right")
    print("  Spacebar           = Stop")
    print("  + or =             = Increase speed")
    print("  - or _             = Decrease speed")
    print("  Q or ESC           = Exit")
    print("=" * 50)
    print(f"\nCurrent speed: {int(speed*100)}%")
    print("Ready for input...\n")

    try:
        while True:
            key = getKey()

            if key.lower() == 'w' or key == '\x1b[A':
                moveForward()
            elif key.lower() == 's' or key == '\x1b[B':
                moveBackward()
            elif key.lower() == 'a' or key == '\x1b[D':
                turnLeft()
            elif key.lower() == 'd' or key == '\x1b[C':
                turnRight()
            elif key == ' ':
                stopMotors()
                print("Stop")
            elif key == '+' or key == '=':
                if speed < 1.0:
                    speed += 0.1
                    speed = min(speed, 1.0)
                    print(f"Speed increased: {int(speed*100)}%")
            elif key == '-' or key == '_':
                if speed > 0.1:
                    speed -= 0.1
                    speed = max(speed, 0.1)
                    print(f"Speed decreased: {int(speed*100)}%")
            elif key.lower() == 'q' or key == '\x1b':
                print("\nExiting program...")
                break

    except KeyboardInterrupt:
        print("\nProgram interrupted by user...")

    finally:
        cleanup()

if __name__ == "__main__":
    main()

