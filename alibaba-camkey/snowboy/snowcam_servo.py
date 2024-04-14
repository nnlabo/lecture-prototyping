# coding: UTF-8
import snowboydecoder
import sys
import signal
import sys
import time
import RPi.GPIO as GPIO

interrupted = False

model = sys.argv[1]


#Start Processing
print('--------------------------------')
print('Start Processing')

def moveservo():
    
    #set open and close pose duty
    open_pose=3.5
    close_pose=8.0
    #Setting for Servo
    GPIO.setmode(GPIO.BCM)
    #GPIO4を出力端子設定 
    GPIO.setup(18, GPIO.OUT)
    #GPIO4をPWM設定、周波数は50Hz 
    p = GPIO.PWM(18, 50)
    #Duty Cycle 0% 
    p.start(0.0)
    p.ChangeDutyCycle(close_pose)

    print('Secret word "Snowboy" called!! Unlocking Door for 5sec!')
    p.ChangeDutyCycle(open_pose)
    time.sleep(5)
    p.ChangeDutyCycle(close_pose)
    
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

#camera = takephoto()

# main loop
detector.start(detected_callback=moveservo,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
