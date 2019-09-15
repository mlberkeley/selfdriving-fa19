import sys
sys.path.append('../')

import controller
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.transforms import Affine2D
import math
import PIL
plt.ion()

class Car_Visualizer():

	def __init__(self):
		self.interface = controller.Car_Interface()

		self.pedal = None
		self.amount = 0
		self.TIME_UNIT = self.interface.dt

		self.img = PIL.Image.open("car.png")


	def start(self):
		self.close = False

		threading.Timer(self.TIME_UNIT, self.update_pos).start()
		threading.Thread(target = self.update_input).start()

		DISPLAY_SPEED = 3

		plt.figure(figsize=(5,5))
		while(True and not self.close):
			time.sleep(self.TIME_UNIT)
			plt.clf()
			plt.xlim(-1.5, 1.5)
			plt.ylim(-1.5, 1.5)
			ang = (self.interface.position * DISPLAY_SPEED) % (2 * math.pi)
			c = plt.Circle((0, 0), 0.95, color='k', fill = False)
			plt.gca().add_artist(c)

			
			rotated_img = OffsetImage(self.img.rotate(-90 + (ang * 180 / math.pi)), zoom = 0.1)
			ab = AnnotationBbox(rotated_img, (math.cos(ang), math.sin(ang)), frameon=False)
			plt.gca().add_artist(ab)

			plt.text(-0.15, 0, f"{self.interface.velocity * 100:.2f}%")

			plt.draw()
			plt.pause(0.0001)
			
	def update_input(self):
		if (self.close):
			return

		inp = input("INPUT CONTROL: ").split(' ')
		if (inp[0] == 'off'):
			self.close = True
		elif (inp[0] == 'forward' or inp[0] == 'reverse'):
			new_gear = self.interface.FORWARD if inp[0] == 'forward' else self.interface.REVERSE
			self.interface.set_gear(new_gear)
			print(f"Setting gear to {inp[0]}")

		elif (inp[0] == 'release'):
			self.pedal = None
			print(f"Releasing Pedal")

		elif (inp[0] == 'accel' or inp[0] == 'brake'):
			self.pedal = self.interface.ACCELERATOR if inp[0] == 'accel' else self.interface.BRAKE
			self.amount = float(inp[1])
			if (inp[0] == "accel"):
				print(f"accelerating {self.amount * 100:.2f}%")
			else:
				print(f"braking {self.amount * 100:.2f}%")

		threading.Thread(target = self.update_input).start()

	def update_pos(self):
		if (self.close):
			return

		if (self.interface.gear is not None):
			self.interface.apply_control(self.pedal, self.amount)

		threading.Timer(self.TIME_UNIT, self.update_pos).start()


cv = Car_Visualizer()
cv.start()



