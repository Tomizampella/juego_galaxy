import pygame
from colores import *
from random import choice
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
fuente = pygame.font.Font("Nova-defender.main/fuentes/Pixeled.ttf", 10)

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
lista_enemigos = pygame.sprite.Group()

grupo_solo_final_boss = pygame.sprite.GroupSingle()

player = Player(50,50,lista_todos_los_sprites)




#Seteo variables niveles

nivel = 0
nivel_maximo = 3
lista_enemigos_por_indice = []

#Clase GAME (funciones por fuera de los sprites)
#Creacion enemigos
def crear_tres_filas_de_enemigos(cantidad_enemigos_por_fila):
    for i in range(cantidad_enemigos_por_fila):
        for j in range(1,4):
            global enemigo
            enemigo = Enemigo(f"Nova-defender.main/imagenes/nave_enemigo_{j}.png", 53, 45, NEGRO,nivel,lista_todos_los_sprites)
            enemigo.rect.x = enemigo.rect.x + 60 * i + 1
            enemigo.rect.y = enemigo.rect.y + 100 * (j - 1)
            lista_enemigos_por_indice.append(enemigo)
            lista_enemigos.add(enemigo)
            lista_todos_los_sprites.add(enemigo)
            



#Creo funcion para subir nivel
def subir_nivel():
    global nivel
    nivel = nivel + 1
    if nivel <= nivel_maximo:
        player.posicion_de_inicio()
        eliminar_todos_los_lasers()
        
        ventana.fill(NEGRO)
        
        
        texto_subida_de_nivel = fuente.render(f"NIVEL {nivel}", True, ROJO)
        
        ventana.blit(texto_subida_de_nivel, (200, 350))
        pygame.display.update()
        pygame.time.delay(2000)

def nueva_partida():
    global nivel
    nivel = 0
    if lista_enemigos:
        for enemigos in lista_enemigos:
            pygame.sprite.Sprite.kill(enemigos)
    lista_todos_los_sprites.add(player)
    player.posicion_de_inicio()
    player.score = 0
    

    
#Creo funcion para el disparon enemigo aleatorio
def disparo_enemigo_aleatorio():
    if len(lista_enemigos) > 0:
        enemigo_aleatorio = choice(lista_enemigos_por_indice)
        enemigo_aleatorio.disparar()
        

def eliminar_todos_los_lasers():
    '''Elimina todos los lasers cuando se sube de nivel'''
    if enemigo.lista_laser_enemigo:
        for laser in enemigo.lista_laser_enemigo:
            pygame.sprite.Sprite.kill(laser)
    
    for bala in player.lista_laser_player:
        pygame.sprite.Sprite.kill(bala)

def chequear_colisiones():
    #laser de alien a player
    
    if len(enemigo.lista_laser_enemigo) > 0:
        for laser in enemigo.lista_laser_enemigo:
            lista_balas_a_player = pygame.sprite.spritecollide(player,enemigo.lista_laser_enemigo, True)#false para que no desaparezca y respawnee arriba
            for _ in lista_balas_a_player:
                lista_todos_los_sprites.remove(laser)
                enemigo.lista_laser_enemigo.remove(laser)
                player.score = player.score - 100
                player.salud = player.salud - 1
                explosion_meteorito.play()

    #laser de player a alien
    if len(player.lista_laser_player) > 0:
        for laser_player in player.lista_laser_player:
            lista_enemigos_explotados = pygame.sprite.spritecollide(laser_player,lista_enemigos, True)#false para que no desaparezca y respawnee arriba
            lista_laser_player_a_final_boss = pygame.sprite.spritecollide(laser_player,grupo_solo_final_boss, False)
            if lista_enemigos_explotados:
                for _ in lista_enemigos_explotados:
                    lista_todos_los_sprites.remove(laser_player)
                    player.lista_laser_player.remove(laser_player)
                    player.score = player.score + 100
                    explosion_meteorito.play()
            
            if lista_laser_player_a_final_boss:
                for _ in lista_laser_player_a_final_boss:
                    lista_todos_los_sprites.remove(laser_player)
                    player.lista_laser_player.remove(laser_player)
                    player.score = player.score + 100
                    final_boss.salud = final_boss.salud - 1 
                    explosion_meteorito.play()

