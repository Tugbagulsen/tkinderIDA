import cv2
import numpy as np
import time


# Görüntünün alt çeyrek kısmında mor tespit eder
#0 ve ya 1 dondurerek kontrolun ihaya gecmesini kontrol eder
def detect_purple_in_lower_quarter_ver1(frame):
    # Görüntünün boyutlarını al
    height, width, _ = frame.shape
    
    # Görüntünün alt çeyrek kısmını al
    lower_quarter = frame[int(3*height/4):, :]
    
    # Görüntüyü HSV renk uzayına dönüştür
    hsv = cv2.cvtColor(lower_quarter, cv2.COLOR_BGR2HSV)
    
    # Mor (RAL 4008) rengini tespit etmek için HSV aralığı
    lower_purple = np.array([140, 50, 50])
    upper_purple = np.array([160, 255, 255])
    
    # Mor renk maskesi oluştur
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    
    # Mor piksel sayısını hesapla
    purple_pixel_count = cv2.countNonZero(mask)
    
    # Belirli bir değeri geçerse 1, aksi halde 0 döndür
    threshold = 500  # Bu değeri ihtiyacınıza göre ayarlayabilirsiniz
    if purple_pixel_count > threshold:
        return 1
    else:
        return 0





# Görüntünün alt çeyrek kısmında mor alanı olcer
def detect_purple_in_lower_quarter_ver2(frame):
    # Görüntünün boyutlarını al
    height, width, _ = frame.shape
    
    # Görüntünün alt çeyrek kısmını al
    lower_quarter = frame[int(3*height/4):, :]
    
    # Görüntüyü HSV renk uzayına dönüştür
    hsv = cv2.cvtColor(lower_quarter, cv2.COLOR_BGR2HSV)
    
    # Mor (RAL 4008) rengini tespit etmek için HSV aralığı
    lower_purple = np.array([140, 50, 50])
    upper_purple = np.array([160, 255, 255])
    
    # Mor renk maskesi oluştur
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    
    # Mor piksel sayısını hesapla
    purple_pixel_count = cv2.countNonZero(mask)
    
    # Mor piksel sayısını döndür
    return purple_pixel_count
# olculen mor alanın 3 sn icindekini degisimine gore controlu duzenler
def check_purple_trend(cap):
    results = []
    
    for _ in range(3):
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame")
            return 0
        
        purple_pixel_count = detect_purple_in_lower_quarter_ver2(frame)
        results.append(purple_pixel_count)
        
        time.sleep(1)  # 1 saniye bekle
    
    # Sonuçların sürekli artıp artmadığını kontrol et
    if results[0] < results[1] < results[2]:
        return 1
    else:
        return 0

