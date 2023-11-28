import pygame
from colores import *
import random
from clase_laser import *


class Player(pygame.sprite.Sprite):
    def __init__(self,ancho,alto,lista_sprites) -> None:
        super().__init__()
        self.image = pygame.image.load("Nova-defender.main/imagenes/nave_espacial.png").convert()
        self.image.set_colorkey(BLANCO) 
        self.image = pygame.transform.scale (self.image, (ancho,alto)) 
        self.rect = self.image.get_rect() 
        self.rect.x = 200
        self.rect.y = 625
        self.imagen_vidas = pygame.image.load("Nova-defender.main/imagenes/corazon_vida.png").convert()
        self.imagen_vidas.set_colorkey(NEGRO)
        self.imagen_vidas = pygame.transform.scale (self.imagen_vidas, (20,20))
        
        self.salud = 3
        self.puntaje = 0
        self.barra_poder = 0
        self.nombre = ""
        self.poder_activado = False

        self.grupo_todos_los_sprites = lista_sprites
        self.lista_laser_player = pygame.sprite.Group()
        self.sonido_laser = pygame.mixer.Sound("Nova-defender.main/audio/sonido_laser.mp3")
        self.sonido_laser.set_volume(0.05)

        self.cooldown_tiempo = 500  
        self.ultimo_disparo = 0  

    def update (self, velocidad_x = 0):
        nueva_x = self.rect.x + velocidad_x
        if nueva_x < 400 and nueva_x > 0:
            self.rect.x = self.rect.x + velocidad_x
        
        if self.barra_poder == 10 and not self.poder_activado:
            self.poder_activado = True
        
    def dibujar_vida_poder (self, pantalla):
        # Muestra vidas en pantalla
        for i in range(self.salud):
            ubicacion_en_la_pantalla = (i*30,30)
            pantalla.blit(self.imagen_vidas,ubicacion_en_la_pantalla)
        
        # Barra de poder
        ancho_barra = 50  
        ancho_poder = 5 * self.barra_poder 
        pygame.draw.rect(pantalla, GRIS, (self.rect.x, self.rect.bottom + 10, ancho_barra, 5))
        pygame.draw.rect(pantalla,AMARILLO, (self.rect.x, self.rect.bottom + 10, ancho_poder, 5))
   

    def disparar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo > self.cooldown_tiempo:
            if self.poder_activado == True:
                # Disparar laser doble
                laser_sprite_izquierdo = Laser("Nova-defender.main/imagenes/laser_player.png",NEGRO,(self.rect.left, self.rect.bottom), -6)
                laser_sprite_derecho = Laser("Nova-defender.main/imagenes/laser_player.png",NEGRO,(self.rect.right, self.rect.bottom), -6)

                self.grupo_todos_los_sprites.add(laser_sprite_izquierdo, laser_sprite_derecho)
                self.lista_laser_player.add(laser_sprite_izquierdo, laser_sprite_derecho)

                self.barra_poder = self.barra_poder - 2
                if self.barra_poder == 0:
                    self.poder_activado = False
                self.sonido_laser.play()
            else:
                # Disparar laser simple
                laser_sprite_player = Laser("Nova-defender.main/imagenes/laser_player.png",NEGRO,(self.rect.centerx, self.rect.top), -6)
                self.grupo_todos_los_sprites.add(laser_sprite_player)
                self.lista_laser_player.add(laser_sprite_player)
                self.sonido_laser.play()
        
            self.ultimo_disparo = tiempo_actual 
    

    def posicion_de_inicio (self):
        self.rect.x = 200
        self.rect.y = 625
        self.salud = 3
    
    def nueva_partida (self):
        self.posicion_de_inicio()
        self.puntaje = 0
        self.barra_poder = 0
        self.poder_activado = False
    
    def modificar_estadisticas(self, valor_puntaje, valor_vida = 0):
        self.puntaje = self.puntaje + 100 * valor_puntaje
        self.salud = self.salud + valor_vida
        

        
        
        
        
        