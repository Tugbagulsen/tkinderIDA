import cv2
import numpy as np
from datetime import datetime
import time
import math

from dedect_digit import *
# PIGPIO
"""
# Motorların bağlı olduğu GPIO pinleri
left_motor_pin = 17
right_motor_pin = 18

# PWM genişlikleri
min_pulse_width = 1000
max_pulse_width = 2000

# pigpio instance
#pi = pigpio.pi()

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

"""

def calculate_angle(pt1, pt2, pt3):
    # pt2 köşe noktası olarak kabul ediliyor
    a = np.array(pt1) - np.array(pt2)
    b = np.array(pt3) - np.array(pt2)
    cos_theta = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    angle = np.degrees(np.arccos(cos_theta))
    return angle

def detect_triangle(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Kırmızı renk aralıkları
    lower_red1 = np.array([0, 70, 70])
    upper_red1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    lower_red2 = np.array([160, 70, 70])
    upper_red2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = mask_red1 + mask_red2

    # Sarı renk aralıkları
    lower_yellow = np.array([15, 70, 70])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Turuncu renk aralıkları
    lower_orange = np.array([5, 70, 70])
    upper_orange = np.array([30, 255, 255])
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    # Kırmızı, sarı ve turuncu maskelerini birleştir
    mask_combined = cv2.bitwise_or(mask_red, cv2.bitwise_or(mask_yellow, mask_orange))

    # Gürültüyü azaltmak için morfolojik işlemler
    kernel = np.ones((5, 5), np.uint8)
    mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel)
    mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_OPEN, kernel)

    triangle_detected = False
    triangle_center = (0, 0)  # Üçgenin merkezi için değişken

    # Kenarları belirlemek için Canny kenar algılama
    edges = cv2.Canny(mask_combined, 50, 150)

    # Konturları bulma
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Konturu yaklaştırma
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Eğer konturun üç köşesi varsa, bu bir üçgendir
        if len(approx) == 3:
            # Üçgenin alanını hesapla
            area = cv2.contourArea(contour)
            if 500 < area < 2000:  # Üçgen alanı filtrelemesi (örneğin 10 ile 10000 arasında)
                # Üçgenin iç açılarını hesapla
                pt1, pt2, pt3 = approx[0][0], approx[1][0], approx[2][0]
                angle1 = calculate_angle(pt1, pt2, pt3)
                angle2 = calculate_angle(pt2, pt3, pt1)
                angle3 = calculate_angle(pt3, pt1, pt2)

                # Eğer açıların her biri 20 ile 120 derece arasındaysa
                if 20 < angle1 < 70 and 20 < angle2 < 70 and 20 < angle3 < 70:
                    # Üçgeni çiz
                    cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)
                    triangle_detected = True
                    
                    # Kırmızı üçgenin ağırlık merkezini (centroid) hesapla
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        triangle_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    else:
                        triangle_center = (0, 0)

    return triangle_center, triangle_detected, pt1, pt2, pt3

def draw_points(frame, triangle_center, pt1, pt2, pt3, hedef_liman):
    if triangle_center == (0, 0):
        print("Üçgen algılanamadı!")
        return None
    
    # Sol alt köşe noktayı bulma
    sol_alt_kose = min([pt1, pt2, pt3], key=lambda x: (x[1],x[0]))  # X eksenine göre en soldaki noktayı bul

    # Sol alt köşenin hizasında 200 piksel aşağıya noktayı yerleştir
    hedef_1 = (sol_alt_kose[0], sol_alt_kose[1] + 200)
    cv2.circle(frame, hedef_1, 5, (255, 0, 0), -1)  # Yeni noktayı mavi çember ile göster
    
    # İkinci nokta: Ağırlık merkezinden 100 piksel yukarı ve 100 piksel sol kaydırılmış nokta
    hedef_2 = (sol_alt_kose[0] - 100, triangle_center[1] - 50)

    # İkinci noktayı çiz (mavi çember ile göster)
    cv2.circle(frame, hedef_2, 3, (255, 0, 0), -1)
    
    # Üçüncü nokta: hedef limanın x ekseninden 100 piksel solda ve y ekseninde aynı hizada
    hedef_3 = (hedef_liman[0] - 200, hedef_liman[1])

    cv2.circle(frame, hedef_3, 5, (255, 0, 0), -1)  # Üçüncü noktayı mavi çember ile göster
    
    # Dördüncü nokta limanın içinde artık sadece 10 piksel solda
    hedef_4 = (hedef_liman[0]-10 , hedef_liman[1])
    cv2.circle(frame, hedef_4, 5, (255, 0, 0), -1)  # Dördüncü noktayı mavi çember ile göster
    
    return hedef_1, hedef_2, hedef_3, hedef_4

