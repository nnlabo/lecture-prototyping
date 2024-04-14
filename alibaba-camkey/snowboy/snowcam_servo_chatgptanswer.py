# coding: UTF-8
import snowboydecoder
import sys
import signal
import RPi.GPIO as GPIO
import time  # timeモジュールを追加

interrupted = False

model = sys.argv[1]

# GPIOの設定
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# PWMの設定
pwm = GPIO.PWM(servo_pin, 50)  # PWM周波数は50Hz
pwm.start(0)

# サーボの角度を変更する関数
def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

# サーボを90度回転させる関数
def moveservo():
    set_angle(90)
    time.sleep(5)  # 5秒間待機してからサーボを元の位置に戻す
    set_angle(0)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

# Ctrl+Cで終了
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# メインループ
detector.start(detected_callback=moveservo,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()

# 終了時にGPIOをクリーンアップ
GPIO.cleanup()
