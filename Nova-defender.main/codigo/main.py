import pygame
from colores import *
import random
from laser import *
from jugador import *
from alien import *
import re
import sqlite3

#Seteo basico
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1)

#Seteo pantalla
ANCHO_VENTANA = 450
ALTO_VENTANA = 700
FPS = 60

ventana = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))

fondo_1 = pygame.image.load("Nova-defender.main/imagenes/fondo_nivel_1.png")
fondo_2 = pygame.image.load("Nova-defender.main/imagenes/fondo_nivel_2.png")
fondo_3 = pygame.image.load("Nova-defender.main/imagenes/fondo_nivel_3.png")

fondo = [fondo_1,fondo_2,fondo_3]

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

#Seteo variables niveles

nivel = 0
nivel_maximo = 3

#Creacion de grupos de sprites
lista_todos_los_sprites = pygame.sprite.Group()
lista_enemigos = pygame.sprite.Group()
lista_laser_enemigos = pygame.sprite.Group()
grupo_solo_final_boss = pygame.sprite.GroupSingle()

player = Player(50,50,lista_todos_los_sprites)

def nueva_partida():
    global nivel
    global player
    
    if lista_enemigos:
        eliminar_sprites_contenidos(lista_enemigos)
    elif nivel == nivel_maximo:
        pygame.sprite.Sprite.kill(final_boss)
    nivel = 0
    lista_todos_los_sprites.add(player)
    player.posicion_de_inicio()
    player.puntaje = 0
    player.bajas = 0




