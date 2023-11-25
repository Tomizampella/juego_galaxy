import pygame.font
from colores import *

class Boton():
	def __init__(self, x, y, texto):
		self.color_texto = ROJO
		self.color_boton = BLANCO
		self.ancho = 200
		self.alto = 50
		self.rect = pygame.rect(0,0,self.ancho,self.alto)

		self.preparar_texto_como_imagen (texto)

	def preparar_texto_como_imagen(self,texto):
		self.texto_image = self.font.render(texto,True,self.color_texto,self.color_boton)
		self.texto_image_rect = self.t