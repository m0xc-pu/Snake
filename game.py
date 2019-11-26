import pygame
import random
import time
import sys
pygame.init()

# definicion de colores
blanco = pygame.Color(255,255,255)
negro = pygame.Color(0,0,0)
rojo = pygame.Color(255,0,0)
rojo_o = pygame.Color(100,0,0)
gris = pygame.Color(200,200,200)
verde = pygame.Color(0,250,100)
verde_o = pygame.Color(0,150,50)
morado = pygame.Color(126, 21, 175)

# tamano ventana
winSizeX = 1000
winSizeY = 600
# tamano serpiente
tam_serp = 25
# nombre de la ventana
titulo_ventana = "Snake!    Ver 2.2    By: moxwel"

# propiedades ventana
pantalla = pygame.display.set_mode((winSizeX,winSizeY))
pygame.display.set_caption(titulo_ventana)
icono_juego = pygame.image.load("resources/img/snake_icon.gif")
pygame.display.set_icon(icono_juego)
reloj = pygame.time.Clock()

# funcion para renderizar texto con bordes (predeterminado = sin bordes)
def render_text(texto, color, tam, x=0, y=0, grosor=0, color_grosor=(255,255,255)):
    fuente = pygame.font.Font("resources/determination.ttf",tam)
    texto_out = fuente.render(texto, True, color_grosor, None)
    texto = fuente.render(texto, True, color, None)
    pantalla.blit(texto_out,(x+grosor,y+grosor))
    pantalla.blit(texto_out,(x+grosor,y-grosor))
    pantalla.blit(texto_out,(x-grosor,y+grosor))
    pantalla.blit(texto_out,(x-grosor,y-grosor))
    pantalla.blit(texto_out,(x+grosor,y))
    pantalla.blit(texto_out,(x-grosor,y))
    pantalla.blit(texto_out,(x,y+grosor))
    pantalla.blit(texto_out,(x,y-grosor))
    pantalla.blit(texto,(x,y))

render_text("Cargando . . .",blanco,40,20,10)
pygame.display.update()

# imagenes y sonidos (cargar antes del main_game para optimizar cargas)
go_image = pygame.transform.scale(pygame.image.load("resources/img/game_over.png"),(winSizeX,winSizeY))
pause_image = pygame.transform.scale(pygame.image.load("resources/img/pause.png"),(winSizeX,winSizeY))
musica = pygame.mixer.Sound("resources/music/music.ogg")
comer = pygame.mixer.Sound("resources/music/apple.ogg")
comer2 = pygame.mixer.Sound("resources/music/apple2.ogg")
comer3 = pygame.mixer.Sound("resources/music/apple3.ogg")
crash = pygame.mixer.Sound("resources/music/crash.ogg")
crash2 = pygame.mixer.Sound("resources/music/crash2.ogg")
keys = pygame.image.load("resources/img/keys.png")
gameover_music = pygame.mixer.Sound("resources/music/gameover.ogg")