#Creacion enemigos
def crear_tres_filas_de_enemigos(cantidad_enemigos_por_fila):
    for i in range(cantidad_enemigos_por_fila):
        for j in range(1,4):
            enemigo = Enemigo(f"Nova-defender.main/imagenes/nave_enemigo_{j}.png", 53, 45, NEGRO,nivel,1)
            enemigo.rect.x = enemigo.rect.x + 60 * i + 1
            enemigo.rect.y = enemigo.rect.y + 100 * (j - 1)
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
        
        
        texto_subida_de_nivel = f"NIVEL {nivel}"
        dibujar_texto(ventana,texto_subida_de_nivel,ANCHO_VENTANA // 2, ALTO_VENTANA // 2)
        
        pygame.display.update()
        pygame.time.delay(2000)


    
#Creo funcion para el disparon enemigo aleatorio
def disparo_enemigo_aleatorio():
    if len(lista_enemigos) > 0:
        random_enemigo = choice(lista_enemigos.sprites())
        laser_sprite_enemigo = Laser("Nova-defender.main/imagenes/laser_enemigo.png",NEGRO,random_enemigo.rect.center, 6)
        lista_laser_enemigos.add(laser_sprite_enemigo)
        sonido_laser_enemigo.play()

def eliminar_sprites_contenidos(grupo_sprites):
    '''Vacia el grupo de sprites y el Sprite se elimina de todos los Grupos que lo contienen'''
    for sprite in grupo_sprites:
        pygame.sprite.Sprite.kill(sprite)

def eliminar_todos_los_lasers():
    '''Elimina todos los lasers cuando se sube de nivel'''
    eliminar_sprites_contenidos(lista_laser_enemigos)
    eliminar_sprites_contenidos(player.lista_laser_player)

def chequear_colisiones():
    #laser de alien a player
    if len(lista_laser_enemigos) > 0:
        for laser in lista_laser_enemigos:
            lista_balas_a_player = pygame.sprite.spritecollide(player,lista_laser_enemigos, False)#false para que no desaparezca y respawnee arriba
            for _ in lista_balas_a_player:
                lista_todos_los_sprites.remove(laser)
                lista_laser_enemigos.remove(laser)
                player.modificar_estadisticas(-1,-1) 
                explosion_meteorito.play()
         

    #laser de player a alien
    if len(player.lista_laser_player) > 0:
       

        for laser_player in player.lista_laser_player:
            colisiones = pygame.sprite.spritecollide(laser_player, lista_enemigos, False)
            for enemigo in colisiones:
                pygame.sprite.Sprite.kill(laser_player)
                enemigo.salud = enemigo.salud - 1
                player.modificar_estadisticas(1)
                if not player.poder_activado :
                    player.barra_poder = player.barra_poder + 1
                explosion_meteorito.play()
    
    if pygame.sprite.spritecollide(player, lista_enemigos, False) :
        player.salud = 0


def dibujar_marcadores_en_pantalla():
    if nivel <= nivel_maximo:
        ventana.blit(fondo[nivel -1],(0,0))
        lista_todos_los_sprites.draw(ventana)
        lista_laser_enemigos.draw(ventana)
    
    # Texto PUNTAJE
    texto_puntaje_ahora = f"PUNTAJE: {player.puntaje}"
    dibujar_texto(ventana,texto_puntaje_ahora,3, 0,False)
    
    # Texto TIEMPO
    texto_tiempo = f"TIEMPO: {cronometro:.0f}"
    dibujar_texto(ventana,texto_tiempo, ANCHO_VENTANA - 95 ,0,False)
    
    # Texto NIVEL
    texto_nivel = f"NIVEL: {nivel}"
    dibujar_texto(ventana,texto_nivel, ANCHO_VENTANA // 2,15)

    # Vidas player y Final boss
    player.dibujar_vida_poder(ventana)
    if nivel == nivel_maximo:
        final_boss.dibujar_barra_salud(ventana)
    

    pygame.display.flip()

#--------------------------------------------------

def dibujar_texto(screen, texto, x, y, generar_rectangulo = True, color = ROJO, tipo_letra = fuente):
        
        texto_superficie = tipo_letra.render(texto, True, color)
        if generar_rectangulo:
            texto_rect = texto_superficie.get_rect(center=(x, y))
            screen.blit(texto_superficie, texto_rect)
        else:

            screen.blit(texto_superficie,(x,y))

#---------------------------------------------------------------
def ventana_ingreso_nombre(ventana, clock):
    ventana.fill(NEGRO)
    
    
    waiting = True
    user_input = ""
    nombre_ingresado = False

    while waiting:
        clock.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if user_input and not nombre_ingresado: 
                        if re.match(r'^[a-zA-Z]{1,10}$', user_input):# Verificar que hay un nombre y no se haya ingresado antes
                            nombre_ingresado = True
                            waiting = False
                elif evento.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif len(user_input) < 10 and re.match(r'^[a-zA-Z]$', evento.unicode):
                    user_input += evento.unicode
        # Dibujar cuadro de entrada con fondo transparente
        input_rect = pygame.Rect(ANCHO_VENTANA // 2 - 100, ALTO_VENTANA // 2, 200, 32)
        pygame.draw.rect(ventana, (BLANCO), input_rect)
        pygame.draw.rect(ventana, (NEGRO), input_rect, 2)
        dibujar_texto(ventana, user_input, ANCHO_VENTANA // 2, (ALTO_VENTANA // 2) + 15 )
        dibujar_texto(ventana, "INGRESE SU NOMBRE", ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50)
        pygame.display.flip()

    return user_input

#-------------------------------------
def mostrar_opciones (en_menu_opciones):
    estado_musica = True
    while en_menu_opciones:
                    
                    ventana.fill(NEGRO)
                    if estado_musica:
                        estado_musica_text = fuente.render("MUSICA ON", True, ROJO)
                        pygame.mixer.unpause()
                    else:
                        estado_musica_text = fuente.render("MUSICA OFF", True, ROJO)
                        pygame.mixer.pause()
                        
                    ranking_historico_text = fuente.render("RANKING HISTORICO", True, ROJO)
                    volver_atras_text = fuente.render("VOLVER", True, ROJO)

                    estado_musica_rect = estado_musica_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 40))
                    ranking_historico_rect = ranking_historico_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 100))
                    volver_atras_rect = volver_atras_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 160))


                    ventana.blit(estado_musica_text, estado_musica_rect)
                    ventana.blit(ranking_historico_text, ranking_historico_rect)
                    ventana.blit(volver_atras_text, volver_atras_rect)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                        
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            posicion_mouse = event.pos
                            if estado_musica_rect.collidepoint(posicion_mouse) :# Clic en PLAY
                                estado_musica = not estado_musica
                            elif ranking_historico_rect.collidepoint(posicion_mouse):# Clic en salir
                                en_ranking = True
                                mostrar_ranking(en_ranking)
                            elif volver_atras_rect.collidepoint(posicion_mouse):
                                en_menu_opciones = False

                    pygame.display.update()
                    clock.tick(FPS)


#----------------------------------------