def find_boat(frame):
    # Botun renginin algılanması
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Mor bot için maske
    lower_purple = np.array([125, 100, 100])
    upper_purple = np.array([150, 255, 255])
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
    
    # Botu dikdörtgene al
    contours, _ = cv2.findContours(mask_purple, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
            cv2.putText(frame, "Bot", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    
    # Find the center of the boat
    M = cv2.moments(mask_purple)
    if M["m00"] != 0:
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        cv2.circle(frame, (x, y), 5, (255, 0, 255), -1)
        cv2.putText(frame, "Center", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    
    return  x , y
 
def find_port(frame):
    # Beyaz limanın renginin algılanması
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Beyaz liman için maske
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    
    # Limanı dikdörtgene al
    contours, _ = cv2.findContours(mask_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            cv2.putText(frame, "Liman", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            return 1
    return 0
   
def mesafe_hesapla(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def yon_hesapla(coord1, coord2):
    delta_x = coord2[0] - coord1[0]
    delta_y = coord2[1] - coord1[1]
    return math.atan2(delta_y, delta_x)

def donus_acisi(frame, hedef_koord):
    baslangic_koord = []
    son_koord = []
    
    baslangic_koord = find_boat(frame)
    time.sleep(2)
    son_koord = find_boat(frame)


    baslangic_mesafe = mesafe_hesapla(baslangic_koord, hedef_koord)
    son_mesafe = mesafe_hesapla(son_koord, hedef_koord)
    
    if son_mesafe < baslangic_mesafe:
        return 0
    else:
        # Cismin mevcut yönü ve hedef yönü
        cisim_yonu = yon_hesapla(baslangic_koord, son_koord)
        hedef_yonu = yon_hesapla(baslangic_koord, hedef_koord)
        
        # Hedefe gitmek için saat yönünde dönmesi gereken açı (radyan cinsinden)
        aci_farki = hedef_yonu - cisim_yonu
        
        # Açıyı normalize etmek (0 ile 360 derece arasında)
        aci_farki = math.degrees(aci_farki)  # Açı farkını dereceye çevir
        
        if aci_farki < 0:
            aci_farki += 360
        
        return aci_farki
     
def drive_IHA(ret , frame, hedef_liman , position_check):
    
     # Görüntü geliyor mu kontrol et
    if not ret:
        print("Görüntü alınamadı!")
        return
    
 
    # Üçgeni algıla
    triangle_center, triangle_detected, pt1, pt2, pt3 = detect_triangle(frame)
    
    # Üçgen algılanamazsa geri dön
    if not triangle_detected:
        print("Turn right")
        print("Go straight")
        drive_IHA(ret, frame)

    # Hedef limanın koordinatları
    liman_hedefleri = dedect_digit()
    
    hedef_liman = liman_hedefleri[hedef_liman]
    # Hedefleri belirle
    hedefler = draw_points(frame, triangle_center, pt1, pt2, pt3, hedef_liman)
    
    # Hedefler arası çizgi çiz
    cv2.line(frame, hedefler[0], hedefler[1], (0, 0, 255), 2)
    cv2.line(frame, hedefler[1], hedefler[2], (0, 0, 255), 2)
    cv2.line(frame, hedefler[2], hedefler[3], (0, 0, 255), 2)
    if position_check<1:
        drive_to_point(frame, hedefler[1])
    elif position_check<2:
        drive_to_point(frame, hedefler[2])
    elif position_check<3:
        drive_to_point(frame, hedefler[3])
    elif position_check<4:
        print("Hedefe ulaşıldı")

def drive_to_point(frame, hedef_koord, position_check):
    
    # Açı farkı hesapla
    # Açı farkını kapatacak şekilde botu döndür
    # Botu düz götür
    
    aci_farki = donus_acisi(frame, hedef_koord)
    gemi_koord = find_boat(frame)
    if 350 > aci_farki > 10 and mesafe_hesapla(gemi_koord, hedef_koord) > 10:
        if aci_farki > 180:
            print(f"Turn right {aci_farki}")
        else:
            print(f"Turn left {aci_farki}")
    else:
        if mesafe_hesapla(gemi_koord, hedef_koord) > 10:
            print("Go straight")
            if mesafe_hesapla(gemi_koord,hedef_koord)<10:
                print("Hedefe ulaşıldı")
                position_check = position_check + 1
    
def start_iha_control(frame):
    metre_kare=200 # 1 metrekareyi goren piksel sayısı olculup guncellenicek
    sinir_alan=18*metre_kare
    b_x,b_y=find_boat(frame)
     # Belirli bir alanı kontrol etmek için bir maske oluştur
    mask = np.zeros(frame.shape[:2], dtype="uint8")
    cv2.circle(mask, (b_x, b_y), int(np.sqrt(sinir_alan / np.pi)), 255, -1)
    
    # Görüntüyü HSV renk uzayına dönüştür
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Sarı rengin HSV aralığını belirle
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    
    # Yeşil rengin HSV aralığını belirle
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([70, 255, 255])
    
    # Sarı, kırmızı ve yeşil renkleri tespit et
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    # Maskeleri belirli alan maskesi ile birleştir
    mask_yellow = cv2.bitwise_and(mask_yellow, mask_yellow, mask=mask)
    mask_green = cv2.bitwise_and(mask_green, mask_green, mask=mask)
    
    # Sarı, kırmızı ve yeşil alanların olup olmadığını kontrol et
    if cv2.countNonZero(mask_yellow)> 2 or  cv2.countNonZero(mask_green) > 2: # 2 yanılsamaya karsı hata payı bunu mutlaka kontrol edin
        return 0
    else:
        return 1

    

def main():
    ret = True
    frame = True
    drive_IHA(ret , frame)
    
if __name__ == "__main__":
    main()
    
