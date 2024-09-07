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
            w = veri['width'][i]
            h = veri['height'][i]
            if veri['text'][i] == '1':
                birler.append((x, y, w, h))
            elif veri['text'][i] == '2':
                ikiler.append((x, y, w, h))
            elif veri['text'][i] == '3':
                ucler.append((x, y, w, h))
    
    return birler, ikiler, ucler

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Görüntüdeki 1, 2 ve 3 rakamlarını ve konumlarını oku
        birler, ikiler, ucler = rakam_ve_konum_oku(frame)
        
        # Tespit edilen rakamların etrafına dikdörtgen çiz ve rakamı ekrana yazdır
        for (x, y, w, h) in birler:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, '1', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print(f"Rakam: 1, Konum: ({x}, {y})")
        
        for (x, y, w, h) in ikiler:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, '2', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print(f"Rakam: 2, Konum: ({x}, {y})")
        
        for (x, y, w, h) in ucler:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, '3', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print(f"Rakam: 3, Konum: ({x}, {y})")

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
