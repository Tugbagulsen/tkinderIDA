# Bazı yorum satırları sanal üzerinden test edilebilmesi üzere inaktif edilmiştir.
# Gemi de çalıştırılması için  ball dosyasındaki yorum satırlarının aktif edilmesi  gerekmektedir.
# ilgili satırlar dosya basında belirtilmistir
# Eğer gemi herhangi bir top göremezse düz gideceği için topları gördükten sonra düz gitmeye devam edecektir
# Geminin durması için q tuşuna basılması gerekmektedir.



import cv2
from ball import *
from datetime import datetime
import time
import keyboard

def start():
    # Kamera başlatma
    cap = cv2.VideoCapture(0)  # Kamera başlatma
    
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return
    
    # Tarih ve saat bilgisini alma video ismi için
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    #videoyu kaydetme
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_filename = f"Akriha_Control_{now}.avi"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))
    
    while cap.isOpened:
        ret , frame = cap.read()
        
        if not ret:
            print("Error: Unable to read frame")
            break

        # ASIL SURUS FONKSIYONU
        drive_boat(ret, frame)
        
        # Videoyu kaydetme
        out.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        cv2.imshow('Frame', frame)


def main():
    start()

       
    
if __name__ == '__main__':
    main()