#MOSTRAR RANKING
def mostrar_ranking (en_ranking_historico):
    
    while en_ranking_historico:
                    
                    ventana.fill(NEGRO)
                    mostrar_top_5_en_pantalla(ventana)

                    #BOTON ATRAS
                    volver_atras_text = fuente.render("VOLVER", True, ROJO)
                    volver_atras_rect = volver_atras_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 160))
                    ventana.blit(volver_atras_text, volver_atras_rect)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                        
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            posicion_mouse = event.pos
                            if volver_atras_rect.collidepoint(posicion_mouse):
                                en_ranking_historico = False

                    pygame.display.update()
                    clock.tick(FPS)




#+---------------------------------------
#FUNCION BASE DE DATOS
def crear_tabla_ranking_puntajes():
    with sqlite3.connect("Nova-defender.main/codigo/ranking_puntajes.db") as conexion: # Conectarse a la base de datos (creará la base si no existe)
        try:

        # Crear la tabla si no existe
            sentencia = ('''CREATE TABLE puntajes 
                            (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nombre TEXT,
                                    puntaje INTEGER
                            )
                        ''')
            conexion.execute(sentencia)
            print("Se creo la tabla de puntajes")
        except sqlite3.OperationalError:
            print("La tabla de puntajes ya existe")

def guardar_puntaje(nombre_jugador, puntaje):
    with sqlite3.connect("Nova-defender.main/codigo/ranking_puntajes.db") as conexion:
        cursor = conexion.execute("SELECT nombre FROM puntajes WHERE nombre = ?", (nombre_jugador,))
        existe_nombre = cursor.fetchone()

        if existe_nombre:
            try:
                conexion.execute("UPDATE puntajes SET puntaje = ? WHERE nombre = ?", (puntaje, nombre_jugador))
                conexion.commit()
                
            except sqlite3.Error:
                print(f"Error al actualizar el puntaje de '{nombre_jugador}'")
        else:
            try:
                conexion.execute("INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)", (nombre_jugador, puntaje))
                conexion.commit()
                print("Se agregó el puntaje correctamente.")
            except sqlite3.Error :
                print(f"Error al insertar el puntaje de '{nombre_jugador}'")
            
def obtener_top_5_puntajes():
    with sqlite3.connect("Nova-defender.main/codigo/ranking_puntajes.db") as conexion:
        cursor = conexion.execute("SELECT nombre, puntaje FROM puntajes ORDER BY puntaje DESC LIMIT 5")
        top_5_puntajes = cursor.fetchall()  # Obtener los 5 mejores puntajes
        
            
        return top_5_puntajes
    
