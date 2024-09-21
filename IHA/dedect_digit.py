import cv2
import pytesseract

# Tesseract'a giden yolu belirt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def dedect_digit(ret, frame):
    # Görüntünün genişliğini ve yüksekliğini al
    if not ret:
        print("Görüntü okunamadı.")
        return
    
    yukseklik, genislik = frame.shape[:2]
    
    # Sağdan ve soldan %15 oranında kesme
    sol_kesim = int(genislik * 0.07)
    sag_kesim = int(genislik * 0.92)
    
    # Görüntüyü kırp
    kirpilmis_goruntu = frame[:, sol_kesim:sag_kesim]
    
    # Görüntüyü griye çevir
    gri = cv2.cvtColor(kirpilmis_goruntu, cv2.COLOR_BGR2GRAY)
    
    # Gürültüyü azaltmak için bulanıklaştırma
    gri = cv2.medianBlur(gri, 5)
    
    # Tesseract ile OCR yaparak verileri elde et
    custom_config = r'--oem 3 --psm 6 -l eng -c tessedit_char_whitelist=123'
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
    
    # Kameranın açılabilirliğini kontrol et
    if not cap.isOpened():
        print("Kamera açılamadı.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Görüntü okunamadı.")
            break

        # Görüntüdeki 1, 2 ve 3 rakamlarını ve konumlarını oku
        konumlar_sözlüğü = dedect_digit(ret, frame)
        
        # Tespit edilen rakamların etrafına dikdörtgen çiz ve rakamı ekrana yazdır
        for rakam, konumlar in konumlar_sözlüğü.items():
            for konum in konumlar:
                x, y = map(int, konum.strip('()').split(', '))
                cv2.rectangle(frame, (x, y), (x + 10, y + 10), (0, 255, 0), 2)  # Genişlik ve yüksekliği basitçe 10 olarak ayarladık
                cv2.putText(frame, rakam, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                print(f"Rakam: {rakam}, Konum: ({x}, {y})")

        # Pencere boyutlandırılabilir olsun
        cv2.namedWindow('Kamera', cv2.WINDOW_NORMAL)
        cv2.imshow('Kamera', frame)

        # Çıkmak için 'q' tuşuna basın
        if cv2.waitKey(10) & 0xFF == ord('q'):  # 10ms gecikme eklendi
            break

    # Kaynakları serbest bırak
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
