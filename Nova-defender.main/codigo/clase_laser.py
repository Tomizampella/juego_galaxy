import pygame 
from random import *
from colores import *


class Laser(pygame.sprite.Sprite):
	def __init__(self,path,color_fondo,posicion,velocidad):
		super().__init__()
		self.image = pygame.image.load(path).convert()
		self.image.set_colorkey(color_fondo)
		self.image = pygame.transform.scale (self.image, (25,25)) 
		self.rect = self.image.get_rect(center = posicion) 
		self.velocidad = velocidad
		self.limite_eje_y = 700

	def destruir(self):
		if self.rect.y <= -50 or self.rect.y >= self.limite_eje_y + 50:
			self.kill()

	def update(self):
		self.rect.y += self.velocidad
		self.destruir()

