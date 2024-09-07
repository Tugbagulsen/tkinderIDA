import cv2
import numpy as np

def calculate_angle(pt1, pt2, pt3):
    # pt2 köşe noktası olarak kabul ediliyor
    a = np.array(pt1) - np.array(pt2)
    b = np.array(pt3) - np.array(pt2)
    cos_theta = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    angle = np.degrees(np.arccos(cos_theta))
    return angle

def detect_triangle(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Kırmızı renk aralıkları
    lower_red1 = np.array([0, 70, 70])
    upper_red1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    lower_red2 = np.array([160, 70, 70])
    upper_red2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = mask_red1 + mask_red2

    # Sarı renk aralıkları
    lower_yellow = np.array([15, 70, 70])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Turuncu renk aralıkları
    lower_orange = np.array([5, 70, 70])
    upper_orange = np.array([30, 255, 255])
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    # Kırmızı, sarı ve turuncu maskelerini birleştir
    mask_combined = cv2.bitwise_or(mask_red, cv2.bitwise_or(mask_yellow, mask_orange))

    # Gürültüyü azaltmak için morfolojik işlemler
    kernel = np.ones((5, 5), np.uint8)
    mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel)
    mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_OPEN, kernel)

    triangle_detected = False
    triangle_center = (0, 0)  # Üçgenin merkezi için değişken

    # Kenarları belirlemek için Canny kenar algılama
    edges = cv2.Canny(mask_combined, 50, 150)

    # Konturları bulma
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Konturu yaklaştırma
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Eğer konturun üç köşesi varsa, bu bir üçgendir
        if len(approx) == 3:
            # Üçgenin alanını hesapla
            area = cv2.contourArea(contour)
            if 500 < area < 2000:  # Üçgen alanı filtrelemesi (örneğin 10 ile 10000 arasında)
                # Üçgenin iç açılarını hesapla
                pt1, pt2, pt3 = approx[0][0], approx[1][0], approx[2][0]
                angle1 = calculate_angle(pt1, pt2, pt3)
                angle2 = calculate_angle(pt2, pt3, pt1)
                angle3 = calculate_angle(pt3, pt1, pt2)

                # Eğer açıların her biri 20 ile 120 derece arasındaysa
                if 20 < angle1 < 70 and 20 < angle2 < 70 and 20 < angle3 < 70:
                    # Üçgeni çiz
                    cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)
                    triangle_detected = True
                    
                    # Kırmızı üçgenin ağırlık merkezini (centroid) hesapla
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        triangle_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    else:
                        triangle_center = (0, 0)

                    # İkinci nokta: Ağırlık merkezinden 100 piksel yukarı ve 100 piksel sağa kaydırılmış nokta
                    ikinci_nokta = (triangle_center[0] + 100, triangle_center[1] - 100)

                    # İkinci noktayı çiz (mavi çember ile göster)
                    cv2.circle(frame, ikinci_nokta, 5, (255, 0, 0), -1)

                    # Sol alt köşe noktayı bulma
                    sol_alt_kose = min([pt1, pt2, pt3], key=lambda x: (x[1],x[0]))  # X eksenine göre en soldaki noktayı bul

                    # Sol alt köşenin hizasında 200 piksel aşağıya noktayı yerleştir
                    ilk_nokta = (sol_alt_kose[0], sol_alt_kose[1] + 200)
                    cv2.circle(frame, ilk_nokta, 5, (255, 0, 0), -1)  # Yeni noktayı mavi çember ile göster


                    """
                    # Sol alt köşe noktayı bulma
                    sol_alt_kose = min([pt1, pt2, pt3], key=lambda x: (x[1], x[0]))
                    
                    # Sol alt köşeden 200 piksel aşağıya noktayı yerleştir
                    yeni_nokta = (sol_alt_kose[0], sol_alt_kose[1] + 200)
                    cv2.circle(frame, yeni_nokta, 5, (255, 0, 0), -1)  # Yeni noktayı mavi çember ile göster
                    """


    return frame, triangle_center, triangle_detected,ilk_nokta,ikinci_nokta

# Video akışını aç
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Üçgen algılama
    frame, triangle_center, triangle_detected = detect_triangle(frame)

    # Görüntüyü göster
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
