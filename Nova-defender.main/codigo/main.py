import pygame
from colores import *
from clase_laser import *
from clase_jugador import *
from clase_alien import *
from funciones import *

# TP Segundo Parcial - Tomás Diaz Zampella

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1)

# Configuracion pantalla
ANCHO_VENTANA = 450
ALTO_VENTANA = 700
FPS = 60
ventana = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
clock = pygame.time.Clock() #Controlo FPS

fondo_1 = pygame.image.load("Nova-defender.main/imagenes/fondo_nivel_1.png")
fondo_2 = pygame.image.load("Nova-defender.main/imagenes/fondo_nivel_2.png")
fondo_3 = pygame.image.load("Nova-defender.main/imagenes/fondo_nivel_3.png")
fondo = [fondo_1,fondo_2,fondo_3]

# Fuentes
fuente = pygame.font.Font("Nova-defender.main/fuentes/Pixeled.ttf", 10)
fuente_titulo = pygame.font.Font("Nova-defender.main/fuentes/Pixeled.ttf", 30)

# Seteo sonidos
musica_fondo = pygame.mixer.Sound("Nova-defender.main/audio/musica_fondo_2.mp3")
musica_fondo.set_volume(0.5)
musica_fondo.play(loops = -1) #Para que se repita en loop

explosion_nave = pygame.mixer.Sound("Nova-defender.main/audio/explosion_potente.mp3")
explosion_nave.set_volume(0.05)

# Seteo variables niveles
nivel = 0
nivel_maximo = 3

# Creacion de grupos de sprites
lista_todos_los_sprites = pygame.sprite.Group()
lista_enemigos = pygame.sprite.Group()
lista_laser_enemigos = pygame.sprite.Group()
lista_enemigos_por_indice = []

# Creacion player sprite
player = Player(50,50,lista_todos_los_sprites)


# Timer
timer_disparo_enemigo = pygame.USEREVENT + 0
pygame.time.set_timer(timer_disparo_enemigo,1000)


# Variable de control Bucle principal
running = True

# BUCLE PRINCIPAL
while running:

    # Variable de control menu de inicio
    en_menu_inicio = True

    # Bucle en menu de inicio
    while en_menu_inicio:

        # Variables de control
        partida_guardada = False
        en_opciones = False
        flag_final_boss_creado = False

        # Dibujar en pantalla
        ventana.fill(NEGRO)
        texto_titulo = "Nova Defender"
        dibujar_texto(ventana, texto_titulo, ANCHO_VENTANA //2, 200, fuente_titulo,True)

        # Botones
        jugar_text = fuente.render("JUGAR", True, ROJO)
        opciones_text = fuente.render("OPCIONES", True, ROJO)
        salir_text = fuente.render("SALIR", True, ROJO)

        jugar_rect = jugar_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 40))
        opciones_rect = opciones_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 100))
        salir_rect = salir_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 160))

        ventana.blit(jugar_text, jugar_rect)
        ventana.blit(opciones_text, opciones_rect)
        ventana.blit(salir_text, salir_rect)
        
        
        # Control de eventos
        lista_eventos = pygame.event.get()

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_mouse = evento.pos
                if jugar_rect.collidepoint(posicion_mouse) :# Clic en JUGAR
                        player.nombre = ventana_ingreso_nombre(ventana,clock,fuente)
                        en_menu_inicio = False
                        en_partida = True
                        nueva_partida(lista_enemigos,lista_todos_los_sprites,lista_enemigos_por_indice,nivel,nivel_maximo,player)
                elif opciones_rect.collidepoint(posicion_mouse):# Clic en OPCIONES
                        en_opciones = True
                        mostrar_opciones(en_opciones,ventana,fuente,clock,FPS)
                elif salir_rect.collidepoint(posicion_mouse):# Clic en SALIR
                        quit()  

        # Actualizar pantalla
        clock.tick(FPS)
        pygame.display.update()
        

    # BUCLE PARTIDA COMENZADA
    while en_partida:

        # Variables de control
        victoria = False

        # Control del tiempo
        cronometro = pygame.time.get_ticks() / 1000 
        
        # Control de eventos
        lista_eventos = pygame.event.get()

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                quit()    
            elif evento.type == pygame.USEREVENT: #Disparo enemigo
                if evento.type == timer_disparo_enemigo:
                    if nivel < nivel_maximo:
                        disparo_enemigo_aleatorio(lista_enemigos,lista_enemigos_por_indice,lista_laser_enemigos)
                    elif flag_final_boss_creado:
                        final_boss.disparar_poder(lista_laser_enemigos)
                    
        
        # Logica del juego
        if player.salud <= 0:
            
            en_partida = False
            partida_terminada = True
            
        if not lista_enemigos:
            nivel = nivel + 1
            subir_nivel(ventana,fuente,lista_laser_enemigos,nivel,nivel_maximo,player)
            if nivel <= 2:
                crear_tres_filas_de_enemigos(6,lista_enemigos,lista_enemigos_por_indice,lista_todos_los_sprites,nivel)
            elif nivel == nivel_maximo:
                final_boss = crear_final_boss(lista_enemigos,lista_todos_los_sprites)
                flag_final_boss_creado = True
            elif nivel > nivel_maximo:
                victoria = True
                en_partida = False
                partida_terminada = True
            
        # Controles
        lista_teclas = pygame.key.get_pressed()

        if lista_teclas[pygame.K_LEFT] :
            player.update(-3)
        elif lista_teclas[pygame.K_RIGHT] :
            player.update(3)
        elif lista_teclas[pygame.K_SPACE] :
            player.disparar()
    
        # Chequeo colisiones
        chequear_colisiones(lista_laser_enemigos,lista_todos_los_sprites,explosion_nave,lista_enemigos,lista_enemigos_por_indice,player)

        # Dibujar en pantalla
        dibujar_marcadores_en_pantalla(ventana,fondo,lista_todos_los_sprites,lista_laser_enemigos,nivel,nivel_maximo,player,cronometro,fuente)
        
        # Actualizar pantalla
        lista_todos_los_sprites.update() 
        lista_laser_enemigos.update()
        clock.tick(FPS)
        pygame.display.flip()


    # BUCLE PARTIDA TERMINADA
    while partida_terminada:
        
        # Dibujar en pantalla
        ventana.fill(NEGRO)
        mostrar_resultado_partida(victoria,ventana,fuente_titulo,fuente,player)

        # Botones
        volver_al_menu_text = fuente.render("VOLVER AL MENU", True, ROJO)
        salir_text = fuente.render("SALIR", True, ROJO)

        volver_al_menu_rect = volver_al_menu_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 200))
        salir_rect = salir_text.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 260))

        ventana.blit(volver_al_menu_text, volver_al_menu_rect)
        ventana.blit(salir_text, salir_rect)


        # Control de eventos
        lista_eventos = pygame.event.get()

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                    posicion_mouse = evento.pos
                    if volver_al_menu_rect.collidepoint(posicion_mouse) :# Clic en VOLVER AL MANU
                        partida_terminada = False
                        en_partida = True
                        nueva_partida(lista_enemigos,lista_todos_los_sprites,lista_enemigos_por_indice,nivel,nivel_maximo,player)
                        nivel = 0
                    elif salir_rect.collidepoint(posicion_mouse):# Clic en SALIR
                        quit()

        # Guardar resultado      
        if not partida_guardada:
            operar_base_de_datos(player)
            partida_guardada = True

        # Actualizar pantalla
        clock.tick(FPS)
        pygame.display.update()

pygame.quit()