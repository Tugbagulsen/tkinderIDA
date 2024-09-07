"""
import cv2
import pytesseract

# Tesseract'a giden yolu belirt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def rakam_ve_konum_oku(goruntu):
    # Görüntünün genişliğini ve yüksekliğini al
    yukseklik, genislik = goruntu.shape[:2]
    
    # Sağdan ve soldan %15 oranında kesme
    sol_kesim = int(genislik * 0.07)
    sag_kesim = int(genislik * 0.92)
    
    # Görüntüyü kırp
    kirpilmis_goruntu = goruntu[:, sol_kesim:sag_kesim]
    
    # Görüntüyü griye çevir
    gri = cv2.cvtColor(kirpilmis_goruntu, cv2.COLOR_BGR2GRAY)
    
    # Gürültüyü azaltmak için bulanıklaştırma
    gri = cv2.medianBlur(gri, 5)
    
    # Tesseract ile OCR yaparak verileri elde et
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=123'
    veri = pytesseract.image_to_data(gri, config=custom_config, output_type=pytesseract.Output.DICT)
    
    # Rakamlar için ayrı listeler
    birler = []
    ikiler = []
    ucler = []
    
    # Veriler arasında gezinerek sayıları ve konumlarını al
    for i in range(len(veri['text'])):
        if veri['text'][i] in ['1', '2', '3']:
            x = veri['left'][i] + sol_kesim  # Kırpılmış görüntüdeki x koordinatını orijinal görüntüye göre ayarla
            y = veri['top'][i]
            if veri['text'][i] == '1':
                birler.append((x, y))
            elif veri['text'][i] == '2':
                ikiler.append((x, y))
            elif veri['text'][i] == '3':
                ucler.append((x, y))
    
    # Konumları string olarak döndür
    konumlar_sözlüğü = {
        '1': [f"({x}, {y})" for (x, y) in birler],
        '2': [f"({x}, {y})" for (x, y) in ikiler],
        '3': [f"({x}, {y})" for (x, y) in ucler]
    }
    
    return konumlar_sözlüğü

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Görüntüdeki 1, 2 ve 3 rakamlarını ve konumlarını oku
        konumlar_sözlüğü = rakam_ve_konum_oku(frame)
        
        # Tespit edilen rakamların etrafına dikdörtgen çiz ve rakamı ekrana yazdır
        for rakam, konumlar in konumlar_sözlüğü.items():
            for konum in konumlar:
                x, y = map(int, konum.strip('()').split(', '))
                cv2.rectangle(frame, (x, y), (x + 10, y + 10), (0, 255, 0), 2)  # Genişlik ve yüksekliği basitçe 10 olarak ayarladık
                cv2.putText(frame, rakam, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                print(f"Rakam: {rakam}, Konum: ({x}, {y})")

        # Görüntüyü ekranda göster
        cv2.imshow('Kamera', frame)

        # Çıkmak için 'q' tuşuna basın
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kaynakları serbest bırak
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
"""

import cv2
import pytesseract
import numpy as np
import threading
import time

# Tesseract kurulumunu yapıldığını varsayarak
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global değişkenler
son_islem_zamani = time.time()
thread_hala_calisiyor = False
orta_nokta2 = None

def rakam_ve_konum_oku(frame):
    global thread_hala_calisiyor, orta_nokta2
    gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gri, (3, 3), 0)
    edges = cv2.Canny(blur, 75, 200)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if 30 < w < 200 and 30 < h < 200:
            roi = gri[y:y + h, x:x + w]

            config = "--psm 6 outputbase digits"
            text = pytesseract.image_to_string(roi, config=config).strip()

            if '2' in text:
                orta_nokta2 = (x + w // 2, y + h // 2)
                thread_hala_calisiyor = False
                return

    orta_nokta2 = None
    thread_hala_calisiyor = False

def process_frame(frame, noktalar):
    # Çerçevede işleme ve çizim yapma işlemlerini burada gerçekleştir
    for nokta in noktalar:
        cv2.circle(frame, nokta, 5, (0, 255, 0), -1)
    return frame

def main():
    global son_islem_zamani, thread_hala_calisiyor, orta_nokta2

    cap = cv2.VideoCapture(0)
    fps_bekleme_suresi = 0.1  # OCR işlemini her 0.1 saniyede bir çalıştırmak için

    frame_count = 0
    while True:
        ret, goruntu = cap.read()
        if not ret:
            break
        
        goruntu = cv2.resize(goruntu, (320, 240))

        # Zaman tabanlı OCR işlemi - her 0.1 saniyede bir
        suanki_zaman = time.time()
        if suanki_zaman - son_islem_zamani >= fps_bekleme_suresi and not thread_hala_calisiyor:
            thread_hala_calisiyor = True
            son_islem_zamani = suanki_zaman
            thread = threading.Thread(target=rakam_ve_konum_oku, args=(goruntu,))
            thread.start()

        # Önceki tespit edilen '2' sayısının sonuçlarını çiz
        if orta_nokta2 is not None:
            x, y = orta_nokta2
            cv2.circle(goruntu, (x, y), 5, (0, 255, 0), -1)

        # Her belirli frame aralığında çizim işlemi yapılır
        if frame_count % int(1 / fps_bekleme_suresi) == 0:
            # Çizim noktaları listesi oluştur
            noktalar = []
            if orta_nokta2 is not None:
                noktalar.append(orta_nokta2)

            # Görüntüyü işleme ve çizme işlemi
            goruntu = process_frame(goruntu, noktalar)

        frame_count += 1
        cv2.imshow('Tanımlanan Sayı', goruntu)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()