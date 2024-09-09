import tkinter as tk
from tkinter import messagebox




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
    messagebox.showinfo("Bilgi", "Arm butonuna tıkandı")

def btnDisarm():
    messagebox.showinfo("Bilgi", "Disarm butonuna tıklandı")

def btnStabilize():
    messagebox.showinfo("Bilgi", "Stabilize butonuna tıklandı")

def btnAuto():
    messagebox.showinfo("Bilgi", "Auto butonuna tıklandı")
    
def label_frame_olusturma(master, text, relx, rely, relwidth, relheight):
    label_frame = tk.LabelFrame(master, text=text)
    label_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return label_frame