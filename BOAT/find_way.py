import cv2
import numpy as np
import time
import pigpio
import keyboard

# Motorların bağlı olduğu GPIO pinleri
left_motor_pin = 17
right_motor_pin = 18

# PWM genişlikleri
min_pulse_width = 1000
max_pulse_width = 2000

# pigpio instance
pi = pigpio.pi()

def gradual_move(pin, target_pulse_width, step_size=10, step_delay=0.01):
    current_pulse_width = pi.get_servo_pulsewidth(pin)
    step = step_size if target_pulse_width > current_pulse_width else -step_size

    for pulse_width in range(current_pulse_width, target_pulse_width, step):
        pi.set_servo_pulsewidth(pin, pulse_width)
        time.sleep(step_delay)
    
    pi.set_servo_pulsewidth(pin, target_pulse_width)

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
    pi.set_servo_pulsewidth(left_motor_pin, 0)
    pi.set_servo_pulsewidth(right_motor_pin, 0)

def drive_direction(mid_way, orjin):
    if mid_way[0] < orjin[0] - 50:
        print("sol")
        turn_left()
    elif mid_way[0] > orjin[0] + 50:
        print("sağ")
        turn_right()
    else:
        print("düz")
        go_straight()

# Max area of a color to be considered as detected
color_limit = 123

def find_center_of_counters(mask, color, frame):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(max_contour)
        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
        else:
            cX, cY = 0, 0  # Default value if division by zero would occur
        max_area = cv2.contourArea(max_contour)
        x, y, w, h = cv2.boundingRect(max_contour)
        if max_area > color_limit:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            return max_area, mask[y:y + h, x:x + w].sum() // 255, (cX, cY)
        else:
            return 0, 0, (0, 0)
    else:
        return 0, 0, (0, 0)  # Return 0 area and pixel count if no contours are found

def find_mid_way(center1, center2):
    mid_x = (center1[0] + center2[0]) // 2
    mid_y = (center1[1] + center2[1]) // 2
    return (mid_x, mid_y)

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def check_balls(red_center, green_center, yellow_center, orjin):
    orjin_x_range = range(orjin[0] - 310, orjin[0] + 310)
    
    red_in_range = red_center[0] in orjin_x_range
    green_in_range = green_center[0] in orjin_x_range
    yellow_in_range = yellow_center[0] in orjin_x_range
    warning_txt = "Cant see"
    ball_counter = 0
    if red_in_range:
        warning_txt = "kirmizi gorunuyor "
        ball_counter += 1
    if green_in_range:
        warning_txt += "yesil gozukuyor "
        ball_counter += 1
    if yellow_in_range:
        warning_txt += "sari gorunuyor "
        ball_counter += 1
    return ball_counter

def find_widest_distance(red_center, green_center, yellow_center):
    if red_center != (0, 0) and yellow_center != (0, 0):
        dist_red_yellow = calculate_distance(red_center, yellow_center)
    else:
        dist_red_yellow = 0
    
    if green_center != (0, 0) and yellow_center != (0, 0):
        dist_green_yellow = calculate_distance(green_center, yellow_center)
    else:
        dist_green_yellow = 0

    if green_center != (0, 0) and red_center != (0, 0):
        dist_green_red = calculate_distance(green_center, red_center)
    else:
        dist_green_red = 0
    return dist_red_yellow, dist_green_yellow, dist_green_red

def find_ways(red_center, green_center, yellow_center, orjin, frame, dist_red_yellow, dist_green_yellow, dist_green_red):
    ball_count = check_balls(red_center, green_center, yellow_center, orjin)
    if ball_count >= 2:
        mid_way = (0, 0)
        if yellow_center != (0, 0) and (red_center != (0, 0) or green_center != (0, 0)):
            if dist_red_yellow > dist_green_yellow:
                mid_way = find_mid_way(red_center, yellow_center)
            else:
                mid_way = find_mid_way(green_center, yellow_center)
        elif red_center != (0, 0) and green_center != (0, 0):
            mid_way = find_mid_way(green_center, red_center)
        else:
            mid_way = (0, 0)
        if mid_way != (0, 0):
            cv2.circle(frame, mid_way, 10, (255, 0, 255), -1)
    else:
        mid_way = (0, 0)
    return mid_way

def drive_boat(ret , frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # RENKLER ICIN MAKSELER
    
    # Kırmızı renk için maske
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)

    # Yeşil renk için maske
    lower_green = np.array([36, 100, 100])
    upper_green = np.array([86, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Sarı renk için maske
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    orjin = (322, 240)  # Kameranın merkezi
 

    red_output = cv2.bitwise_and(frame, frame, mask=mask_red)
    green_output = cv2.bitwise_and(frame, frame, mask=mask_green)
    yellow_output = cv2.bitwise_and(frame, frame, mask=mask_yellow)

    max_red_area, red_pixels, red_center = find_center_of_counters(mask_red, (0, 0, 255), frame)
    max_green_area, green_pixels, green_center = find_center_of_counters(mask_green, (0, 255, 0), frame)
    max_yellow_area, yellow_pixels, yellow_center = find_center_of_counters(mask_yellow, (0, 255, 255), frame)

    dist_red_yellow, dist_green_yellow, dist_green_red = find_widest_distance(red_center, green_center, yellow_center)

    mid_way = find_ways(red_center, green_center, yellow_center, orjin, frame, dist_red_yellow, dist_green_yellow, dist_green_red)

    # Yönlendirme komutlarını çağır
    if mid_way != (0, 0):
        drive_direction(mid_way, orjin)
    else:
        go_straight()
        ...
   
def main():
    ...

if __name__ == '__main__':
    main()