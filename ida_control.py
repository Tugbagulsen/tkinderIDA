import tkinter as tk
from tkinter import LabelFrame, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime

# Başlangıç penceresi boyutları
canvas_genislik = 1000
canvas_yukseklik = 450
panel_margin = 10
top_margin = 20  # burada top_margin tanımlandı

# Tkinter ana penceresi
master = tk.Tk()
master.title("Kamera ve Veri Okuma Uygulaması")

# Kanvas oluşturma
canvas = tk.Canvas(master, width=canvas_genislik, height=canvas_yukseklik)
canvas.pack()

# Panel oluşturma fonksiyonu
def label_frame_olusturma(master, text, relx, rely, relwidth, relheight):
    label_frame = LabelFrame(master, text=text)
    label_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return label_frame

# Veri Paneli (kamera görüntüsü burada gösterilecek)
label_frame_veri = label_frame_olusturma(master, "Veri", 0.04, top_margin / canvas_yukseklik, 0.5, 0.65)

# Sonuç Paneli (kameradan çıkarılan veriler burada yazdırılacak)
label_frame_sonuc = label_frame_olusturma(master, "Sonuç", 0.6, 0.2, 0.35, 0.5)

# Fonksiyon Paneli
label_frame_fonksiyon = label_frame_olusturma(master, "Fonksiyon", 0.6, 0.6, 0.35, 0.3)

# Kamera açma butonu
def btnCamera():
    start_video_capture()

# Video akışını başlatacak fonksiyon
def start_video_capture():
    label_veri = tk.Label(label_frame_veri)  # "Veri" panelinde kamera görüntüsü gösterilecek
    label_veri.pack()

    def video_thread():
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Hata", "Kamera bulunamadı veya açılamadı!")
            return

        # Video kaydı için nesne oluşturma
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_filename = f"video_kayit_{now}.avi"
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                # Görüntüyü "Veri" panelinde göster
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(img)

                label_veri.config(image=imgtk)
                label_veri.image = imgtk

                # Video kaydı
                out.write(frame)

                # Kameradan bazı verileri "Sonuç" paneline yazdır
                height, width, _ = frame.shape
                update_sonuc_panel(f"Görüntü Boyutu: {width}x{height}")

            else:
                break

            time.sleep(0.05)  # Görüntü güncellemeleri arasında küçük bir bekleme süresi

        # Kaynakları serbest bırak
        cap.release()
        out.release()  # Video kaydını tamamla

    threading.Thread(target=video_thread, daemon=True).start()

# Sonuç paneline veri yazdırmak için fonksiyon
def update_sonuc_panel(text):
    # "Sonuç" paneline veri eklemek için mevcut içeriği temizle ve yeni içerik ekle
    for widget in label_frame_sonuc.winfo_children():
        widget.destroy()

    label = tk.Label(label_frame_sonuc, text=text)
    label.pack()

# Fonksiyonlar
def btnBatma():
    messagebox.showinfo("Bilgi", "Batma butonuna tıklandı")

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
    row = i // 2
    column = i % 2
    buton = tk.Button(label_frame_fonksiyon, text=metin, width=10, height=1, background='White', command=buton_fonksiyonlari[i])
    buton.grid(row=row, column=column, padx=40, pady=3)

# Tkinter ana döngüsü
master.mainloop()
