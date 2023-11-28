import pygame
from colores import *
from clase_laser import *


class Enemigo (pygame.sprite.Sprite):
    def __init__(self,path,ancho,alto,color_fondo,nivel,vidas) -> None:
        super().__init__()
        self.image = pygame.image.load(path).convert()
        self.image.set_colorkey(color_fondo) 
        self.image = pygame.transform.scale (self.image, (ancho,alto)) 
        self.rect = self.image.get_rect() 
        self.rect.x = 45
        self.rect.y = 100
        self.velocidad_x = nivel
        self.direccion = 1 
        self.ancho_alien = ancho
        self.salud = vidas
        self.sonido_laser = pygame.mixer.Sound("Nova-defender.main/audio/sonido_laser.mp3")
        self.sonido_laser.set_volume(0.05)
       
    
    def update(self):
        # Mueve la nave en la direccion actual
        self.rect.x += self.velocidad_x * self.direccion

        # Verifica si enemigo toco los bordes de la pantalla
        if self.rect.x > (450 - self.ancho_alien):
            self.rect.x = 450 - self.ancho_alien
            self.rect.y = self.rect.y + 40
            self.direccion = -1 
        elif self.rect.x < 10:
            self.rect.x = 10
            self.rect.y = self.rect.y + 40
            self.direccion = 1  
        
        if self.salud <= 0:
            self.kill()

    def dibujar_barra_salud(self, pantalla):
        # Barra de salud
        ancho_barra = 100 
        ancho_salud = 10 * self.salud 
        pygame.draw.rect(pantalla, ROJO, (self.rect.x, self.rect.y - 10, ancho_barra, 5))
        pygame.draw.rect(pantalla, VERDE, (self.rect.x, self.rect.y - 10, ancho_salud, 5))

    def disparar(self,lista_laser_enemigo):
        # Disparar laser simple
        laser_sprite_enemigo = Laser("Nova-defender.main/imagenes/laser_enemigo.png",NEGRO,(self.rect.centerx, self.rect.bottom), 6)
        lista_laser_enemigo.add(laser_sprite_enemigo)
        self.sonido_laser.play()
        

    def disparar_poder(self,lista_laser_enemigo):
        # Disparar laser doble
        laser_derecha_abajo = Laser("Nova-defender.main/imagenes/laser_final_boss.png",NEGRO,(self.rect.right - 15, self.rect.bottom - 10), 6)
        laser_izquierda_abajo = Laser("Nova-defender.main/imagenes/laser_final_boss.png",NEGRO,(self.rect.left + 15, self.rect.bottom - 10), 6)
        
        lista_laser_enemigo.add(laser_derecha_abajo)
        lista_laser_enemigo.add(laser_izquierda_abajo)
        self.sonido_laser.play()

    
        

    
       


