import pyfirmata
from time import sleep

class Motor():
    def __init__(self, port, EnaA, In1A, In2A, EnaB, In1B, In2B):
        self.board = pyfirmata.Arduino(port)  # Connect to the Arduino board
        self.EnaA = self.board.get_pin(f'd:{EnaA}:p')  # Enable pins as PWM
        self.In1A = self.board.get_pin(f'd:{In1A}:o')  # Motor direction pins as OUTPUT
        self.In2A = self.board.get_pin(f'd:{In2A}:o')
        self.EnaB = self.board.get_pin(f'd:{EnaB}:p')
        self.In1B = self.board.get_pin(f'd:{In1B}:o')
        self.In2B = self.board.get_pin(f'd:{In2B}:o')
        self.mySpeed = 0

    def move(self, speed=0.5, turn=0, t=0):
        speed *= 255  # Scale to PWM range (0-255)
        turn *= 70    # Adjust turn sensitivity

        leftSpeed = speed - turn
        rightSpeed = speed + turn

        # Ensure speed is within PWM range
        leftSpeed = max(0, min(255, leftSpeed))
        rightSpeed = max(0, min(255, rightSpeed))

        # Set motor PWM values
        self.EnaA.write(leftSpeed / 255)  # Normalize PWM range (0 to 1)
        self.EnaB.write(rightSpeed / 255)

        # Set motor direction
        if leftSpeed > 0:
            self.In1A.write(1)
            self.In2A.write(0)
        else:
            self.In1A.write(0)
            self.In2A.write(1)

        if rightSpeed > 0:
            self.In1B.write(1)
            self.In2B.write(0)
        else:
            self.In1B.write(0)
            self.In2B.write(1)

        sleep(t)

    def stop(self, t=0):
        # Stop motors by setting PWM to 0
        self.EnaA.write(0)
        self.EnaB.write(0)
        self.mySpeed = 0
        sleep(t)

def motor_setup():
    # Create motor instance (Adjust COM port and pins as needed)
    motor = Motor('COM12', 3, 5, 6, 9, 10, 11)
    return motor
