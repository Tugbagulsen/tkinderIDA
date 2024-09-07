import cv2
import numpy as np
import pytesseract
from PIL import Image
from tkinderIDA.Master.dedect_digit import *
from balls_part import *
import keyboard

def find_boat(frame):
    # Botun renginin algılanması
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Mor bot için maske
    lower_purple = np.array([125, 100, 100])
    upper_purple = np.array([150, 255, 255])
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
    
    # Botu dikdörtgene al
    contours, _ = cv2.findContours(mask_purple, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
            cv2.putText(frame, "Bot", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            print(f"Botun konumu: ({x}, {y})")
    return  x , y

def find_port(frame):
    # Beyaz limanın renginin algılanması
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Beyaz liman için maske
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    
    # Limanı dikdörtgene al
    contours, _ = cv2.findContours(mask_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            cv2.putText(frame, "Liman", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            


def IHA_commands(frame , PORT):
    # Botun renginin algılanması
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    
    # Botu dikdörtgene al konumu döndür
    x_boat , y_boat = find_boat(frame)
    
    # Beyaz limanın renginin algılanması ve dikdörtgene alınması
    find_port(frame)
    
    # Limandakı sayıların algılanması ve konumlarının sözlük olarak döndürülmesi
    konumlar_sözlüğü = read_locate_digit(frame)
    
    # Girilen PORT değerine göre botun hareket kendi konumunu belirlemesi ve hareket etmesi
    def lead_toPort():
        
        
        # Neslinin ya da Muhammedin kodunu buraya yaz
        if PORT == 1:
            ...
        elif PORT == 2:
            ...
        elif PORT == 3:
            ...
        else:
            ...
            
    while keyboard.is_pressed() == False:
        lead_toPort()
    
    