# Importar las librerias necesarias
import random
import pygame
from pygame import *

# Inicializar la libreria pygame. Esencial su llamado al trabajar con esta libreria
pygame.init()

# Crear y configurar pantalla de juego (900 width x 600 height).
pantalla = pygame.display.set_mode((900,600))

# Establecer imagen de fondo del juego
fondo = pygame.image.load('fondo.png')

# Establecer musica de fondo del juego
mixer.music.load("musica_fondo.wav")
mixer.music.play(-1) #REPRODUCE LA MUSICA, REPETIDA EN BUCLE

# TITULO E ICONO DEL JUEGO
pygame.display.set_caption("IRON-MAN GAME")
icono = pygame.image.load('icono.ico')
pygame.display.set_icon(icono)

# Movimiento del jugador y posicion
jugador_img = pygame.image.load('jugador.png')

# COORDENADAS INICIALES
jugadorX = 370
jugadorY = 480

# CONTROLA EL MOVIMIENTO LATERAL DEL JUGADOR
jugadorX_cambio = 0

# Establecer enemigo y movimientos del enemigo, y cantidad de enemigos
enemigo_img = [] # ALMACENA LAS IMAGENES DE LOS ENEMIGOS
enemigoX = []
enemigoY = []
enemigoX_cambio = []
enemigoY_cambio = []
num_de_enemigos = 6

# Movimientos del enemigo de izquierda a derecha (imagen 70x70 formato png)
# append() agrega elementos al final de una lista
for i in range(num_de_enemigos):
    enemigo_img.append(pygame.image.load('enemigo.png'))

    # Ubicacion aleatoria de los enemigos
    enemigoX.append(random.randint(0,736))
    enemigoY.append(random.randint(50,150))

    # VELOCIDAD DE MOVIMIENTO DEL ENEMIGO
    enemigoX_cambio.append(1)
    enemigoY_cambio.append(40)

# Establecer cohete o bala + movimiento vertical de la bala
bala_img = pygame.image.load('bala.png')
balas = []
balaY_cambio = 2 # Velocidad vertical de la bala

# Puntuacion del jugador
valor_puntuacion = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
textoX = 10
textoY = 10

# Pantalla final GameOver
fuente_game_over = pygame.font.Font('freesansbold.ttf', 64)

def mostrar_puntuacion(x, y):
    puntuacion = fuente.render("PUNTAJE : " + str(valor_puntuacion), True, (255,255,255))
    pantalla.blit(puntuacion, (x,y))

def texto_game_over():
    texto_game_over = fuente_game_over.render("GAME OVER", True, (255,255,255))
    pantalla.blit(texto_game_over, (200,250))

def jugador(x, y):
    pantalla.blit(jugador_img, (x,y))

def enemigo(x, y, i):
    pantalla.blit(enemigo_img[i], (x,y))

def disparar_bala(x, y):
    bala = {'x': x, 'y': y}
    balas.append(bala)

import math

def colision(enemigoX, enemigoY, balaX, balaY):
    distancia = math.sqrt(math.pow(enemigoX - balaX, 2) + (math.pow(enemigoY - balaY, 2)))
    if distancia < 27:
        return True
    else:
        return False
    
# Bucles del juego
jugando = True

while jugando:
    pantalla.fill((0,0,0)) # SE LLENA LA PANTALLA CON COLOR NEGRO
    pantalla.blit(fondo, (0,0)) # SE MUESTRA EL FONDO

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugadorX_cambio = -2

            if evento.key == pygame.K_RIGHT:
                jugadorX_cambio = 2

            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.wav")
                sonido_bala.play()
                balaX = jugadorX
                disparar_bala(balaX, jugadorY)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugadorX_cambio = 0;

    # Movimiento del jugador (dentro de bucles del juego)
    jugadorX += jugadorX_cambio

    # Que el jugador no se salga de la pantalla
    if jugadorX <= 0:
        jugadorX = 0
    elif jugadorX >= 736:
        jugadorX = 736

    # Movimientos de los enemigos y colision del impacto de la bala (dentro de bucles del juego)
    for i in range(num_de_enemigos):
        if enemigoY[i] > 440:
            for j in range(num_de_enemigos):
                enemigoY[j] = 2000
            texto_game_over()
            break
        
        enemigoX[i] += enemigoX_cambio[i]
        if enemigoX[i] <= 0:
            enemigoX_cambio[i] = 1 # Reducimos velocidad de movimiento horizontal de enemigos
            enemigoY[i] += enemigoY_cambio[i]
        elif enemigoX[i] >= 736:
            enemigoX_cambio[i] = -1
            enemigoY[i] += enemigoY_cambio[i]

        # Impacto de las balas en los enemigos + sonido de duracion 1 segundo max 2 segundos (en bucle)
        for bala in balas:
            # Declaraciones de depuración para examinar errores esta te identifica que parte esta funcionando mal en caso de algun inconveniente me escribes
            print(f"Enemigo X: {enemigoX[i]}, Enemigo Y: {enemigoY[i]}, Bala X: {bala['x']}, Bala Y: {bala['y']}")
            
            colisiona = colision(enemigoX[i], enemigoY[i], bala['x'], bala['y'])

            if colisiona:
                sonido_explosion = mixer.Sound("explosion.wav")
                sonido_explosion.play()
                balas.remove(bala)
                valor_puntuacion += 1
                enemigoX[i] = random.randint(0, 736)
                enemigoY[i] = random.randint(50, 150)
                break

        enemigo(enemigoX[i], enemigoY[i], i)

    # Movimiento y renderizado de las balas (dentro de bucles del juego)
    for bala in balas:
        bala['y'] -= balaY_cambio
        pantalla.blit(bala_img, (bala['x'] + 16, bala['y'] + 10))

    # Eliminar balas fuera de pantalla (dentro de bucles del juego)
    for bala in balas.copy():
        if bala['y'] <= 0:
            balas.remove(bala)

    # Mostrar jugador y puntuacion
    jugador(jugadorX, jugadorY)
    mostrar_puntuacion(textoX, textoY)
    pygame.display.update()