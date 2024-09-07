import cv2
import numpy as np
import math
import time
#BU DOSYADAKİ KODALAR GEMİNİN DOGRU YONE GİDİP GİTMEDİGİNİ BELİRLEMEK İCİN

#BU DOSYADAKİ KODLARLA DAHA SONRASINDA GEMİNİN HIZI BULUNABİLİR

def mesafe_hesapla(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def yon_hesapla(coord1, coord2):
    delta_x = coord2[0] - coord1[0]
    delta_y = coord2[1] - coord1[1]
    return math.atan2(delta_y, delta_x)

#GEMİNİN ANLIK KOORDİNATINI BULUR X VE Y KOORDİNATLARINI DÖNDÜRÜR
def gemi_koordinat_bul(frame):

    mor_alt = np.array([130, 50, 50])  # Alt sınır (H, S, V)
    mor_ust = np.array([160, 255, 255])  # Üst sınır (H, S, V)
    # Görüntüyü HSV renk uzayına çevir
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Mor renk için maske oluştur
    maske = cv2.inRange(hsv, mor_alt, mor_ust)
    
    # Mor cismi bulmak için maske üzerinde kontur işlemi
    konturlar, _ = cv2.findContours(maske, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for kontur in konturlar:
        alan = cv2.contourArea(kontur)
        if alan > 500:  # Çok küçük gürültüleri elemek için bir alan filtresi
            # Konturun etrafına bir dikdörtgen çiz
            x, y, w, h = cv2.boundingRect(kontur)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Mor cismin koordinatlarını yazdır
            merkez_x = x + w // 2
            merkez_y = y + h // 2
            cv2.putText(frame, f"Koordinatlar: ({merkez_x}, {merkez_y})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            return merkez_x, merkez_y
    
    return None, None  # Eğer cisim bulunamazsa None döndür

#5 SN ARALIKLA GEMİYİ KONTROL EDEREK HEDEF KOORDİNATA GİDİP GİTMEDİGİNİ KONTROL EDER
#HEDEF KOORDİNATA GİDİYORSA 0 DÖNDÜRÜR
#HEDEF KOORDİNATA GİTMİYORSA HEDEFE GİDEBİLMEK İCİN SAAT YONUNDE DONMESİ GEREKEN ACIYI DÖNDÜRÜR
def donus_acisi(frame, hedef_koord):

    baslangic_koord = []
    son_koord = []

    baslangic_koord = gemi_koordinat_bul(frame)
    time.sleep(5)
    son_koord = gemi_koordinat_bul(frame)


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

