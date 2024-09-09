from triangle_detection import ilk_nokta, ikinci_nokta

frame, triangle_center, triangle_detected = detect_triangle(frame)

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