# pantalla de inicio del juego
def intro_juego():
    print("[Intro] Bienvenido a Snake!")

    intro_state = True
    pantalla.blit(pause_image,(0,0))

    render_text(titulo_ventana,negro,20,3,1,)
    render_text("El objetivo principal del juego es",blanco,30,50,220,2,negro)
    render_text("lograr que la serpiente se coma",blanco,30,50,250,2,negro)
    render_text("todas las manzanas posibles.",blanco,30,50,280,2,negro)

    render_text("Si la serpiente sale del escenario",blanco,30,50,370,2,negro)
    render_text("o se choca a si misma...",blanco,30,50,400,2,negro)

    pantalla.blit(keys,(650,40))
    render_text("Moverse",blanco,30,690,160,2,negro)
    render_text("[P] Pausa",blanco,30,685,200,2,negro)
    render_text("[Q] Salir",blanco,30,685,240,2,negro)

    pygame.draw.circle(pantalla,rojo,(510,320),20)
    pygame.draw.circle(pantalla,verde_o,(510,390),20)
    pygame.draw.circle(pantalla,morado,(510,460),20)

    render_text("Manzana normal. Comelas para aumentar tu puntaje!",blanco,22,540,310,2,negro)
    render_text("Manzana verde. Si comes una, aumentaras tu rapidez.",blanco,22,540,380,2,negro)
    render_text("Manzana lila. Si comes una, seras mucho mas grande!",blanco,22,540,450,2,negro)

    while intro_state == True:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                print("[Evento/inicio] Ventana cerrada. Cerrando...")
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    print("[Evento/inicio] Espacio. Iniciando juego...")
                    pygame.mixer.stop()
                    main_game()
                if evento.key == pygame.K_q:
                    print("[Evento/inicio] Saliendo del juego / Tecla Q")
                    sys.exit()

        # Letras parpadeando
        render_text("Snake!",verde,100,50,50,3,verde_o)
        render_text("P I E R D E S",rojo,30,320,400,2,negro)
        render_text("Presiona [Espacio] para comenzar",verde,40,240,530,2,negro)
        reloj.tick(5.45)
        pygame.display.update()
        render_text("Snake!",verde_o,100,50,50,3,verde)
        render_text("P I E R D E S",negro,30,320,400,2,rojo)
        render_text("Presiona [Espacio] para comenzar",blanco,40,240,530,2,negro)
        reloj.tick(5.45)
        pygame.display.update()

def pause_screen():
    pantalla.blit(pause_image,(0,0))

    pantalla.blit(keys,(650,40))
    render_text("Moverse",blanco,30,690,160,2,negro)
    render_text("[P] Reanudar",blanco,30,685,200,2,negro)
    render_text("[Q] Salir",blanco,30,685,240,2,negro)

    render_text("Pausa.",verde,100,50,50,3,verde_o)

    pygame.draw.circle(pantalla,rojo,(510,320),20)
    pygame.draw.circle(pantalla,verde_o,(510,390),20)
    pygame.draw.circle(pantalla,morado,(510,460),20)

    render_text("Manzana normal. Comelas para aumentar tu puntaje!",blanco,22,540,310,2,negro)
    render_text("Manzana verde. Si comes una, aumentaras tu rapidez.",blanco,22,540,380,2,negro)
    render_text("Manzana lila. Si comes una, seras mucho mas grande!",blanco,22,540,450,2,negro)

    pygame.display.update()

