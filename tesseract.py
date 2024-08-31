import cv2
import pytesseract
# pytesseract kurulumu yapılması lazım githubdan dosya indirilerek ve sistem değişkenlerine PATH ekleyerek yapılıyor
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def rakam_ve_konum_oku(goruntu):
    # Görüntüyü griye çevir
    gri = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)
    
    # Gürültüyü azaltmak için bulanıklaştırma
    gri = cv2.medianBlur(gri, 5)
    
    # Tesseract ile OCR yaparak verileri elde et
    config = "--psm 6 outputbase digits"
    veri = pytesseract.image_to_data(gri, config=config, output_type=pytesseract.Output.DICT)
    
    sayilar_konumlari = []
    
    # Veriler arasında gezinerek sayıları ve konumlarını al
    for i in range(len(veri['text'])):
        if veri['text'][i].isdigit():  # Eğer bir rakam ise
            x = veri['left'][i]
            y = veri['top'][i]
            w = veri['width'][i]
            h = veri['height'][i]
            sayi = veri['text'][i]
            sayilar_konumlari.append((sayi, x, y, w, h))
    
    return sayilar_konumlari

    """
    Kullanımı :
    rakam_oku(Tespit edilecek görüntü)
    config = "--psm 6 outputbase digits" parametresi ile sadece rakamları tespit eder.
    return = [(sayi, x, y, w, h)]
    array şeklinde aldığı için tüm görünen sayılara erişilebilir.
    """
    
def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Görüntüdeki rakamları ve konumlarını oku
        sayilar_konumlari = rakam_ve_konum_oku(frame)
        
        # Tespit edilen rakamların etrafına dikdörtgen çiz ve rakamı ekrana yazdır
        for (sayi, x, y, w, h) in sayilar_konumlari:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, sayi, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print(f"Rakam: {sayi}, Konum: ({x}, {y})")

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