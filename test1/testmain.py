import cv2
from ball import *
from datetime import datetime
import time

def start():
    cap = cv2.VideoCapture(0)  # Kamera başlatma
    
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return
    
    
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    #videoyu kaydetme
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_filename = f"Akriha_Control_{now}.avi"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))
    while cap.isOpened:
        ret , frame = cap.read()
        
        if not ret:
            print("Error: Unable to read frame")
            break


        drive_boat(ret, frame)
        out.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        cv2.imshow('Frame', frame)


def main():
    start()

       
    
if __name__ == '__main__':
    main()
