import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import threading

master=tk.Tk()

canvas=tk.Canvas(master, bg= "Grey", width=800, height=500)
canvas.pack()

def label_frame_olusturma(master, text, relx, rely, relwidth, relheight, bg, fg="white",font=("Arial",  12)):
    label_frame = LabelFrame(master, text=text, bg=bg, fg=fg, font=font)
    label_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return label_frame



label_frame_baslik=label_frame_olusturma(master,"Corydora Panel",0,0,1,0.1,bg="Blue",fg="white",font=("Arial", 12))
label_frame_modlar=label_frame_olusturma(master, "MODLAR",0.01,0.11,0.23,0.33,bg="black", fg="white", font=("Arial", 12))
label_frame_yontemler=label_frame_olusturma(master, "YONTEMLER",0.01,0.45,0.23,0.54,bg="black", fg="white", font=("Arial", 12))
label_frame_veri=label_frame_olusturma(master, "VERİ",0.26,0.11,0.73,0.55,bg="black", fg="white", font=("Arial", 12))
label_frame_enalt=label_frame_olusturma(master, "BOS" ,0.26,0.67,0.73,0.32,bg="black", fg="white", font=("Arial", 12))

var=IntVar()
R1=Radiobutton(label_frame_modlar,text="renk tespit modu", bg="black", fg="white", font="Verdana 8 ", variable = var, value=1)
R1.pack(pady=5,padx=15)
R2=Radiobutton(label_frame_modlar,text="hedef tespit modu", bg="black", fg="white", font="Verdana 8 ", variable = var, value=2)
R2.pack(pady=5,padx=15)
R3=Radiobutton(label_frame_modlar,text="renk tespit modu",  bg="black", fg="white" , font="Verdana 8 ", variable = var, value=3)
R3.pack(pady=5, padx=15)


var1=IntVar()


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
        out = cv2.VideoWriter('video_kaydi.avi', fourcc, 20.0, (640, 480))

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


start_video_capture()



master.mainloop()


