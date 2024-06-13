from rpi_ws281x import *


class LED:
    def __init__(self):
        self.LED_COUNT = 3
        self.LED_PIN = 12
        self.LED_FREQ_HZ = 800000
        self.LED_DMA = 10
        self.LED_BRIGHTNESS = 255
        self.LED_INVERT = False
        self.LED_CHANNEL = 0

        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT,
                                       self.LED_BRIGHTNESS, self.LED_CHANNEL)

        self.strip.begin()

    def colorWipe(self, R, G, B):
        color = Color(R, G, B)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
