"""
import cv2
import numpy as np
from triangle_detection import detect_triangle  # import

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Üçgen algılama
    frame, triangle_center, triangle_detected = detect_triangle(frame)
    
    
    frame = cv2.resize(frame, (640, 480))  # Çözünürlüğü 640x480 olarak ayarla

    # OCR işlemini her karede yap
    tesseract4.rakam_ve_konum_oku(frame)  # Sadece 'frame' gönderilir

    # OCR sonucu 'orta_nokta2' değişkenini kontrol edin
    global orta_nokta2
    print(f"Orta Nokta 2: {orta_nokta2}")

    # Gemi ortalama hesapla (örneğin red_center ve green_center)
    orta_yol = find_mid_way(red_center, green_center)

    # Triangle_center kontrol
    x_red, y_red = triangle_center
    print(f"Triangle Center: {triangle_center}")

    # Çizim işlemleri ve koordinatlar
    y_nokta = y_red - 100
    nokta_koordinat = (x_red, y_nokta)
    cv2.circle(frame, nokta_koordinat, 5, (0, 255, 0), -1)

    # Görüntüyü işleme
    frame = process_frame(frame, nokta_koordinat)

    # X ekseni başlangıç noktaları
    x_ekseni_baslangic = (x_red, y_nokta)
    x_ekseni_bitis = (frame.shape[1] - 1, y_nokta)
    orta_nokta = (x_red, y_nokta)

    if orta_nokta2:
        x_ekseni_bitis = orta_nokta2
        x_orta = (x_red + x_ekseni_bitis[0]) // 2
        y_orta = y_nokta
        orta_nokta = (x_orta, y_orta)

        # Çizim işlemleri
        cv2.line(frame, x_ekseni_baslangic, orta_nokta, (0, 0, 0), 1)
        cv2.line(frame, orta_nokta, x_ekseni_bitis, (0, 0, 0), 1)
        cv2.circle(frame, orta_nokta, 5, (255, 0, 0), -1)

    # Görüntü işleme sonrası
    frame = process_frame(frame, nokta_koordinat)



    # Görüntüyü göster
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import LabelFrame, messagebox
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
from tkinderIDA.trials.checkpoint_muhammed import process_frame
import tkinderIDA.trials.tesseract as tesseract
from tkinderIDA.Master.IHA.IHA_Muhamemed import ilk_nokta, ikinci_nokta
# Tkinter ana penceresi
master = tk.Tk()

# Başlangıç penceresi boyutları
canvas_genislik = 1000
canvas_yukseklik = 450
panel_genislik = 150
panel_yukseklik = 250
panel_margin = 10
top_margin = 20

# Tkinter ana penceresi
master.title("Kamera ve Veri Okuma Uygulamasi")

# Kanvas oluşturma
canvas = tk.Canvas(master, width=canvas_genislik, height=canvas_yukseklik)
canvas.pack()

def label_frame_olusturma(master, text, relx, rely, relwidth, relheight):
    label_frame = LabelFrame(master, text=text)
    label_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return label_frame

# Veri Paneli (Kamera görüntüsü burada olacak)
label_frame_veri = label_frame_olusturma(master, "Veri", 0.04, top_margin / canvas_yukseklik, 0.5, 0.65)

# Araç Paneli (başka bir örnek için)
label_frame_arac = label_frame_olusturma(master, "Araç", 0.6, 0.04, 0.34, 0.1)
label_arac = tk.Label(label_frame_arac, text="arac ismi icin simdilik bos birakilmistir")
label_arac.pack(padx=15, pady=5, anchor=tk.NW)

# Sonuç Paneli (veriler burada gösterilecek)
label_frame_sonuc = label_frame_olusturma(master, "Sonuç", 0.6, 0.2, 0.35, 0.5)

# Fonksiyon Paneli
label_frame_fonksiyon = label_frame_olusturma(master, "Fonksiyon", 0.6, 0.6, 0.35, 0.3)

# Kamera açma butonu
def btnCamera():
    start_video_capture()

# Diğer buton fonksiyonları    
def btnBatma():
    messagebox.showinfo("Bilgi", "Batma butonuna tikandi")    
def btnCikma():
    messagebox.showinfo("Bilgi", "Çıkma butonuna tıklandı")

def btnSag():
    messagebox.showinfo("Bilgi", "Sağ butonuna tıklandı")

def btnSol():
    messagebox.showinfo("Bilgi", "Sol butonuna tıklandı")

def btnIleri():
    messagebox.showinfo("Bilgi", "İleri butonuna tıklandı")

def btnGeri():
    messagebox.showinfo("Bilgi", "Geri butonuna tıklandı")

def btnReset():
    messagebox.showinfo("Bilgi", "Reset butonuna tıklandı")

def btnArm():
    messagebox.showinfo("Bilgi", "Arm butonuna tıklandı")

def btnDisarm():
    messagebox.showinfo("Bilgi", "Disarm butonuna tıklandı")

def btnStabilize():
    messagebox.showinfo("Bilgi", "Stabilize butonuna tıklandı")

def btnAuto():
    messagebox.showinfo("Bilgi", "Auto butonuna tıklandı")

# Butonları yerleştirme
buton_metinleri = ["Batma", "Çıkma", "Sağ", "Sol", "İleri", "Geri", "Kamera", "Reset", "Arm", "Disarm", "Stabilize", "Auto"]
buton_fonksiyonlari = [btnBatma, btnCikma, btnSag, btnSol, btnIleri, btnGeri, btnCamera, btnReset, btnArm, btnDisarm, btnStabilize, btnAuto]

for i, metin in enumerate(buton_metinleri):
    row, column = divmod(i, 2)
    buton = tk.Button(label_frame_fonksiyon, text=metin, width=10, height=1, background='White', command=buton_fonksiyonlari[i])
    buton.grid(row=row, column=column, padx=40, pady=3)

# Sonuç paneline veri yazdırmak için fonksiyon
def update_sonuc_panel(text):
    for widget in label_frame_sonuc.winfo_children():
        widget.destroy()
    label = tk.Label(label_frame_sonuc, text=text)
    label.pack()


def find_mid_of_counters(mask, color, frame):
    # Apply Gaussian Blur to the mask to reduce noise
    blurred_mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Find contours in the blurred mask
    contours, _ = cv2.findContours(blurred_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(max_contour)
        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
        else:
            cX, cY = 0, 0  # Default value if division by zero would occur
        max_area = cv2.contourArea(max_contour)
        x, y, w, h = cv2.boundingRect(max_contour)
        if max_area > 500:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            return max_area, mask[y:y + h, x:x + w].sum() // 255, (cX, cY)
        else:
            return 0, 0, (0, 0)
    else:
        return 0, 0, (0, 0)  # Return 0 area and pixel count if no contours are found

def find_mid_way(center1, center2):
    mid_x = (center1[0] + center2[0]) // 2
    mid_y = (center1[1] + center2[1]) // 2
    return (mid_x, mid_y)

orta_nokta2 = None
    

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Video akışını başlatacak fonksiyon
def start_video_capture():
    label_veri = tk.Label(label_frame_veri)
    label_veri.pack()

         
                

    def video_thread():
        global orta_nokta2
        
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Hata", "Kamera bulunamadi veya acilamadi!")
            return

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_filename = f"Akriha_Control_{now}.avi"
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))

        # sonuc = {"x": None, "y": None, "w": None, "h": None, "orta_nokta2": None}
        # frame_count = 0
        # fps_bekleme_suresi = 20  # OCR işlemini her 5 frame'de bir çalıştır

        while cap.isOpened():
            
            ret, frame = cap.read()
            
            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # Kırmızı renk için maske
                lower_red1 = np.array([0, 100, 100])
                upper_red1 = np.array([10, 255, 255])
                mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
                lower_red2 = np.array([160, 100, 100])
                upper_red2 = np.array([180, 255, 255])
                mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
                mask_red = mask_red1 + mask_red2

                # Yeşil renk için maske
                lower_green = np.array([36, 100, 100])
                upper_green = np.array([86, 255, 255])
                mask_green = cv2.inRange(hsv, lower_green, upper_green)

                # Sarı renk için maske
                lower_yellow = np.array([20, 100, 100])
                upper_yellow = np.array([30, 255, 255])
                mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
                
                # turuncu için maske
                lower_orange = np.array([10, 100, 100])
                upper_orange = np.array([25, 255, 255])
                mask_orange=cv2.inRange(hsv,lower_orange,upper_orange)

                # beyaz renk için maske
                
                lower_black = np.array([130, 50, 50])
                upper_black = np.array([160, 255, 255])
                mask_black = cv2.inRange(hsv, lower_black, upper_black)




                red_output = cv2.bitwise_and(frame, frame, mask=mask_red)
                green_output = cv2.bitwise_and(frame, frame, mask=mask_green)
                yellow_output = cv2.bitwise_and(frame, frame, mask=mask_yellow)
                black_output= cv2.bitwise_and(frame,frame,mask=mask_black)



                max_red_area, red_pixels, red_center = find_mid_of_counters(mask_red, (0, 0, 255), frame)
                max_green_area, green_pixels, green_center = find_mid_of_counters(mask_green, (0, 255, 0), frame)
                max_yellow_area, yellow_pixels, yellow_center = find_mid_of_counters(mask_yellow, (0, 255, 255), frame)
                max_black_area,black_pixels,black_center= find_mid_of_counters(mask_black,(0,0,0),frame)
               

                mask_combined = cv2.bitwise_or(mask_red, cv2.bitwise_or(mask_yellow, mask_orange))


                # Sarı ile kırmızı ve sarı ile yeşil arasındaki mesafeleri hesapla
                if red_center != (0, 0) and yellow_center != (0, 0):
                    dist_red_yellow = calculate_distance(red_center, yellow_center)
                else:
                    dist_red_yellow = 0
                
                # alttaki 4 satır gemi kendini ortalaması için  yapıldı
                if green_center != (0, 0) and red_center != (0, 0):
                    dist_green_red = calculate_distance(green_center, red_center)
                else:
                    dist_green_red = 0

                if green_center != (0, 0) and yellow_center != (0, 0):
                    dist_green_yellow = calculate_distance(green_center, yellow_center)
                else:
                    dist_green_yellow = 0

                # En uzun mesafeyi bul ve orta noktaya mor yuvarlak çiz
                if dist_red_yellow > dist_green_yellow:
                    mid_way = find_mid_way(red_center, yellow_center)
                else:
                    mid_way = find_mid_way(green_center, yellow_center)
                
                if mid_way != (0, 0):  # Eğer geçerli bir orta nokta varsa
                    cv2.circle(frame, mid_way, 10, (255, 0, 255), -1)
                  # Tesseract4'ten orta noktayı almak için fonksiyonu çağır


                frame = cv2.resize(frame, (640, 480))  # Çözünürlüğü 640x480 olarak ayarla

                # OCR işlemini her karede yap
                tesseract4.rakam_ve_konum_oku(frame)  # Sadece 'frame' gönderilir

                # OCR sonucu 'orta_nokta2' değişkenini kontrol edin
                global orta_nokta2
                print(f"Orta Nokta 2: {orta_nokta2}")

                # Gemi ortalama hesapla (örneğin red_center ve green_center)
                orta_yol = find_mid_way(red_center, green_center)

                # Triangle_center kontrol
                frame, triangle_center, triangle_detected = detect_triangle(frame)
                print(f"Triangle Center: {triangle_center}")

                # Çizim işlemleri ve koordinatlar
                # y_nokta = y_red - 100
                # nokta_koordinat = (x_red, y_nokta)
                ilk_nokta=nokta_koordinat
                cv2.circle(frame, nokta_koordinat, 5, (0, 255, 0), -1)
                
                # Görüntüyü işleme
                frame = process_frame(frame, ilk_nokta)

                # X ekseni başlangıç noktaları
                x_ekseni_baslangic = (x_red, y_nokta)
                x_ekseni_bitis = (frame.shape[1] - 1, y_nokta)
                orta_nokta = (x_red, y_nokta)

                if orta_nokta2 is not None:
                    # X ekseni başlangıç ve bitiş noktaları
                    orta_nokta = ((ilk_nokta[0] + orta_nokta2[0]) // 2, y_nokta)
                    x_ekseni_bitis = orta_nokta2

                    # Çizim işlemleri
                    cv2.line(frame, ilk_nokta, ikinci_nokta, (0, 0, 0), 1)
                    cv2.line(frame, ikinci_nokta, orta_nokta, (0, 0, 0), 1)
                    cv2.line(frame, orta_nokta, x_ekseni_bitis, (0, 0, 0), 1)

                    # Noktaların üzerine daireler çizilir
                    cv2.circle(frame, ilk_nokta, 5, (255, 0, 0), -1)
                    cv2.circle(frame, ikinci_nokta, 5, (255, 0, 0), -1)
                    cv2.circle(frame, orta_nokta, 5, (255, 0, 0), -1)
                    cv2.circle(frame, x_ekseni_bitis, 5, (255, 0, 0), -1)
                else:
                    print("orta_nokta2 tanımlı değil!")

                # Görüntü işleme sonrası
                frame = process_frame(frame, nokta_koordinat)

                if black_center != (0, 0):  
                    cv2.circle(frame,black_center, 10, (0, 0, 0), -1)
                
                # normalde x,y= orta_yol
                x,y=black_center
                a,b=mid_way

                def öneri2_fn(x_ekseni_baslangic, ikinci_nokta, orta_nokta, x_ekseni_bitis, nokta_koordinat):
                    x_gemi, y_gemi = nokta_koordinat  # Geminin merkez koordinatları

                    if gemi_uyarısı_metin == "gemiyi görüyorum":
                        # Gemi başlangıç ve ikinci nokta arasındaysa
                        if x_ekseni_baslangic[0] <= x_gemi <= ikinci_nokta[0]:
                            if y_gemi < ikinci_nokta[1] - 2:
                                öneri2_metin = "gemiyi sola kır (Başlangıç-İkinci Nokta)"
                                return "gemiyi sola kır (Başlangıç-İkinci Nokta)"
                            elif y_gemi > ikinci_nokta[1] + 2:
                                öneri2_metin = "gemiyi sağa kır (Başlangıç-İkinci Nokta)"
                                return "gemiyi sağa kır (Başlangıç-İkinci Nokta)"
                            else:
                                öneri2_metin = "dümdüz devam (Başlangıç-İkinci Nokta)"
                                return "dümdüz devam (Başlangıç-İkinci Nokta)"

                        # Gemi ikinci nokta ve orta nokta arasındaysa
                        elif ikinci_nokta[0] < x_gemi <= orta_nokta[0]:
                            if y_gemi < orta_nokta[1] - 2:
                                öneri2_metin = "gemiyi sola kır (İkinci Nokta-Orta)"
                                return "gemiyi sola kır (İkinci Nokta-Orta)"
                            elif y_gemi > orta_nokta[1] + 2:
                                öneri2_metin = "gemiyi sağa kır (İkinci Nokta-Orta)"
                                return "gemiyi sağa kır (İkinci Nokta-Orta)"
                            else:
                                öneri2_metin = "dümdüz devam (İkinci Nokta-Orta)"
                                return "dümdüz devam (İkinci Nokta-Orta)"

                        # Gemi orta nokta ve bitiş nokta arasındaysa
                        elif orta_nokta[0] < x_gemi <= x_ekseni_bitis[0]:
                            if y_gemi < x_ekseni_bitis[1] - 2:
                                öneri2_metin = "gemiyi sola kır (Orta-Bitiş)"
                                return "gemiyi sola kır (Orta-Bitiş)"
                            elif y_gemi > x_ekseni_bitis[1] + 2:
                                öneri2_metin = "gemiyi sağa kır (Orta-Bitiş)"
                                return "gemiyi sağa kır (Orta-Bitiş)"
                            else:
                                öneri2_metin = "dümdüz devam (Orta-Bitiş)"
                                return "dümdüz devam (Orta-Bitiş)"
                    else:
                        öneri2_metin = "gemi gözükmüyor"
                        return "gemi gözükmüyor"
                
                gemi_uyarısı_metin="birazdan gemi uyarısı geliyor..."
                öneri1_metin="birazdan öneri1 geliyor..."
                öneri2_metin="birazdan öneri2 geliyor..."
                # öneri3_metin="birazdan öneri3 geliyor..."
                
                gemi_uyarısı_metin= gemi_görüyor_fn(black_center,red_center,green_center,yellow_center,orjin,gemi_uyarısı_metin)
                # öneri1_metin= öneri1_fn(x,orjin)
                öneri2_metin= öneri2_fn(x_ekseni_baslangic, orta_nokta, x_ekseni_bitis, nokta_koordinat)
                # öneri3_metin =öneri3_fn(yellow_center,green_center,red_center,orjin,gemi_uyarısı_metin)
              
                   
                
                        
                        
                    
                        
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(img)

                def update_gui():
                    label_veri.imgtk = imgtk
                    label_veri.config(image=imgtk)
                    height, width, _ = frame.shape
                    update_sonuc_panel(f"Görüntü Boyutu: {width}x{height}\n{gemi_uyarısı_metin}\n{öneri2_metin}")

                master.after(0, update_gui)
                out.write(frame)

            else:
                break

            time.sleep(0.05)  # Görüntü güncellemeleri arasında küçük bir bekleme süresi

        cap.release()
        out.release()

    threading.Thread(target=video_thread, daemon=True).start()

# Tkinter ana döngüsü
master.mainloop()