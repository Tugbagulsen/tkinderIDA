# ida3 teki boş yerleri sildim
import cv2
import numpy as np
import tkinter as tk
from tkinter import LabelFrame, messagebox
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime

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

# Color limit
color_limit = 123

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
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
        if max_area > color_limit:
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

    

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Video akışını başlatacak fonksiyon
def start_video_capture():
    label_veri = tk.Label(label_frame_veri)
    label_veri.pack()
    def video_thread():
        
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

        while cap.isOpened():
            
            ret, frame = cap.read()
            
            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                # Kırmızı renk için maske
                lower_red1 = np.array([0, 120, 70])
                upper_red1 = np.array([10, 255, 255])
                mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
                lower_red2 = np.array([170, 120, 70])
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
                
                red_output = cv2.bitwise_and(frame, frame, mask=mask_red)
                green_output = cv2.bitwise_and(frame, frame, mask=mask_green)
                yellow_output = cv2.bitwise_and(frame, frame, mask=mask_yellow)

                max_red_area, red_pixels, red_center = find_mid_of_counters(mask_red, (0, 0, 255), frame)
                max_green_area, green_pixels, green_center = find_mid_of_counters(mask_green, (0, 255, 0), frame)
                max_yellow_area, yellow_pixels, yellow_center = find_mid_of_counters(mask_yellow, (0, 255, 255), frame)
                
                if max_red_area > color_limit:
                    color_detected = f"Kirmizi: {red_pixels} piksel"
                elif max_green_area > color_limit:
                    color_detected = f"Yesil: {green_pixels} piksel"
                elif max_yellow_area > color_limit:
                    color_detected = f"Sari: {yellow_pixels} piksel"
                else:
                    color_detected = "Renk Yok"

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
                
                # kamera orjini
                orjin=(322,240)
                cv2.circle(frame,orjin,5,(0,0,0),-1)
        
                a,b=mid_way
                def turn_left():
                    pass
                def turn_right():
                    pass
                def find_balls():
                    # Düz ilerle
                    pass
                # daha fazla ayrıntı eklendi, artık topları teker teker seçebiliyor
                def check_balls(red_center, green_center, yellow_center, orjin, warning_txt):
                    orjin_x_range = range(orjin[0] - 300, orjin[0] + 300)
                    
                    red_in_range = red_center[0] in orjin_x_range
                    green_in_range = green_center[0] in orjin_x_range
                    yellow_in_range = yellow_center[0] in orjin_x_range
                    warning_txt = "Cant see"
                    saw = 0
                    if red_in_range: 
                        saw+=1
                        warning_txt = "kirmizi gorunuyor "
                    if green_in_range:
                        saw+=1
                        warning_txt += "yesil gozukuyor "
                    if yellow_in_range:
                        saw+=1
                        warning_txt += "sari gorunuyor "
                    

                    choose_way(red_center , green_center , yellow_center)
                    return warning_txt
                
                def choose_way():
                    # sari center yoksa kırmızı ve yeşilin ortasını bulup yuvarlak çiz


                    #sari center varsa kırmızı ve sari , yeşil ve sari arasındaki farka göre yolu bul yuvarlak çiz
                    pass        
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(img)

                def update_gui():
                    label_veri.imgtk = imgtk
                    label_veri.config(image=imgtk)
                    height, width, _ = frame.shape
                    update_sonuc_panel(f"Görüntü Boyutu: {width}x{height}\n{color_detected}\n")

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
