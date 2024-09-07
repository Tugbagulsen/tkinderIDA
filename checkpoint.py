"""
import cv2
import numpy as np

# Checkpoint koordinatları
x_red, y_red = 150, 250  # Örnek başlangıç koordinatları
checkpoint_above_triangle = (x_red, y_red - 100)  # Kırmızı üçgenin yukarısındaki nokta

# Başlangıç durumu - kontrol gemi kamerasında
control_source = "boat"  # "boat" veya "drone" olabilir

# Minimum alan büyüklüğü (piksel cinsinden)
MIN_AREA = 1500  # Bu değeri beyaz teknenizin boyutuna göre ayarlayın

def distance(point1, point2):
    # İki nokta arasındaki mesafeyi hesapla
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def check_reached(current_position, target_position, threshold=20):
    # Hedefe ulaşılıp ulaşılmadığını kontrol et
    return distance(current_position, target_position) < threshold

def control_boat(current_position):
    global control_source
    
    # Checkpoint'e ulaşıldığında kontrol kaynağını değiştir
    if check_reached(current_position, checkpoint_above_triangle):
        print("Checkpoint'e ulaşıldı. Kontrol kaynağı drone'a değiştiriliyor.")
        control_source = "drone"
    
    # Geçerli kontrol kaynağına göre komut işle
    if control_source == "boat":
        process_boat_camera()
    elif control_source == "drone":
        process_drone_camera()

def process_boat_camera():
    # Geminin kamerasından gelen görüntü işleme ve kontrol fonksiyonu
    print("Geminin kamerasından gelen görüntü işleniyor...")

def process_drone_camera():
    # Drone'un kamerasından gelen görüntü işleme ve kontrol fonksiyonu
    print("Drone'un kamerasından gelen görüntü işleniyor...")

# Kamerayı başlat
cap = cv2.VideoCapture(0)

while True:
    # Kameradan bir kare al
    ret, frame = cap.read()
    if not ret:
        break

    # BGR'den HSV renk alanına dönüştür
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Beyaz renk için maske
    lower_white = np.array([0, 0, 168])
    upper_white = np.array([172, 111, 255])
    mask_white = cv2.inRange(hsv_frame, lower_white, upper_white)

    # Maske üzerinde konturları bul
    contours, _ = cv2.findContours(mask_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Konturun alanını hesapla
        area = cv2.contourArea(contour)
        
        # Alanı minimum alan büyüklüğünden büyük olanları işle
        if area > MIN_AREA:
            # Beyaz nesnenin merkezini bul
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                current_position = (cX, cY)

                # Checkpointlere ve nesneye daireler çiz
                cv2.circle(frame, checkpoint_above_triangle, 10, (0, 255, 0), -1)  # Checkpoint (yeşil daire)
                cv2.circle(frame, current_position, 10, (255, 0, 0), -1)  # Beyaz nesne (mavi daire)

                # Beyaz tekne çevresine yeşil çerçeve çiz
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Kontrol kaynağını güncelle
                control_boat(current_position)

    # Görüntüyü göster
    cv2.imshow("Geminin Kamerasi", frame)

    # 'q' tuşuna basıldığında döngüden çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
"""
# checkpoint.py
import cv2
import numpy as np

MIN_AREA = 1500  # Beyaz teknenizin boyutuna göre ayarlayın
control_source = "boat"  # Başlangıç durumu - kontrol gemi kamerasında

def distance(point1, point2):
    """İki nokta arasındaki mesafeyi hesaplar."""
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def check_reached(current_position, target_position, threshold=20):
    """Hedefe ulaşılıp ulaşılmadığını kontrol eder."""
    return distance(current_position, target_position) < threshold

def control_boat(current_position, nokta_kordinat):
    """Checkpoint'e ulaşıldığında kontrol kaynağını değiştirir."""
    global control_source
    
    # Checkpoint'e ulaşıldığında kontrol kaynağını değiştir
    if check_reached(current_position, nokta_kordinat):
        print("Checkpoint'e ulaşıldı. Kontrol kaynağı drone'a değiştiriliyor.")
        control_source = "drone"
    
    # Geçerli kontrol kaynağına göre komut işle
    if control_source == "boat":
        process_boat_camera()
    elif control_source == "drone":
        process_drone_camera()

def process_boat_camera():
    """Geminin kamerasından gelen görüntü işleme ve kontrol fonksiyonu."""
    print("Geminin kamerasından gelen görüntü işleniyor...")

def process_drone_camera():
    """Drone'un kamerasından gelen görüntü işleme ve kontrol fonksiyonu."""
    print("Drone'un kamerasından gelen görüntü işleniyor...")

def process_frame(frame, nokta_kordinat):
    """Kareyi işler ve checkpoint kontrolünü yapar."""
    global control_source
    
    # BGR'den HSV renk alanına dönüştür
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Beyaz renk için maske
    lower_white = np.array([0, 0, 168])
    upper_white = np.array([172, 111, 255])
    mask_white = cv2.inRange(hsv_frame, lower_white, upper_white)

    # Maske üzerinde konturları bul
    contours, _ = cv2.findContours(mask_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Konturun alanını hesapla
        area = cv2.contourArea(contour)
        
        # Alanı minimum alan büyüklüğünden büyük olanları işle
        if area > MIN_AREA:
            # Beyaz nesnenin merkezini bul
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                current_position = (cX, cY)

                # Checkpointlere ve nesneye daireler çiz
                cv2.circle(frame, nokta_kordinat, 10, (0, 255, 0), -1)  # Checkpoint (yeşil daire)
                cv2.circle(frame, current_position, 10, (255, 0, 0), -1)  # Beyaz nesne (mavi daire)

                # Beyaz tekne çevresine yeşil çerçeve çiz
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Kontrol kaynağını güncelle
                control_boat(current_position, nokta_kordinat)

    return frame
