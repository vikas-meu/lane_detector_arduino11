from arduinopyfirmata import motor_setup
from lanedetector import getLaneCurve
import WebcamModule


 
motor = motor_setup()  # This will initialize and return the motor object
 
def main():
    img = WebcamModule.getImg()
    curveVal = getLaneCurve(img, 0)
    
    
    sen = 1.3  # SENSITIVITY
    maxVal = 0.3  # MAX SPEED
    if curveVal > maxVal:
        curveVal = maxVal
    if curveVal < -maxVal:
        curveVal = -maxVal
    print(curveVal)
    
    if curveVal > 0:
        sen = 1.7
        if curveVal < 0.05:
            curveVal = 0
    else:
        if curveVal > -0.08:
            curveVal = 0

    motor.move(0.20, -curveVal * sen, 0.05)

if __name__ == '__main__':
    while True:
        main()
