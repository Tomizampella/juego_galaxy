import pygame
from colores import *
import random
from laser import *
from jugador import *
from alien import *
import re
import sqlite3
from main import *

def nueva_partida():
    global nivel
    global player
    
    if lista_enemigos:
        eliminar_sprites_contenidos(lista_enemigos)
        lista_todos_los_sprites.empty()
    elif nivel == nivel_maximo:
        pygame.sprite.Sprite.kill(final_boss)
    nivel = 0
    lista_todos_los_sprites.add(player)
    player.posicion_de_inicio()
    player.puntaje = 0
    player.barra_poder = 0