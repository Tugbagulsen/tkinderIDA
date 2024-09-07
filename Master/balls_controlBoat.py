import cv2
import numpy as np
from tkinter import messagebox
import time

# ESC'leri kontrol etmek için pigpio nesnesi oluştur
import pigpio

# Motorların bağlı olduğu GPIO pinleri
left_motor_pin = 17
right_motor_pin = 18

# PWM genişlikleri
min_pulse_width = 1000
max_pulse_width = 2000

# pigpio instance
pi = pigpio.pi()

# Kademeli motor hareketi
def gradual_move(pin, target_pulse_width, step_size=10, step_delay=0.01):
    current_pulse_width = pi.get_servo_pulsewidth(pin)
    step = step_size if target_pulse_width > current_pulse_width else -step_size

    for pulse_width in range(current_pulse_width, target_pulse_width, step):
        pi.set_servo_pulsewidth(pin, pulse_width)
        time.sleep(step_delay)
    
    pi.set_servo_pulsewidth(pin, target_pulse_width)

# Motor hareket fonksiyonları
def turn_left():
    gradual_move(left_motor_pin, min_pulse_width)
    gradual_move(right_motor_pin, max_pulse_width)
    time.sleep(1)
    stop_motors()

def turn_right():
    gradual_move(left_motor_pin, max_pulse_width)
    gradual_move(right_motor_pin, min_pulse_width)
    time.sleep(1)
    stop_motors()

def go_straight():
    gradual_move(left_motor_pin, max_pulse_width)
    gradual_move(right_motor_pin, max_pulse_width)
    time.sleep(1)
    stop_motors()

def stop_motors():
    gradual_move(left_motor_pin, min_pulse_width)
    gradual_move(right_motor_pin, min_pulse_width)

# Topların merkezi hesaplamaları
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def find_mid_way(center1, center2):
    mid_x = (center1[0] + center2[0]) // 2
    mid_y = (center1[1] + center2[1]) // 2
    return (mid_x, mid_y)

def drive_boat(mid_way, orjin, turn_left, turn_right, go_straight):
    cv2.circle(mid_way , orjin , 10 , (255, 0 ,255) , -1)
    mid_way_x , mid_way_y = mid_way

    if mid_way_x < orjin[0]-20:
        turn_right()
    elif mid_way_x > orjin[0]+20:
        turn_left()
    else:
        go_straight()
