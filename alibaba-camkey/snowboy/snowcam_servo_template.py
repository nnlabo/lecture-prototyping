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
    
    #Write your code here to move servo 90 degree to unlock key
    
    #Procedure
    #set GPIO 18 for servo signal pin
    #servo pwm frequency is 50Hz
    #lock position is 0 degree
    #unlock position is about 90 degree
    #keep unlock for 5sec
    
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
