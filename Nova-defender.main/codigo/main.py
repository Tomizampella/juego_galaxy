import pygame
from colores import *
import random
from laser import *
from jugador import *
from alien import *


#Seteo basico
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1)

ANCHO_VENTANA = 450
ALTO_VENTANA = 700
FPS = 60

ventana = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
fondo = pygame.image.load("Nova-defender.main/imagenes/fondo_nivel_1.png")
clock = pygame.time.Clock() #Controlo FPS


#Seteo sonidos
musica_fondo = pygame.mixer.Sound("Nova-defender.main/audio/musica_fondo_2.mp3")
musica_fondo.set_volume(0.5)
musica_fondo.play(loops = -1) #Para que se repita en loop

explosion_meteorito = pygame.mixer.Sound("Nova-defender.main/audio/explosion_potente.mp3")
explosion_meteorito.set_volume(0.05)

sonido_laser_enemigo = pygame.mixer.Sound("Nova-defender.main/audio/sonido_laser_enemigo.mp3")
sonido_laser_enemigo.set_volume(0.05)

#Creacion de personaje
lista_todos_los_sprites = pygame.sprite.Group()
lista_meteoritos = pygame.sprite.Group()
lista_enemigos = pygame.sprite.Group()
lista_balas = pygame.sprite.Group()
lista_laser_enemigos = pygame.sprite.Group()
lista_player = pygame.sprite.Group()

player = Player(50,50,lista_todos_los_sprites)
lista_todos_los_sprites.add (player)


#Clase GAME (funciones por fuera de los sprites)
#Creacion enemigos
def crear_tres_filas_de_enemigos(cantidad_enemigos_por_fila):
    for i in range(cantidad_enemigos_por_fila):
        for j in range(1,4):
            enemigo = Enemigo(f"Nova-defender.main/imagenes/nave_enemigo_{j}.png", 53, 45, NEGRO)
            enemigo.rect.x = enemigo.rect.x + 60 * i + 1
            enemigo.rect.y = 100 + 100 * (j - 1)
            lista_enemigos.add(enemigo)
            lista_todos_los_sprites.add(enemigo)


#Creo funcion para el disparon enemigo aleatorio

def disparo_enemigo_aleatorio():
    if len(lista_enemigos) > 0:
        random_enemigo = choice(lista_enemigos.sprites())
        laser_sprite_enemigo = Laser(random_enemigo.rect.center, 6, ALTO_VENTANA)
        lista_todos_los_sprites.add(laser_sprite_enemigo)
        lista_laser_enemigos.add(laser_sprite_enemigo)
        sonido_laser_enemigo.play()

def chequear_colisiones():
    if len(lista_laser_enemigos) > 0:
        for laser in lista_laser_enemigos:
            lista_balas_a_player = pygame.sprite.spritecollide(player,lista_laser_enemigos, False)#false para que no desaparezca y respawnee arriba
            for _ in lista_balas_a_player:
                lista_todos_los_sprites.remove(laser)
                lista_laser_enemigos.remove(laser)
                player.score = player.score - 100
                player.salud = player.salud - 1
                explosion_meteorito.play()

    if len(player.lista_laser_player) > 0:
        for laser_player in player.lista_laser_player:
            lista_enemigos_explotados = pygame.sprite.spritecollide(laser_player,lista_enemigos, True)#false para que no desaparezca y respawnee arriba
            for _ in lista_enemigos_explotados:
                lista_todos_los_sprites.remove(laser_player)
                player.lista_laser_player.remove(laser_player)
                player.score = player.score + 100
                explosion_meteorito.play()

def dibujar_en_pantalla():
    ventana.blit(fondo, [0, 0])
    lista_todos_los_sprites.draw(ventana)

    # Texto SCORE
    fuente = pygame.font.Font("Nova-defender.main/fuentes/Pixeled.ttf", 10)
    texto_score = fuente.render(f"Score: {player.score}", True, ROJO)
    ventana.blit(texto_score, (0, 0))

    # Texto SALUD
    texto_salud = fuente.render(f"Salud: {player.salud}", True, ROJO)
    ventana.blit(texto_salud, (0, 20))

    # Texto TIEMPO
    texto_tiempo = fuente.render(f"Tiempo: {cronometro:.0f}", True, ROJO)
    ventana.blit(texto_tiempo, (0, 40))

    player.vidas_en_pantalla(ventana)
    pygame.display.flip()

#Creacion de enemigos y timer para disparos aleatorios
crear_tres_filas_de_enemigos(6)

timer_disparo_enemigo = pygame.USEREVENT + 0
pygame.time.set_timer(timer_disparo_enemigo,1000)

running = True
while running:
    cronometro = pygame.time.get_ticks() / 1000 #Divido por mil porque por default viene en milisegundos
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            running = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE: # para que se pueda tirar solo cuando se apreta el espacio
                player.disparar()
                
        if evento.type == pygame.USEREVENT: #Disparo enemigo
            if evento.type == timer_disparo_enemigo:
                disparo_enemigo_aleatorio()
                

    #Controles
    lista_teclas = pygame.key.get_pressed()

    if lista_teclas[pygame.K_LEFT] :
        player.update(-3)
    if lista_teclas[pygame.K_RIGHT] :
        player.update(3)
  
    #CHEQUEO DE COLISIONES
    chequear_colisiones()
    # print(len(lista_enemigos))
    lista_todos_los_sprites.update()

    dibujar_en_pantalla()

    clock.tick(FPS)

pygame.quit()