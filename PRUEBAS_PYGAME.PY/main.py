import pygame
from colores import *
import random

FPS = 60
#Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self,ancho,alto) -> None:
        super().__init__()
        self.image = pygame.image.load("nave_espacial.png").convert()
        self.image.set_colorkey(BLANCO) #le saco el color blanco de fondo
        self.image = pygame.transform.scale (self.image, (ancho,alto)) #escalo la imagen
        self.rect = self.image.get_rect() #obtengo el rectangulo a partir de la imagen
        self.rect.x = 200
        self.rect.y = 625
        self.score = 0

    def update (self, velocidad_x = 0): #seteo velocidad en cero si no rompe por no poder encontrarle el valor
        nueva_x = player.rect.x + velocidad_x
        if nueva_x < 400 and nueva_x > 0:
            player.rect.x = player.rect.x + velocidad_x
        
#Meteorito
class Meteorito (pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("meteorito.png").convert()
        self.image.set_colorkey(NEGRO) #le saco el color negro de fondo
        self.image = pygame.transform.scale (self.image, (30,30)) #escalo la imagen
        self.rect = self.image.get_rect() #obtengo el rectangulo a partir de la imagen

#Bala
class Bala (pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("bala.png").convert()
        self.image.set_colorkey(NEGRO) #le saco el color negro de fondo
        self.image = pygame.transform.scale (self.image, (25,25)) #escalo la imagen
        self.rect = self.image.get_rect() #obtengo el rectangulo a partir de la imagen

    def update (self):
        self.rect.y = self.rect.y - 5
        
#Seteo basico
pygame.init()

ANCHO_VENTANA = 450
ALTO_VENTANA = 700

ventana = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
clock = pygame.time.Clock() #Controlo FPS

fondo = pygame.image.load("fondo_nivel_1.png")

#Crecion de personaje
all_sprite_list = pygame.sprite.Group()
lista_meteoritos = pygame.sprite.Group()
lista_balas = pygame.sprite.Group()

player = Player(50,50)
all_sprite_list.add (player)

#creacion de meteoritos
for i in range(50):
    meteorito = Meteorito()
    meteorito.rect.x = random.randrange(420)
    meteorito.rect.y = random.randrange(500)

    lista_meteoritos.add(meteorito)
    all_sprite_list.add(meteorito)


running = True
while running:

    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            running = False
    

    #Controles
    lista_teclas = pygame.key.get_pressed()

    if lista_teclas[pygame.K_LEFT] :
        player.update(-3)
    if lista_teclas[pygame.K_RIGHT] :
        player.update(3)
    if lista_teclas[pygame.K_SPACE]:
        bala = Bala()
        bala.rect.x = player.rect.x  + 12 # +12 pixel para centrar la salida del laser
        bala.rect.y = player.rect.y 

        all_sprite_list.add(bala)
        lista_balas.add(bala)
        
    #LOGICA--------------------
    for bala in lista_balas:
        lista_meteoritos_explotados = pygame.sprite.spritecollide(bala,lista_meteoritos, True)
        for meteorito in lista_meteoritos_explotados:
            all_sprite_list.remove(bala)
            lista_balas.remove(bala)
            player.score = player.score + 100

        if bala.rect.y < -10:
            all_sprite_list.remove(bala)
            lista_balas.remove(bala)
           
    all_sprite_list.update()

    #COLOR DE FONDO------------
    ventana.blit(fondo,[0,0])

    #ZONA DE DIBUJO------------
    all_sprite_list.draw(ventana)

    #ACTUALIZAR PANTALLA------
    
    fuente = pygame.font.Font("Pixeled.ttf",10) #pygame.font.Font : crear un nuevo objeto de fuente a partir de un archivo
    texto = fuente.render(f"Score : {player.score}", True, ROJO)
    ventana.blit(texto,(0,0))

    pygame.display.flip()
    clock.tick(FPS) #Seteo FPS

pygame.quit()