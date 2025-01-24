import cv2
import numpy as np
import os

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

cap = "Data/video_rodovia.mp4"
capture = cv2.VideoCapture(cap)

if not capture.isOpened():
    print("Erro ao carregar o vídeo.")
    exit(0)

rois = []
subtractors = []
drawing = False
start_point = (-1, -1)
veiculos_contagem = [0] * 10
linhas_passagem = []
velocidades_veiculos = {}
frame_counter = 0
historico_centroides = []

def select_roi(event, x, y, flags, param):
    global drawing, start_point, rois, subtractors
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        frame_copy = frame.copy()
        cv2.rectangle(frame_copy, start_point, (x, y), (0, 0, 139), 2)
        cv2.imshow("Vídeo Principal", frame_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        x1, y1 = start_point
        x2, y2 = end_point
        rois.append((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
        subtractors.append(cv2.createBackgroundSubtractorKNN())
        linha = (min(x1, x2), (min(y1, y2) + max(y1, y2)) // 2, max(x1, x2), (min(y1, y2) + max(y1, y2)) // 2)
        linhas_passagem.append(linha)
        print(f"ROI definida: {rois[-1]}, Linha de passagem: {linha}")

ret, frame = capture.read()
if not ret:
    print("Erro ao carregar o primeiro frame.")
    exit(0)

cv2.namedWindow("Vídeo Principal")
cv2.setMouseCallback("Vídeo Principal", select_roi)

print("Desenhe as ROIs com o mouse e pressione 'q' para continuar.")
while True:
    cv2.imshow("Vídeo Principal", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

if not rois:
    print("Nenhuma ROI foi definida. Por favor, reinicie o script e selecione as ROIs.")
    exit(0)

def preprocess_frame(frame, subtractor, kernel_size=5, image_threshold=170):
    fgmask = subtractor.apply(frame)
    blur = cv2.GaussianBlur(fgmask, (7, 7), 0)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    closing = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    _, binary_image = cv2.threshold(opening, image_threshold, 255, cv2.THRESH_BINARY)
    return binary_image

def get_centroid(contour):
    moments = cv2.moments(contour)
    if moments['m00'] != 0:
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
    else:
        cx, cy = 0, 0
    return (cx, cy)

def calcular_velocidade(centroid_atual, centroid_anterior, frames, pixel_length, frames_per_second):
    if centroid_anterior is None:
        return 0, 0
    distancia_pixels = np.linalg.norm(np.array(centroid_atual) - np.array(centroid_anterior))
    velocidade_px_frame = distancia_pixels / frames
    cm_to_km_per_hour = 0.036
    velocidade_kmh = distancia_pixels * pixel_length * frames_per_second * cm_to_km_per_hour
    return velocidade_px_frame, velocidade_kmh

def detectar_veiculos(binary_image, frame, linha, roi_offset, min_area=150, centroid_dist_threshold=50, pixel_length=7.2, frames_per_second=30):
    global historico_centroides

    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contagem = 0
    x_offset, y_offset = roi_offset

    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        centroid = get_centroid(contour)
        centroid_global = (centroid[0] + x_offset, centroid[1] + y_offset)
        bbox_global = (x + x_offset, y + y_offset, w, h)

        carro_id = None
        menor_distancia = np.inf
        velocidade_px_frame = 0
        velocidade_kmh = 0

        for id_historico, (centroid_historico, frame_historico) in enumerate(historico_centroides):
            distancia = np.linalg.norm(np.array(centroid_global) - np.array(centroid_historico))
            if distancia < menor_distancia and distancia < centroid_dist_threshold:
                menor_distancia = distancia
                carro_id = id_historico
                velocidade_px_frame, velocidade_kmh = calcular_velocidade(
                    centroid_global, centroid_historico, frame_counter - frame_historico, pixel_length, frames_per_second
                )

        if carro_id is None:
            carro_id = len(historico_centroides)
            historico_centroides.append((centroid_global, frame_counter))
        else:
            historico_centroides[carro_id] = (centroid_global, frame_counter)

        if linha[1] - 5 <= centroid_global[1] <= linha[1] + 5:
            contagem += 1

        cv2.rectangle(frame, (bbox_global[0], bbox_global[1]), (bbox_global[0] + w, bbox_global[1] + h), (0, 100, 0), 2)
        cv2.circle(frame, centroid_global, 5, (0, 255, 255), -1)
        cv2.putText(frame, f"ID: {carro_id}", (bbox_global[0], bbox_global[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Vel: {velocidade_px_frame:.2f} px/frame", (bbox_global[0], bbox_global[1] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"{velocidade_kmh:.2f} km/h", (bbox_global[0], bbox_global[1] - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    historico_centroides = [item for item in historico_centroides if frame_counter - item[1] < 30]

    return contagem

while True:
    ret, frame = capture.read()
    if not ret:
        break

    frame_copy = frame.copy()
    frame_counter += 1

    for i, (x1, y1, x2, y2) in enumerate(rois):
        roi = frame[y1:y2, x1:x2]
        linha = linhas_passagem[i]
        cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 0, 139), 2)
        binary_image = preprocess_frame(roi, subtractors[i])
        contagem = detectar_veiculos(binary_image, frame_copy, linha, (x1, y1))
        veiculos_contagem[i] += contagem
        cv2.line(frame_copy, (linha[0], linha[1]), (linha[2], linha[3]), (0, 0, 139), 2)
        cv2.putText(frame_copy, f"ROI {i+1}: Total: {veiculos_contagem[i]}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 139), 2)

    cv2.imshow("Vídeo Principal", frame_copy)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
