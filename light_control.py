#!/usr/bin/env python3
#
# Control remoto de color de la pantalla, para tomar la foto de
# http://drmad.org/blog/fotografia-foreveralone.html
#
# Por Oliver Etchebarne / Paperclip X10
# http://drmad.org / http://x10.pe
#

import pygame, os
import socketserver

screen = None

color = [0, 0, 0]

class myUDPHandler ( socketserver.BaseRequestHandler ):
    ''' Clase de manejo de paquetes UDP de socketserver '''
    def handle ( self ):
        # Leemos el texto que viene
        data = self.request[0].strip()

        # Sacamos los valores y los convertimos a decimal
        R = int(data[0:2], 16)
        G = int(data[2:4], 16)
        B = int(data[4:6], 16)
        I = int(data[6:8], 16)
        
        # La intensidad va desde -126 a 127
        I -= 127

        # Ajustamos los colores, dependiendo de la intensidad.
        if I < 0:
            # Oscurecemos
            I = ( ( I + 127 ) * 2) / 256

            R *= I
            G *= I
            B *= I

        elif I > 0:
            # Aclaramos 
            I = ( I * 2 ) / 256

            R = R + ( ( 255 - R ) * I )
            G = G + ( ( 255 - G ) * I )
            B = B + ( ( 255 - B ) * I )
           
        # Colocamos el color en la pantalla.
        color = [ int(R), int(G), int(B) ]
        screen.fill ( color )
        pygame.display.flip()


# Inicialización de PyGame
pygame.init()

screenres = (1920,1080)
screen = pygame.display.set_mode ( screenres, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN )
pygame.mouse.set_visible ( False )

# Pintamos de un color temporal.
screen.fill ( [255, 0, 255] )
pygame.display.flip()

# E iniciamos un servidor UDP en un puerto cualquiera.
server = socketserver.UDPServer( ('0.0.0.0', 1922), myUDPHandler)
server.serve_forever()
