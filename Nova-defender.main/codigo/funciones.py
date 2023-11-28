import pygame
from colores import *
import random
from clase_laser import *
from clase_jugador import *
from clase_alien import *
import re
import sqlite3

ANCHO_VENTANA = 450
ALTO_VENTANA = 700


def nueva_partida(lista_enemigos,lista_todos_los_sprites,lista_enemigos_por_indice,nivel,nivel_maximo,player):
    '''Restablece los valores de inicio para comenzar una nueva partida'''

    # Vaciar listas
    if lista_enemigos:
        eliminar_sprites_contenidos(lista_enemigos)
        lista_todos_los_sprites.empty()
        lista_enemigos_por_indice.clear()
    elif nivel == nivel_maximo:
        pygame.sprite.Sprite.kill(final_boss)
    
    # Valores predeterminados
    player.nueva_partida()
    lista_todos_los_sprites.add(player)


def subir_nivel(ventana,fuente,lista_laser_enemigos,nivel,nivel_maximo,player):
    '''Restablece los valores para aumentar de nivel y muestra pantalla de carga con el nivel aumentado'''

    if nivel <= nivel_maximo:
        player.posicion_de_inicio()
        eliminar_todos_los_lasers(lista_laser_enemigos,player)
        ventana.fill(NEGRO)
        texto_subida_de_nivel = f"NIVEL {nivel}"
        dibujar_texto(ventana,texto_subida_de_nivel,ANCHO_VENTANA // 2, ALTO_VENTANA // 2,fuente)
        
        pygame.display.update()
        pygame.time.delay(2000)


def crear_tres_filas_de_enemigos(cantidad_enemigos_por_fila,lista_enemigos,lista_enemigos_por_indice,lista_todos_los_sprites,nivel):
    '''Crea 3 filas de enemigos con la cantidad sprites por fila que se le pase por parametro '''

    for i in range(cantidad_enemigos_por_fila):
        for j in range(1,4):
            enemigo = Enemigo(f"Nova-defender.main/imagenes/nave_enemigo_{j}.png", 53, 45, NEGRO,nivel,1)
            enemigo.rect.x = enemigo.rect.x + 60 * i + 1
            enemigo.rect.y = enemigo.rect.y + 100 * (j - 1)
            lista_enemigos_por_indice.append(enemigo)
            lista_enemigos.add(enemigo)
            lista_todos_los_sprites.add(enemigo)


def crear_final_boss(lista_enemigos,lista_todos_los_sprites):
    '''Crea final boss y lo retorna'''

    global final_boss
    final_boss = Enemigo("Nova-defender.main/imagenes/nave_enemigo_4.png", 116, 100, NEGRO,2,10)
    lista_enemigos.add(final_boss)
    lista_todos_los_sprites.add(final_boss)
    return final_boss
            

def disparo_enemigo_aleatorio(lista_enemigos,lista_enemigos_por_indice,lista_laser_enemigos):
    '''Si hay enemigos, elige 1 enemigo de la lista_enemigos y llama al metodo disparar() del objeto enemigo'''

    if len(lista_enemigos) > 0:
        enemigo_aleatorio = choice(lista_enemigos_por_indice)
        enemigo_aleatorio.disparar(lista_laser_enemigos)


def eliminar_sprites_contenidos(grupo_sprites):
    '''Vacia el grupo de sprites y el Sprite se elimina de todos los Grupos que lo contienen'''
    for sprite in grupo_sprites:
        pygame.sprite.Sprite.kill(sprite)

def eliminar_todos_los_lasers(lista_laser_enemigos,player):
    '''Elimina todos los lasers cuando se sube de nivel'''
    eliminar_sprites_contenidos(lista_laser_enemigos)
    eliminar_sprites_contenidos(player.lista_laser_player)

def chequear_colisiones(lista_laser_enemigos,lista_todos_los_sprites,explosion_nave,lista_enemigos,lista_enemigos_por_indice,player):
    # Colision laser de enemigo a player
    if len(lista_laser_enemigos) > 0:
        for laser in lista_laser_enemigos:
            lista_balas_a_player = pygame.sprite.spritecollide(player,lista_laser_enemigos, False)#false para que no desaparezca y respawnee arriba
            for _ in lista_balas_a_player:
                lista_todos_los_sprites.remove(laser)
                lista_laser_enemigos.remove(laser)
                player.modificar_estadisticas(-1,-1) 
                explosion_nave.play()
         
    # Colision laser de player a enemigo
    if len(player.lista_laser_player) > 0:

        for laser_player in player.lista_laser_player:
            colisiones = pygame.sprite.spritecollide(laser_player, lista_enemigos, False)
            for enemigo in colisiones:
                pygame.sprite.Sprite.kill(laser_player)
                enemigo.salud = enemigo.salud - 1
                player.modificar_estadisticas(1)
                if not player.poder_activado :
                    player.barra_poder = player.barra_poder + 1
                explosion_nave.play()

                if enemigo in lista_enemigos_por_indice:
                    lista_enemigos_por_indice.remove(enemigo)
                    
    # Colision entre player y enemigo
    if pygame.sprite.spritecollide(player, lista_enemigos, False) :
        player.salud = 0


def dibujar_marcadores_en_pantalla(ventana,fondo,lista_todos_los_sprites,lista_laser_enemigos,nivel,nivel_maximo,player,cronometro,fuente):
    '''Dibuja en pantalla todas las estadisticas al momento'''
    if nivel <= nivel_maximo:
        ventana.blit(fondo[nivel -1],(0,0))
        lista_todos_los_sprites.draw(ventana)
        lista_laser_enemigos.draw(ventana)
    
    # Texto PUNTAJE
    texto_puntaje_ahora = f"PUNTAJE: {player.puntaje}"
    dibujar_texto(ventana,texto_puntaje_ahora,3, 0,fuente,False)
    
    # Texto TIEMPO
    texto_tiempo = f"TIEMPO: {cronometro:.0f}"
    dibujar_texto(ventana,texto_tiempo, ANCHO_VENTANA - 95 ,0,fuente,False)
    
    # Texto NIVEL
    texto_nivel = f"NIVEL: {nivel}"
    dibujar_texto(ventana,texto_nivel, ANCHO_VENTANA // 2,15,fuente)

    # Vidas player y Final boss
    player.dibujar_vida_poder(ventana)
    if nivel == nivel_maximo:
        final_boss.dibujar_barra_salud(ventana)
    

def dibujar_texto(screen, texto, x, y, tipo_letra, generar_rectangulo = True ,color = ROJO):
    '''Dibuja en pantalla el texto que se le pase por parametro'''
    texto_superficie = tipo_letra.render(texto, True, color)
    if generar_rectangulo:
        texto_rect = texto_superficie.get_rect(center=(x, y))
        screen.blit(texto_superficie, texto_rect)
    else:

        screen.blit(texto_superficie,(x,y))


def mostrar_resultado_partida(victoria,ventana,fuente_titulo,fuente,player):
    '''Dibuja en pantalla todas las estadisticas finales'''
    texto_nombre_jugador = f"--------    {player.nombre}    --------"
    texto_puntaje_final = f"PUNTAJE FINAL: {player.puntaje}"
        
    if victoria:
        texto_titulo = "¡VICTORIA!"
    else:
        texto_titulo = "DERROTA"
        
    dibujar_texto(ventana, texto_titulo, ANCHO_VENTANA //2, 200, fuente_titulo)
    dibujar_texto(ventana,texto_nombre_jugador, ANCHO_VENTANA //2, 350,fuente)
    dibujar_texto(ventana,texto_puntaje_final, ANCHO_VENTANA //2, 450,fuente)


def ventana_ingreso_nombre(ventana, clock, fuente):
    '''Bucle para ingresar nombre del jugador, lo retorna al presionar ENTER'''
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
                        if re.match(r'^[a-zA-Z]{1,10}$', user_input):# Verificacion
                            nombre_ingresado = True
                            waiting = False
                elif evento.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif len(user_input) < 10 and re.match(r'^[a-zA-Z]$', evento.unicode):
                    user_input += evento.unicode
        
        # Dibujar en pantalla
        input_rect = pygame.Rect(ANCHO_VENTANA // 2 - 100, ALTO_VENTANA // 2, 200, 32)
        pygame.draw.rect(ventana, (BLANCO), input_rect)
        pygame.draw.rect(ventana, (NEGRO), input_rect, 2)
        dibujar_texto(ventana, user_input, ANCHO_VENTANA // 2, (ALTO_VENTANA // 2) + 15,fuente)
        dibujar_texto(ventana, "INGRESE SU NOMBRE", ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50,fuente)
        
        pygame.display.flip()

    return user_input


def mostrar_opciones (en_menu_opciones,ventana,fuente,clock,FPS):
    '''Bucle para mostrar opciones'''
    estado_musica = True
    while en_menu_opciones:
                    
                    # Dibujar en pantalla
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

                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            quit()
                        
                        elif evento.type == pygame.MOUSEBUTTONDOWN:
                            posicion_mouse = evento.pos
                            if estado_musica_rect.collidepoint(posicion_mouse) :# Clic en PLAY
                                estado_musica = not estado_musica
                            elif ranking_historico_rect.collidepoint(posicion_mouse):# Clic en salir
                                en_ranking = True
                                mostrar_ranking(en_ranking,ventana,fuente,clock,FPS)
                            elif volver_atras_rect.collidepoint(posicion_mouse):
                                en_menu_opciones = False

                    pygame.display.update()
                    clock.tick(FPS)



def mostrar_ranking (en_ranking_historico,ventana,fuente,clock,FPS):
    '''Bucle para mostrar top 5 mejores puntajes'''
    while en_ranking_historico:
                    
                    # Dibujar en pantalla
                    ventana.fill(NEGRO)
                    mostrar_top_5_en_pantalla(ventana,fuente)

                    # Boton atras
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


# Funciones base de datos
def crear_tabla_ranking_puntajes():
    '''Crea la tabla de puntajes si no existe'''
    
    with sqlite3.connect("Nova-defender.main/codigo/ranking_puntajes.db") as conexion:
        try:

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
    '''Guarda le puntaje en la base de datos, si ya existe el nombre, solo lo actualiza'''

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
    '''Toma los mejores 5 puntajes y los retorna en una lista de tuplas (nombre,puntaje)'''

    with sqlite3.connect("Nova-defender.main/codigo/ranking_puntajes.db") as conexion:
        try:
            cursor = conexion.execute("SELECT nombre, puntaje FROM puntajes ORDER BY puntaje DESC LIMIT 5")
            top_5_puntajes = cursor.fetchall()  
            
            return top_5_puntajes
        except sqlite3.OperationalError:
            print("La tabla de puntajes esta vacia")
    
def mostrar_top_5_en_pantalla(ventana,fuente):
    '''Muestra en pantalla los mejores 5 puntajes'''

    top_5 = obtener_top_5_puntajes()
    tope_titulo = (ALTO_VENTANA // 2) - 200
    dibujar_texto(ventana,"RANKING HISTORICO",ANCHO_VENTANA// 2, tope_titulo,fuente)

    if top_5:
        separacion_en_y = 100
        for indice, puntaje in enumerate(top_5, start=1):
            nombre, score = puntaje
            nombre = nombre.upper()
            texto_puntaje = f"{indice}-  {nombre}:  {score}"
            dibujar_texto(ventana,texto_puntaje,ANCHO_VENTANA// 2, tope_titulo + separacion_en_y,fuente)
            separacion_en_y = separacion_en_y + 50

def vaciar_tabla():
    '''Elimina todas las filas de la tabla PUNTAJES'''

    try:
        with sqlite3.connect("Nova-defender.main/codigo/ranking_puntajes.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM puntajes") 
            conexion.commit()
            print("La tabla 'puntajes' ha sido vaciada.")
    except sqlite3.Error :
        print(f"Error al vaciar la tabla")


def operar_base_de_datos(player):
    '''Crea tabla puntajes y guarda puntaje del jugador'''

    crear_tabla_ranking_puntajes()
    guardar_puntaje(player.nombre,player.puntaje)
    
