import serial

ser = serial.Serial("COM7", 115200)  # Windows
# ser = serial.Serial("/dev/ttyACM0", 115200)  # Linux
# ser = serial.Serial("/dev/cu.usbmodem...", 115200)  # macOS
print("OK")

while True:
    line = ser.readline().decode().strip()
    print("Reçu:", line)