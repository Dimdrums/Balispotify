import cv2
import numpy as np
import os

COLORS=False

# Vidéo source
video_file = "pedro_h264_3fps.mp4"

# Dossier de sortie
output_dir = "frames_raw"
os.makedirs(output_dir, exist_ok=True)

# Taille de l'écran GC9A01
WIDTH = 240
HEIGHT = 240

# Conversion RGB888 -> RGB565
def rgb888_to_rgb565(frame):
    r = frame[:, :, 0] >> 3
    g = frame[:, :, 1] >> 2
    b = frame[:, :, 2] >> 3
    return ((r << 11) | (g << 5) | b).astype(np.uint16)

# Lire la vidéo
cap = cv2.VideoCapture(video_file)
frame_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionner
    frame = cv2.resize(frame, (WIDTH, HEIGHT))

    if COLORS:
        # Convertir BGR -> RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Normaliser 0-255 si besoin (garanti valeurs entières)
        frame = np.clip(frame, 0, 255).astype(np.uint8)

        # Convertir en RGB565
        rgb565 = rgb888_to_rgb565(frame)
    else:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_rgb = cv2.merge([frame_gray, frame_gray, frame_gray])
        rgb565 = rgb888_to_rgb565(frame_rgb)

    # Sauver en raw (little endian)

    rgb565.tofile(os.path.join(output_dir, f"frame{frame_idx:03d}.raw"))
    frame_idx += 1

cap.release()
print(f"{frame_idx} frames générées dans {output_dir}")