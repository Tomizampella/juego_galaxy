import pygame 
from random import *
from colores import *
class Laser(pygame.sprite.Sprite):
	def __init__(self,posicion,velocidad):
		super().__init__()
		self.image = pygame.image.load("Nova-defender.main/imagenes/laser.png").convert()
		self.image.set_colorkey(NEGRO)
		self.image = pygame.transform.scale (self.image, (25,25)) #escalo la imagen
		self.rect = self.image.get_rect(center = posicion) #obtengo el rectangulo a partir de la imagen
		self.velocidad = velocidad
		self.limite_eje_y = 700

	def destroy(self):
		if self.rect.y <= -50 or self.rect.y >= self.limite_eje_y + 50:
			self.kill()

	def update(self):
		self.rect.y += self.velocidad
		self.destroy()