def dibujar_en_marcadores_pantalla():
    ventana.blit(fondo, [0, 0])
    lista_todos_los_sprites.draw(ventana)
    # lista_enemigos.draw(ventana)#vida enemigos // #VER MIERCOLES
    
    # Texto SCORE
    texto_score = fuente.render(f"SCORE: {player.score}", True, ROJO)
    ventana.blit(texto_score, (0, 0))

    # Texto SALUD
    texto_salud = fuente.render(f"SALUD: {player.salud}", True, ROJO)
    ventana.blit(texto_salud, (0, 20))

    # Texto TIEMPO
    texto_tiempo = fuente.render(f"TIEMPO: {cronometro:.0f}", True, ROJO)
    ventana.blit(texto_tiempo, (0, 40))

    # Texto NIVEL
    texto_nivel = fuente.render(f"NIVEL: {nivel}", True, ROJO)
    ventana.blit(texto_nivel, (0, 60))

    player.vidas_en_pantalla(ventana)
    if grupo_solo_final_boss:
        final_boss.dibujar_barra_salud(ventana)
    

    pygame.display.flip()
    


timer_disparo_enemigo = pygame.USEREVENT + 0
pygame.time.set_timer(timer_disparo_enemigo,1000)

running = True
while running:

    en_menu_inicio = True
    while en_menu_inicio:
        
        ventana.fill(NEGRO)

        fuente_titulo = pygame.font.Font("Nova-defender.main/fuentes/Pixeled.ttf", 30)
        texto_titulo = fuente_titulo.render("Nova Defender", True, ROJO)
        texto_instrucciones = fuente.render("Press ENTER to play // S to exit", True, ROJO)

        ventana.blit(texto_titulo, (40, 200))
        ventana.blit(texto_instrucciones, (80, 500))
        
        lista_eventos = pygame.event.get()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                quit()

        lista_teclas = pygame.key.get_pressed()

        if lista_teclas[pygame.K_RETURN]:

            en_menu_inicio = False
            en_partida = True
            nueva_partida()

        if lista_teclas[pygame.K_s]:
            quit()


        clock.tick(FPS)
        pygame.display.update()


    en_partida = True
    while en_partida:
        victoria = False
        derrota = False
        cronometro = pygame.time.get_ticks() / 1000 #Divido por mil porque por default viene en milisegundos
        lista_eventos = pygame.event.get()

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE: # para que se pueda tirar solo cuando se apreta el espacio
                    player.disparar()
                    
            if evento.type == pygame.USEREVENT: #Disparo enemigo
                if evento.type == timer_disparo_enemigo:
                    disparo_enemigo_aleatorio()
                    if grupo_solo_final_boss:
                        final_boss.disparar()
                    
        

        if player.salud <= 0:
            derrota = True
            en_partida = False
            juego_terminado = True
            
        if not lista_enemigos and not grupo_solo_final_boss:
            subir_nivel()
            
            if nivel <= 2:#Si no hay mas enemigos
                crear_tres_filas_de_enemigos(6)
            elif nivel == 3:
                final_boss = Enemigo("Nova-defender.main/imagenes/nave_enemigo_2.png", 106, 90, NEGRO,nivel,lista_todos_los_sprites)
                grupo_solo_final_boss.add(final_boss)
                lista_todos_los_sprites.add(final_boss)
            elif nivel > nivel_maximo:
                victoria = True
                en_partida = False
                juego_terminado = True
            
        
            
        

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
        # lista_enemigos.update(ventana)#vida enemigos // #VER MIERCOLES

        dibujar_en_marcadores_pantalla()

        clock.tick(FPS)

    juego_terminado = True
    while juego_terminado:
        
        ventana.fill(NEGRO)
        
        fuente_titulo = pygame.font.Font("Nova-defender.main/fuentes/Pixeled.ttf", 30)
        texto_puntaje_final = fuente.render(f"PUNTAJE FINAL: {player.score}", True, ROJO)
        texto_instrucciones = fuente.render("Press ENTER to play // S to exit", True, ROJO)
        
        if victoria:
            texto_titulo = fuente_titulo.render("¡VICTORIA!", True, ROJO)
        elif derrota:
            texto_titulo = fuente_titulo.render("DERROTA", True, ROJO)

        ventana.blit(texto_titulo, (110, 200))
        ventana.blit(texto_puntaje_final, (130, 450))
        ventana.blit(texto_instrucciones, (80, 500))
        
        lista_eventos = pygame.event.get()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                quit()

        lista_teclas = pygame.key.get_pressed()

        if lista_teclas[pygame.K_RETURN]:
            juego_terminado = False
            en_partida = True
            nueva_partida()

        if lista_teclas[pygame.K_s]:
            quit()


        clock.tick(FPS)
        pygame.display.update()

pygame.quit()