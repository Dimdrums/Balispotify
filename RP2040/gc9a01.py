from micropython import const
import framebuf
import time

_SWRESET = const(0x01)
_SLPOUT  = const(0x11)
_DISPON  = const(0x29)
_CASET   = const(0x2A)
_RASET   = const(0x2B)
_RAMWR   = const(0x2C)
_MADCTL  = const(0x36)
_COLMOD  = const(0x3A)

class GC9A01(framebuf.FrameBuffer):

    def __init__(self, spi, width, height, reset, cs, dc):
        self.spi = spi
        self.width = width
        self.height = height
        self.reset = reset
        self.cs = cs
        self.dc = dc

        self.buffer = bytearray(width * height * 2)
        super().__init__(self.buffer, width, height, framebuf.RGB565)

        self.reset_display()
        self.init_display()

    def write_cmd(self, cmd):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, data):
        self.cs(0)
        self.dc(1)
        self.spi.write(data)
        self.cs(1)

    def reset_display(self):
        self.reset(1)
        time.sleep_ms(50)
        self.reset(0)
        time.sleep_ms(50)
        self.reset(1)
        time.sleep_ms(150)

    def init_display(self):
        self.write_cmd(_SWRESET)
        time.sleep_ms(150)

        self.write_cmd(_SLPOUT)
        time.sleep_ms(150)

        self.write_cmd(_COLMOD)
        self.write_data(bytearray([0x55]))  # RGB565

        # IMPORTANT : BGR mode activé
        self.write_cmd(_MADCTL)
        self.write_data(bytearray([0x08]))

        # Paramètres spécifiques GC9A01
        self.write_cmd(0xFE)
        self.write_cmd(0xEF)

        self.write_cmd(0xEB)
        self.write_data(bytearray([0x14]))

        self.write_cmd(0x84)
        self.write_data(bytearray([0x40]))

        self.write_cmd(0x85)
        self.write_data(bytearray([0xFF]))

        self.write_cmd(0x86)
        self.write_data(bytearray([0xFF]))

        self.write_cmd(0x87)
        self.write_data(bytearray([0xFF]))

        self.write_cmd(0x88)
        self.write_data(bytearray([0x0A]))

        self.write_cmd(0x89)
        self.write_data(bytearray([0x21]))

        self.write_cmd(0x8A)
        self.write_data(bytearray([0x00]))

        self.write_cmd(0x8B)
        self.write_data(bytearray([0x80]))

        self.write_cmd(0x8C)
        self.write_data(bytearray([0x01]))

        self.write_cmd(0x8D)
        self.write_data(bytearray([0x01]))

        self.write_cmd(0x8E)
        self.write_data(bytearray([0xFF]))

        self.write_cmd(0x8F)
        self.write_data(bytearray([0xFF]))

        self.write_cmd(_DISPON)
        time.sleep_ms(100)

    def show(self):
        self.write_cmd(_CASET)
        self.write_data(bytearray([0x00, 0x00, 0x00, self.width - 1]))

        self.write_cmd(_RASET)
        self.write_data(bytearray([0x00, 0x00, 0x00, self.height - 1]))

        self.write_cmd(_RAMWR)

        # conversion little -> big endian
        buf = self.buffer
        swapped = bytearray(len(buf))

        for i in range(0, len(buf), 2):
            swapped[i] = buf[i+1]
            swapped[i+1] = buf[i]

        self.write_data(swapped)
