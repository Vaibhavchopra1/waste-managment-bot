import RPi.GPIO as GPIO
import time

# GPIO pins for Left Stepper Motor
LEFT_PULSE_PIN = 23
LEFT_DIR_PIN = 24

# GPIO pins for Right Stepper Motor
RIGHT_PULSE_PIN = 3
RIGHT_DIR_PIN = 2

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_PULSE_PIN, GPIO.OUT)
GPIO.setup(LEFT_DIR_PIN, GPIO.OUT)
GPIO.setup(RIGHT_PULSE_PIN, GPIO.OUT)
GPIO.setup(RIGHT_DIR_PIN, GPIO.OUT)

# Function to move a single stepper motor
def move_stepper(pulse_pin, dir_pin, steps, direction='forward', speed=0.005):
    GPIO.output(dir_pin, GPIO.HIGH if direction == 'forward' else GPIO.LOW)
    for _ in range(steps):
        GPIO.output(pulse_pin, GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(pulse_pin, GPIO.LOW)
        time.sleep(speed)

# Function to move both motors simultaneously
def move_both_motors(steps, direction='forward', speed=0.005):
    GPIO.output(LEFT_DIR_PIN, GPIO.HIGH if direction == 'forward' else GPIO.LOW)
    GPIO.output(RIGHT_DIR_PIN, GPIO.HIGH if direction == 'forward' else GPIO.LOW)
    
    for _ in range(steps):
        GPIO.output(LEFT_PULSE_PIN, GPIO.HIGH)
        GPIO.output(RIGHT_PULSE_PIN, GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(LEFT_PULSE_PIN, GPIO.LOW)
        GPIO.output(RIGHT_PULSE_PIN, GPIO.LOW)
        time.sleep(speed)

# Cleanup GPIO
def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    
    command = 'forward'
    
    if command == 'forward':
        print("Moving both motors forward 1000 steps...")
        move_both_motors(6000, 'forward', speed=0.001)
    
    elif command == 'backward':
        print("Moving both motors backward 1000 steps...")
        move_both_motors(6000, 'backward', speed=0.001)
    
    elif command == 'quit':
        print("Exiting program...")
    

    cleanup()
