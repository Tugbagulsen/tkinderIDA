import numpy as np
import cv2
import math

# Renk aralıkları (HSV) - Beyaz limanı tespit etmek için
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 30, 255])

# Drone başlangıç pozisyonu (orijin olarak kabul edilir)
drone_position = np.array([0, 0])

# Üçgenin başlangıç taban genişliği
base_width_start = 50  # Başlangıç taban genişliği ALINAN GORUNTUNUN OZELLİKLERİNE GORE DEGİSTİRİLECEK
height = 50  # Drone’un yükseklikle ilgisi yok ama sabit bir hareket mesafesi

# Açının tanımlanması (derece cinsinden)
angle = 45  # Drone’un tarama yapacağı açı İLERDE DEGİSTİRİLECEK

def detect_white_area(frame):
    """Beyaz alanı tespit eden fonksiyon."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    return np.any(mask)  # Beyaz var mı?

def calculate_horizontal_distance(vertical_distance, angle):
    """Verilen dikey mesafe ve açıya göre yatay mesafeyi hesapla."""
    return vertical_distance * math.tan(math.radians(angle))

def scan_area(drone_pos, step_size, base_width_start, height, angle, frame):
    """Drone'un tarama işlemi."""
    iter_count = 0

    while True:
        iter_count += 1

        # Şu ana kadar dikeyde kat edilen mesafe
        vertical_distance = iter_count * height
        
        # Dinamik taban genişliği hesaplama
        base_width = base_width_start + 2 * vertical_distance  # Dinamik taban genişliği
        horizontal_distance = calculate_horizontal_distance(vertical_distance, angle)
        
        # Yatay mesafe üçgenin taban genişliğiyle sınırlı olmalı
        if horizontal_distance > base_width / 2:
            horizontal_distance = base_width / 2
        
        # Yatay tarama yap
        for i in range(int(-horizontal_distance), int(horizontal_distance) + 1, step_size):
            scan_pos = drone_pos + np.array([i, 0])
            
            # Beyaz liman olup olmadığını kontrol et
            if detect_white_area(frame):
                return iter_count, scan_pos  # Liman bulundu
        
        # İleri hareket et
        drone_pos[1] += height
        
        # Eğer taban genişliği alanının dışına çıkıyorsa, döngüyü kır
        if abs(drone_pos[1]) > base_width_start + 2 * vertical_distance:
            break

    return iter_count, drone_pos

# Kamera ile görüntü yakalama (Raspberry Pi Camera Module veya USB kamera)
cap = cv2.VideoCapture(0)

# Tarama adım boyutu
step_size = 10

while True:
    ret, frame = cap.read()
    if not ret:
        break

    iter_count, final_pos = scan_area(drone_position, step_size, base_width_start, height, angle, frame)
    
    if iter_count > 0:
        print(f"Liman bulundu! İterasyon sayısı: {iter_count}, Son pozisyon: {final_pos}")
        break

    # Çıkış için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakma
cap.release()
cv2.destroyAllWindows()
