from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import time
import threading


text_1 = 'GEWBOT.COM'
text_2 = 'IP:CONNECTING'
text_3 = '<ARM> OR <PT> MODE'
text_4 = 'MPU6050 DETECTING'
text_5 = 'FUNCTION OFF'
text_6 = 'Message:None'

def run():
	with canvas(device) as draw:
		draw.text((0, 0), "WWW.CODELECTRON.COM", fill="white")
		draw.text((0, 10), "WWW.CODELECTRON.COM", fill="white")
		draw.text((0, 20), "WWW.CODELECTRON.COM", fill="white")
		draw.text((0, 30), "WWW.CODELECTRON.COM", fill="white")
		draw.text((0, 40), "WWW.CODELECTRON.COM", fill="white")
		draw.text((0, 50), "WWW.CODELECTRON.COM", fill="white")
	while 1:
		time.sleep(1)

if __name__ == '__main__':
	try:
		serial = i2c(port=1, address=0x40)
		device = ssd1306(serial, rotate=0)
		print("Todo bien jefe")
	except:
		print('OLED disconnected\nOLED没有连接')
	run()