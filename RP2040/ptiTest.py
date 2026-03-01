from machine import Pin, SPI
import gc9a01
import time

# SPI0
spi = SPI(0, baudrate=20000000, sck=Pin(2), mosi=Pin(3))

# Création écran
tft = gc9a01.GC9A01(
    spi,
    240,
    240,
    reset=Pin(4, Pin.OUT),
    cs=Pin(1, Pin.OUT),
    dc=Pin(0, Pin.OUT),
    rotation=0
)

import math
import gc9a01

darkgrey = gc9a01.color565(40, 40, 40)

tft.fill(gc9a01.BLACK)
tft.fill_circle(120, 120, 100, darkgrey)

angle = 0
old_x = 120
old_y = 120

while True:
    # Efface ancienne boule
    tft.fill_circle(old_x, old_y, 12, darkgrey)

    # Nouvelle position
    x = int(120 + math.cos(angle) * 80)
    y = int(120 + math.sin(angle) * 80)

    # Dessine nouvelle boule
    tft.fill_circle(x, y, 12, gc9a01.RED)

    old_x = x
    old_y = y
    angle += 0.2
    time.sleep(0.15)

# import math
# import gc9a01
# 
# darkgrey = gc9a01.color565(40, 40, 40)
# 
# tft.fill(gc9a01.BLACK)
# tft.fill_circle(120, 120, 100, darkgrey)
# 
# angle = 0
# old_x = 120
# old_y = 120
# 
# while True:
# 
#     # Restaurer fond exact sous ancienne boule
#     for dx in range(-10, 11):
#         for dy in range(-10, 11):
#             if dx*dx + dy*dy <= 100:
#                 px = old_x + dx
#                 py = old_y + dy
# 
#                 # vérifier si pixel appartient au grand cercle
#                 if (px-120)**2 + (py-120)**2 <= 100*100:
#                     tft.pixel(px, py, darkgrey)
#                 else:
#                     tft.pixel(px, py, gc9a01.BLACK)
# 
#     # Nouvelle position
#     x = int(120 + math.cos(angle) * 80)
#     y = int(120 + math.sin(angle) * 80)
# 
#     tft.fill_circle(x, y, 9, gc9a01.RED)
# 
#     old_x = x
#     old_y = y
#     angle += 0.1
#     time.sleep(0.1)