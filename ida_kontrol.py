import tkinter as tk
from tkinter import LabelFrame, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import datetime



master = tk.Tk()

canvas_genislik = 1000 # burada neden degişken atamayı kullandık
canvas_yukseklik = 450
panel_genislik = 150
panel_yukseklik = 250
panel_margin = 10
top_margin = 20

canvas = tk.Canvas(master, width=canvas_genislik, height=canvas_yukseklik)
canvas.pack()


def label_frame_olusturma(master, text, relx, rely, relwidth, relheight):
    label_frame = LabelFrame(master, text=text)
    label_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return label_frame


# Veri Paneli Oluşturma Fonksiyonu
label_frame_veri = label_frame_olusturma(master, "Veri", 0.04, top_margin / canvas_yukseklik, 0.5, 0.65)

# Arac Paneli Oluşturma Fonksiyonu
label_frame_arac = label_frame_olusturma(master, "Arac", 0.6, 0.04, 0.34, 0.1)
label_arac = tk.Label(label_frame_arac, text="Jetson Nano    192.168.1.1")
label_arac.pack(padx=15, pady=5, anchor=tk.NW)

# Sonuç Paneli Oluşturma Fonksiyonu
label_frame_sonuc = label_frame_olusturma(master, "Sonuç", 0.04, top_margin / 28, 0.9, 0.2)

# Fonksiyon Paneli Oluşturma Fonksiyonu
label_frame_fonksiyon = label_frame_olusturma(master, "Fonksiyon", 0.6, 0.2, 0.35, 0.5)


# Fonksiyonlar
def func1():
    messagebox.showinfo("Bilgi", "Butona 1 tıklandı")


def func2():
    messagebox.showinfo("Bilgi", "Butona 2 tıklandı")


def func3():
    messagebox.showinfo("Bilgi", "Butona 3 tıklandı")


def func4():
    messagebox.showinfo("Bilgi", "Butona 4 tıklandı")


def func5():
    messagebox.showinfo("Bilgi", "Butona 5 tıklandı")


def func6():
    messagebox.showinfo("Bilgi", "Butona 6 tıklandı")


def func7():
    start_video_capture()


def func8():
    messagebox.showinfo("Bilgi", "Butona 8 tıklandı")


def func9():
    messagebox.showinfo("Bilgi", "Butona 9 tıklandı")


def func10():
    messagebox.showinfo("Bilgi", "Butona 10 tıklandı")


def func11():
    messagebox.showinfo("Bilgi", "Butona 11 tıklandı")


def func12():
    messagebox.showinfo("Bilgi", "Butona 12 tıklandı")


# Butonları Dinamik Olarak Yerleştirme
buton_metinleri = ["Batma", "Çıkma", "Sağ", "Sol", "İleri", "Geri", "Kamera", "Reset", "Arm", "Disarm", "Stabilize",
                   "Auto"]
buton_fonksiyonlari = [func1, func2, func3, func4, func5, func6, func7, func8, func9, func10, func11,
                       func12]
for i, metin in enumerate(buton_metinleri):
    row = i // 2
    column = i % 2
    buton = tk.Button(label_frame_fonksiyon, text=metin, width=10, height=1, background='White',
                      command=buton_fonksiyonlari[i])
    buton.grid(row=row, column=column, padx=40, pady=3)


def kamera_goruntusu_goster():
    def kamera_thread():



        # Kamera başlatma
        kamera = cv2.VideoCapture(0)

        while True:
            # Kameradan bir kare al
            ret, kare = kamera.read()

            # Eğer kare başarılı bir şekilde alındıysa
            if ret:
                # OpenCV kütüphanesinden görüntüyü Tkinter ile uyumlu hale getirme
                kare = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)
                kare = Image.fromarray(kare)
                kare = ImageTk.PhotoImage(kare)

                # Görüntüyü bir etikete yerleştirme
                label = tk.Label(label_frame_veri, image=kare)
                label.image = kare
                label.pack()

                # 10 ms bekleyerek kareyi güncelleme
                label.after(10, kamera_thread)
            else:
                messagebox.showerror("Hata", "Kamera görüntüsü alınamadı.")
                break

        # Kamerayı kapat
        kamera.release()

    # Kamera işlemlerini arka planda gerçekleştirme
    threading.Thread(target=kamera_thread, daemon=True).start()


def start_video_capture():
    def video_thread():


        # Video kaydı için kamera yakalama
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Hata", "Kamera bulunamadı veya açılamadı!")
            return
        # Video kaydı için VideoWriter nesnesi oluşturma


        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        tarih_saat = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dosya_adi = f'video_{tarih_saat}.avi'
        out = cv2.VideoWriter(dosya_adi, fourcc, 20.0, (640, 480))

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Her kareyi uygun formata dönüştürme
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)

                # Görüntüyü bir etikete yerleştirme
                label.config(image=frame)
                label.image = frame

                # 'q' tuşuna basılınca kayıttan çık
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

            # 30 ms bekleyerek kareyi güncelleme
            label.after(30)

        # Pencere ve kayıt nesnelerini serbest bırak
        cap.release()
        out.release()

    # İlk kareyi göstermek için bir etiket oluşturma
    label = tk.Label(label_frame_veri)
    label.pack()

    # Video işlemlerini arka planda gerçekleştirme
    threading.Thread(target=video_thread, daemon=True).start()



master.mainloop()