# funcion principal del juego, facilita volver a empezar el juego
def main_game():
    # cada vez que comienza el juego, el fondo puede ser aleatorio
    num_fondo = random.randint(1,4)
    print("[Fondo] Usando fondo " + str(num_fondo))
    if num_fondo == 1:
        bg_image = pygame.transform.scale(pygame.image.load("resources/img/fondo.png"),(winSizeX,winSizeY))
    elif num_fondo == 2:
        bg_image = pygame.transform.scale(pygame.image.load("resources/img/fondo2.png"),(winSizeX,winSizeY))
    elif num_fondo == 3:
        bg_image = pygame.transform.scale(pygame.image.load("resources/img/fondo3.png"),(winSizeX,winSizeY))
    elif num_fondo == 4:
        bg_image = pygame.transform.scale(pygame.image.load("resources/img/fondo4.png"),(winSizeX,winSizeY))

    # posicion inicial serpiente (aleatoria)
    posX = random.randrange(0, winSizeX-tam_serp+1, tam_serp)
    posY = random.randrange(0, winSizeY-tam_serp+1, tam_serp)
    # cambios de posicion (inicial = inmovil)
    cambioX,cambioY = 0,0
    # propiedades de la serpiente
    largo_serp = 1
    coord_serp = []
    points = 0
    # posicion inicial manzana (aleatoria)
    appleX = random.randrange(0, winSizeX-tam_serp+1, tam_serp)
    appleY = random.randrange(0, winSizeY-tam_serp+1, tam_serp)
    # Posicion inicial manzana verde (aleatoria)
    apple2X = random.randrange(0, winSizeX-tam_serp+1, tam_serp)
    apple2Y = random.randrange(0, winSizeY-tam_serp+1, tam_serp)
    # Posicion inicial manzana morada (aleatoria)
    apple3X = random.randrange(0, winSizeX-tam_serp+1, tam_serp)
    apple3Y = random.randrange(0, winSizeY-tam_serp+1, tam_serp)
    # movimiento anterior (8=U  2=D  4=L  6=R  0=n/a) para evitar giros en 180 grados
    mov_ant = 0
    # variables de estado del juego
    gameOver = False
    pauseGame = False
    fps = 13

    # reproducir musica
    musica.play(-1)

    # renderizar serpiente
    def render_snake():
        # la variable "cuerpo" va a tomar el valor de cada "mini lista" dentro de la lista "coord_serp"...
        for cuerpo in coord_serp:
            # ..y va a hacer que se dibuje el cuerpo de la serpiente en la coordenada que se encuentra dentro de la "mini lista".
            pygame.draw.rect(pantalla, negro, [(cuerpo[0],cuerpo[1]),(tam_serp,tam_serp)])
            # coord_serp = [[x1,y1],[x2,y2],[x3,y3]]
            # cuerpo = [x1,y1]                cuerpo = [x2,y2]                cuerpo = [x3,y3]
            # cuerpo[0],cuerpo[1] = x1,y1     cuerpo[0],cuerpo[1] = x2,y2     cuerpo[0],cuerpo[1] = x3,y3

    # main loop del juego
    while True:
        pygame.mixer.unpause()
        # si el estado del juego es gameOver, entonces pasa a la seccion de "juego terminado"
        while gameOver == True:
            # Detener todos los efectos
            musica.stop()
            comer.stop()
            # modo game over
            pantalla.blit(go_image,(0,0))
            render_snake()
            render_text("Juego terminado",rojo,50,(winSizeX/2)-150,(winSizeY/2)-70,3,rojo_o)
            render_text("[Espacio] Volver a jugar",negro,30,(winSizeX/2)-150,(winSizeY/2)+10,2)
            render_text("[Q] Volver al inicio",negro,30,(winSizeX/2)-150,(winSizeY/2)+35,2)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    print("[Evento/GameOver] Ventana cerrada. Cerrando...")
                    sys.exit()

                # Si se toca Espacio, vuelve a empezar, si toca Q, el juego se cierra
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        print("[Volviendo a iniciar snake]")
                        pygame.mixer.stop()
                        main_game()
                    if evento.key == pygame.K_q:
                        print("[Evento/GameOver] Saliendo del juego / Tecla Q")
                        pygame.mixer.stop()
                        intro_juego()

        # Si esta en modo pausa
        while pauseGame == True:
            pygame.mixer.pause()
            pause_screen()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    print("[Evento/pausa] Ventana cerrada. Cerrando...")
                    sys.exit()

                # Si se toca Espacio, vuelve a empezar, si toca Q, el juego se cierra
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        print("[Evento/pausa] Q. Saliendo")
                        sys.exit()
                    if evento.key == pygame.K_p:
                        print("[Evento/pausa] reanudando")
                        pauseGame = False

        # juego normal
        pantalla.blit(bg_image,(0,0))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                print("[Evento/Juego] Ventana cerrada. Cerrando...")
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and mov_ant != 6:
                    cambioX,cambioY = -tam_serp,0
                    mov_ant = 4
                elif evento.key == pygame.K_UP and mov_ant != 2:
                    cambioX,cambioY = 0,-tam_serp
                    mov_ant = 8
                elif evento.key == pygame.K_RIGHT and mov_ant != 4:
                    cambioX,cambioY = tam_serp,0
                    mov_ant = 6
                elif evento.key == pygame.K_DOWN and mov_ant != 8:
                    cambioX,cambioY = 0,tam_serp
                    mov_ant = 2
                elif evento.key == pygame.K_p:
                    print("[Tecla P] PAUSA")
                    pauseGame = True

        # renderizacion manzana
        pygame.draw.circle(pantalla,rojo,(appleX+tam_serp//2,appleY+tam_serp//2),tam_serp//2)
        pygame.draw.circle(pantalla,verde_o,(apple2X+tam_serp//2,apple2Y+tam_serp//2),tam_serp//2)
        pygame.draw.circle(pantalla,morado,(apple3X+tam_serp//2,apple3Y+tam_serp//2),tam_serp//2)


        # cambio de posicion de serpiente
        posX += cambioX
        posY += cambioY
        # guarda las coordenadas actuales de la cabeza de la serpiente a una lista...
        cabeza_serp = []
        cabeza_serp.append(posX)
        cabeza_serp.append(posY)
        # ...y luego las anade a otra lista que guarda todas las coordenadas (coord_serp)
        coord_serp.append(cabeza_serp)
        # si el tamano de la lista "coord_serp" es mayor al del supuesto largo de la serpiente, entonces que elimine el primer termino.
        if len(coord_serp) > largo_serp:
            del coord_serp[0]

        # DEBUG: print(coord_serp)
        render_snake()

        # mostrar los puntos y velocidad
        render_text("Puntos: " + str(points),blanco,40,10,0,2,negro)
        render_text("Rapidez: " + str(fps-12),blanco,40,200,0,2,negro)

        # cuando recien comience el juego, pedir que se toque alguna tecla
        if mov_ant == 0:
            render_text("Toca una tecla direccional para comenzar",blanco,30,(winSizeX/2)-250,(winSizeY/2)-20,2,negro)

        # si la serpiente toca la manzana, generar una nueva manzana aleatoria y aumentar el largo de serpiente
        if (posX,posY) == (appleX,appleY):
            comer.play()
            print("[Evento] Se toco la manzana en: " + str(appleX) + "," + str(appleY))
            appleX = random.randrange(0, winSizeX-tam_serp+1, tam_serp)
            appleY = random.randrange(0, winSizeY-tam_serp+1, tam_serp)
            largo_serp += 1
            points += 1
            render_text("Puntos: " + str(points),rojo,40,10,0,2,negro)
            # Cada vez que se consigan 3 puntos, la velocidad va a ir aumentando
            if points > 0:
                if points % 3 == 0:
                    fps += 1
                    render_text("Rapidez: " + str(fps-12),rojo,40,200,0,2,negro)

        # si la serpiente toca la manzana VERDE, generar una nueva manzana aleatoria y aumentar velocidad
        if (posX,posY) == (apple2X,apple2Y):
            comer2.play()
            print("[Evento] Se toco la manzana verde en: " + str(appleX) + "," + str(appleY))
            apple2X = random.randrange(0, winSizeX-tam_serp+1, tam_serp)
            apple2Y = random.randrange(0, winSizeY-tam_serp+1, tam_serp)
            fps += 1
            points += 2
            render_text("Puntos: " + str(points),verde,40,10,0,2,negro)
            render_text("Rapidez: " + str(fps-12),verde,40,200,0,2,negro)

        # si la serpiente toca la manzana MORADA, generar una nueva manzana aleatoria y aumentar largo de serpiente
        if (posX,posY) == (apple3X,apple3Y):
            comer3.play()
            print("[Evento] Se toco la manzana morada en: " + str(appleX) + "," + str(appleY))
            apple3X = random.randrange(0, winSizeX-tam_serp+1, tam_serp)
            apple3Y = random.randrange(0, winSizeY-tam_serp+1, tam_serp)
            largo_serp += 10
            points += 10
            render_text("Puntos: " + str(points),morado,40,10,0,2,negro)

        # si la serpiente se choca a si misma, pierde el juego
        if largo_serp > 1:
            for x in range(len(coord_serp)-1):
                if coord_serp[x] == cabeza_serp:
                    print("[Evento] Autochoque. Game over.")
                    crash2.play()
                    gameover_music.play()
                    gameOver = True

        # si la serpiente sale del escenario, pierde (se activa el estado gameOver)
        if (posX < 0 or posX > winSizeX-tam_serp) or (posY < 0 or posY > winSizeY-tam_serp):
            print("[Evento] Fuera de escenario. Game over.")
            crash.play()
            gameover_music.play()
            gameOver = True

        reloj.tick(fps)
        pygame.display.update()

intro_juego()
print("inicio_juego ---> main_game")
main_game()

# moxwel 2018
# Algunos recursos son propiedad de terceros.
