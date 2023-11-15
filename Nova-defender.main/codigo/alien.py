import pygame
from colores import *
import random
from laser import *


#Enemigo
class Enemigo (pygame.sprite.Sprite):
    def __init__(self,path,ancho,alto,color_fondo) -> None:
        super().__init__()
        self.image = pygame.image.load(path).convert()
        self.image.set_colorkey(color_fondo) #le saco el color negro de fondo
        self.image = pygame.transform.scale (self.image, (ancho,alto)) #escalo la imagen
        self.rect = self.image.get_rect() #obtengo el rectangulo a partir de la imagen
        self.rect.x = 45
        self.velocidad_x = 1
        self.direccion = 1  # 1 para moverse a la derecha, -1 para moverse a la izquierda

        self.sonido_laser = pygame.mixer.Sound("Nova-defender.main/audio/sonido_laser.mp3")
        self.sonido_laser.set_volume(0.05)


        
    
    def update(self):
        # Mueve la nave en la dirección actual
        self.rect.x += self.velocidad_x * self.direccion

        # Verifica si la nave ha alcanzado los límites de pantalla
        if self.rect.x > 400:
            self.rect.x = 400
            self.rect.y = self.rect.y + 40
            self.direccion = -1  # Cambia la dirección a izquierda
        elif self.rect.x < 10:
            self.rect.x = 10
            self.rect.y = self.rect.y + 40
            self.direccion = 1  # Cambia la dirección a derecha
        # elif self.rect.y >= player.rect.y: VER QUE PASA SI ENEMIGO PASA EL RECT.Y DE PLAYER
        #     pygame.quit()

