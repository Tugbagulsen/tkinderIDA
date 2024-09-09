import tkinter as tk
from tkinter import LabelFrame, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
import numpy as np
import pytesseract
from tkinderIDA.Master.balls_part import *
from tkinderIDA.Master.tesseract import *
import keyboard

# Tesseract'ın yolunu belirtin
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



# Tkinter GUI setup
root = tk.Tk()
root.title("Ball Detection, OCR and Motor Control")
root.geometry("800x600")

label_frame_veri = LabelFrame(root, text="Video Feed", width=640, height=480)
label_frame_veri.pack(padx=10, pady=10)

label_veri = tk.Label(label_frame_veri)
label_veri.pack()

# OCR ile tespit edilen rakamları göstermek için Label
label_rakamlar = tk.Label(root, text="Tespit edilen rakamlar: Yok", font=("Arial", 16))
label_rakamlar.pack(pady=10)

# Function to start video capture
def start_video_capture():
    
# BU KISIMDA GEMININ KAMERASI KULLANILACAK
    # GEMININ KAMERASI HANGISI ISE
    boat_camera = 0
    iha_camera = 1
    
    cap = cv2.VideoCapture(boat_camera)  # Capture from default camera
    if not cap.isOpened():
        messagebox.showerror("Error", "BOAT Camera not found or cannot be opened!")
        return

    def video_thread_boat():
        orjin = (320, 240)  # Define the center of the screen

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Color detection process (from your previous code)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                drive_boat(frame)
                # Convert the frame from BGR to RGB for Tkinter display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)

                label_veri.imgtk = imgtk
                label_veri.config(image=imgtk)

            time.sleep(0.05)

        cap.release()
        
    cap = cv2.VideoCapture(iha_camera)  # Capture from iha camera
    
    if not cap.isOpened():
        messagebox.showerror("Error", "IHA Camera not found or cannot be opened!")
        return
    
    def video_thread_iha():
        orjin = (320, 240)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                ...
                        
        

                

# Button to start video capture
start_button = tk.Button(root, text="Start Video Capture", command=start_video_capture)
start_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
