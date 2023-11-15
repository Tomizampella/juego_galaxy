import pygame
from colores import *
import random
from laser import *



#Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self,ancho,alto,lista_sprites) -> None:
        super().__init__()
        self.image = pygame.image.load("Nova-defender.main/imagenes/nave_espacial.png").convert()
        self.image.set_colorkey(BLANCO) #le saco el color blanco de fondo
        self.image = pygame.transform.scale (self.image, (ancho,alto)) #escalo la imagen
        self.rect = self.image.get_rect() #obtengo el rectangulo a partir de la imagen
        self.rect.x = 200
        self.rect.y = 625
        self.salud = 3
        self.imagen_vidas = pygame.image.load("Nova-defender.main/imagenes/corazon_vida.png").convert()
        self.imagen_vidas.set_colorkey(NEGRO)
        self.imagen_vidas = pygame.transform.scale (self.imagen_vidas, (20,20))
        self.score = 0

        self.grupo_todos_los_sprites = lista_sprites
        self.lista_laser_player = pygame.sprite.Group()
        

        self.sonido_laser = pygame.mixer.Sound("Nova-defender.main/audio/sonido_laser.mp3")
        self.sonido_laser.set_volume(0.05)

    def update (self, velocidad_x = 0): #seteo velocidad en cero si no rompe por no poder encontrarle el valor
        
        nueva_x = self.rect.x + velocidad_x
        if nueva_x < 400 and nueva_x > 0:
            self.rect.x = self.rect.x + velocidad_x
        
    def vidas_en_pantalla (self, superficie):
        for i in range(self.salud):
            ubicacion_en_la_pantalla = (i*30,90)
            superficie.blit(self.imagen_vidas,ubicacion_en_la_pantalla)#muestra vidas en pantalla // logica bien
        
    def disparar(self):
        laser_sprite_player = Laser(self.rect.center, -6, self.rect.bottom)
        self.grupo_todos_los_sprites.add(laser_sprite_player)
        self.lista_laser_player.add(laser_sprite_player)
        self.sonido_laser.play()
        