def mostrar_top_5_en_pantalla(ventana):
    top_5 = obtener_top_5_puntajes()
    tope_titulo = (ALTO_VENTANA // 2) - 200
    dibujar_texto(ventana,"RANKING HISTORICO",ANCHO_VENTANA// 2, tope_titulo)

    if top_5:
        separacion_en_y = 100
        for indice, puntaje in enumerate(top_5, start=1):
            nombre, score = puntaje
            texto_puntaje = f"{indice}. {nombre}: {score}"
            dibujar_texto(ventana,texto_puntaje,ANCHO_VENTANA// 2, tope_titulo + separacion_en_y)
            separacion_en_y = separacion_en_y + 50

def vaciar_tabla():
    try:
        with sqlite3.connect("Nova-defender.main/codigo/ranking_puntajes.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM puntajes")  # Elimina todas las filas de la tabla 'puntajes'
            conexion.commit()
            print("La tabla 'puntajes' ha sido vaciada.")
    except sqlite3.Error :
        print(f"Error al vaciar la tabla")


def operar_base_de_datos():
    crear_tabla_ranking_puntajes()
    guardar_puntaje(player.nombre,player.puntaje)
    
#----------------------------------------
timer_disparo_enemigo = pygame.USEREVENT + 0
pygame.time.set_timer(timer_disparo_enemigo,1000)



running = True
while running:

    
    en_menu_inicio = True
    while en_menu_inicio:
        
        partida_guardada = False
        en_opciones = False
        ventana.fill(NEGRO)

       
        #titulo juego
        fuente_titulo = pygame.font.Font("Nova-defender.main/fuentes/Pixeled.ttf", 30)
        texto_titulo = fuente_titulo.render("Nova Defender", True, ROJO)
        ventana.blit(texto_titulo, (40, ALTO_VENTANA // 4))


        #BOTONES
        jugar_text = fuente.render("JUGAR", True, ROJO)
        opciones_text = fuente.render("OPCIONES", True, ROJO)
        salir_text = fuente.render("SALIR", True, ROJO)


        jugar_rect = jugar_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 40))
        opciones_rect = opciones_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 100))
        salir_rect = salir_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 160))

        ventana.blit(jugar_text, jugar_rect)
        ventana.blit(opciones_text, opciones_rect)
        ventana.blit(salir_text, salir_rect)
        
        
        
        
        lista_eventos = pygame.event.get()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_mouse = evento.pos
                # Comprobar si el clic fue en los textos
                
                if jugar_rect.collidepoint(posicion_mouse) :# Clic en PLAY
                        player.nombre = ventana_ingreso_nombre(ventana,clock)
                        en_menu_inicio = False
                        en_partida = True
                        nueva_partida()
                elif salir_rect.collidepoint(posicion_mouse):# Clic en salir
                        quit()  # Clic en salir
                elif opciones_rect.collidepoint(posicion_mouse):# Clic en OPCIONES
                        en_opciones = True
                        mostrar_opciones(en_opciones)



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
                    if nivel == nivel_maximo:
                        final_boss.disparar(lista_laser_enemigos)
                    
        

        if player.salud <= 0:
            derrota = True
            en_partida = False
            juego_terminado = True
            
        if not lista_enemigos and not grupo_solo_final_boss:
            subir_nivel()
            
            if nivel <= 2:#Si no hay mas enemigos
                crear_tres_filas_de_enemigos(6)

            elif nivel == 3:#Si es nivel 3, entra el final boss
                final_boss = Enemigo("Nova-defender.main/imagenes/nave_enemigo_4.png", 116, 100, NEGRO,2,10)
                lista_enemigos.add(final_boss)
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
        lista_laser_enemigos.update()
        # lista_enemigos.update(ventana)#vida enemigos // #VER MIERCOLES

        dibujar_marcadores_en_pantalla()

        clock.tick(FPS)

    juego_terminado = True
    while juego_terminado:
        
        ventana.fill(NEGRO)
        
        # RESULTADO
        fuente_titulo = pygame.font.Font("Nova-defender.main/fuentes/Pixeled.ttf", 30)
        texto_nombre_jugador = fuente.render(f"--------    {player.nombre}    --------", True, ROJO)
        texto_puntaje_final = fuente.render(f"PUNTAJE FINAL: {player.puntaje}", True, ROJO)
        
        if victoria:
            texto_titulo = fuente_titulo.render("¡VICTORIA!", True, ROJO)
        elif derrota:
            texto_titulo = fuente_titulo.render("DERROTA", True, ROJO)
        
        ancho_texto_titulo = texto_titulo.get_width()
        ancho_texto_nombre = texto_nombre_jugador.get_width()
        ancho_texto_puntaje = texto_puntaje_final.get_width()

        x_titulo = (ANCHO_VENTANA - ancho_texto_titulo) // 2
        x_nombre = (ANCHO_VENTANA - ancho_texto_nombre) // 2
        x_puntaje = (ANCHO_VENTANA - ancho_texto_puntaje) // 2

        ventana.blit(texto_titulo, (x_titulo, 200))
        ventana.blit(texto_nombre_jugador, (x_nombre, 350))
        ventana.blit(texto_puntaje_final, (x_puntaje, 450))

        #BOTONES
        volver_a_jugar_text = fuente.render("VOLVER AL MENU", True, ROJO)
        salir_text = fuente.render("SALIR", True, ROJO)


        volver_a_jugar_rect = volver_a_jugar_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 200))
        salir_rect = salir_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 260))

        ventana.blit(volver_a_jugar_text, volver_a_jugar_rect)
        ventana.blit(salir_text, salir_rect)


        #EVENTOS
        lista_eventos = pygame.event.get()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                    posicion_mouse = evento.pos
                    # Comprobar si el clic fue en los textos
                    if volver_a_jugar_rect.collidepoint(posicion_mouse) :# Clic en PLAY
                        juego_terminado = False
                        en_partida = True
                        
                    elif salir_rect.collidepoint(posicion_mouse):# Clic en salir
                        quit()
        if not partida_guardada:
            operar_base_de_datos()
            partida_guardada = True
            
        clock.tick(FPS)
        pygame.display.update()

pygame.quit()