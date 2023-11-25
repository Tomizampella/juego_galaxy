import pygame
from colores import *
import random
from laser import *


#Enemigo
class Enemigo (pygame.sprite.Sprite):
    def __init__(self,path,ancho,alto,color_fondo,nivel,lista_sprites) -> None:
        super().__init__()
        self.image = pygame.image.load(path).convert()
        self.image.set_colorkey(color_fondo) #le saco el color negro de fondo
        self.image = pygame.transform.scale (self.image, (ancho,alto)) #escalo la imagen
        self.rect = self.image.get_rect() #obtengo el rectangulo a partir de la imagen
        self.rect.x = 45
        self.rect.y = 100
        self.velocidad_x = nivel
        self.direccion = 1  # 1 para moverse a la derecha, -1 para moverse a la izquierda
        self.ancho_alien = ancho
        self.salud = 3
        self.sonido_laser = pygame.mixer.Sound("Nova-defender.main/audio/sonido_laser.mp3")
        self.sonido_laser.set_volume(0.05)
       
        self.grupo_todos_los_sprites = lista_sprites
        self.lista_laser_enemigo = pygame.sprite.Group()

        
    
    def update(self):
        # Mueve la nave en la dirección actual
        self.rect.x += self.velocidad_x * self.direccion

        # Verifica si la nave ha alcanzado los límites de pantalla
        if self.rect.x > (450 - self.ancho_alien):
            self.rect.x = 450 - self.ancho_alien
            self.rect.y = self.rect.y + 40
            self.direccion = -1  # Cambia la dirección a izquierda
        elif self.rect.x < 10:
            self.rect.x = 10
            self.rect.y = self.rect.y + 40
            self.direccion = 1  # Cambia la dirección a derecha
        
        if self.salud <= 0:
            self.kill()

    def dibujar_barra_salud(self, pantalla):
        # Define los colores
        

        # Calcula el ancho de la barra de salud basado en la salud actual del enemigo
        ancho_barra = 100  # Ancho total de la barra de salud
        salud_relativa = max(self.salud, 0) / 3.0  # Normaliza la salud entre 0 y 1
        ancho_salud = int(ancho_barra * salud_relativa)

        # Dibuja el rectángulo rojo (fondo)
        pygame.draw.rect(pantalla, ROJO, (self.rect.x, self.rect.y - 10, ancho_barra, 5))

        # Dibuja el rectángulo verde (indicador de salud)
        pygame.draw.rect(pantalla, VERDE, (self.rect.x, self.rect.y - 10, ancho_salud, 5))
        

    def disparar(self):
        laser_sprite_enemigo = Laser(self.rect.center, 6)
        self.grupo_todos_los_sprites.add(laser_sprite_enemigo)
        self.lista_laser_enemigo.add(laser_sprite_enemigo)
        self.sonido_laser.play()
        
       


