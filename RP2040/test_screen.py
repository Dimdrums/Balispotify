from machine import Pin, SPI
import gc9a01
import time
import os

# SPI et écran
spi = SPI(0, baudrate=40000000, sck=Pin(2), mosi=Pin(3))
tft = gc9a01.GC9A01(spi, 240, 240, reset=Pin(4), cs=Pin(1), dc=Pin(0))
tft.init()

# Couleur de fond
bg = gc9a01.BLACK
tft.fill(bg)

# Liste des frames
frame_count = 20  # jusqu'à 190
frame_folder = "/frames_raw"  # racine de la Pico ou dossier où tu as mis les .raw

# Affichage boucle
fps = 20  # frames par seconde
delay = 1 / fps

for i in range(frame_count):
    filename = "{}/frame{:03d}.raw".format(frame_folder, i)
    try:
        with open(filename, "rb") as f:
            buf = f.read()  # 240*240*2 = 115200 bytes
            tft.blit_buffer(buf, 0, 0, 240, 240)
        time.sleep(delay)
    except OSError:
        print("Impossible de lire", filename)

print("End")
