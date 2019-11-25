import pygame
import time
import configparser
#DANIEL SANCHEZ SEPULVEDA

centro = [384, 288]
#ancho=640
#alto=512 ,768,576
ancho=768
alto=576

VERDE=[0,255,0]
ROJO=[255,0,0]
BLANCO=[255,255,255]
NEGRO=[0,0,0]
GRIS=[70,70,70]
AZUL=[0,0,47]


win = pygame.display.set_mode([ancho,alto])






#PARA CREAR UNA MATRIZ DE SPRITES
def recorteSimple (imagenArecortar, x, y):
    imagen = pygame.image.load(imagenArecortar)
    limites = imagen.get_rect()
    lx = int(limites[2] / x)
    ly = int(limites[3] / y)
    m=[]
    for i in range(0,lx):
        for j in range(0, ly):
            cuadro=imagen.subsurface(i*x,j*y,x,y)
            m.append(cuadro)
    return m

####### PARA ACTUALIZAR SIEMPRE EL ESTADO DEL JUEGO
def redrawWindonw():
    win.fill(AZUL)
    playerList.draw(win)
    ModifierOne.draw(win)
    ModifierTwo.draw(win)
    ModifierThree.draw(win)
    ModifierFour.draw(win)
    Disparadordebils.draw(win)
    Disparadorfuertes.draw(win)
    Caminantesinmortales.draw(win)
    Caminantesmortales.draw(win)
    Balas.draw(win)
    Balasenemigas.draw(win)
    Balasenemigas1.draw(win)
    muros1.draw(win)
    bloquevidas.draw(win)
    pygame.display.flip()
##########




class Muro (pygame.sprite.Sprite):
    def __init__(self,archivo, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(archivo)
        self.rect=self.image.get_rect()# Devulve ancho alto pos x pos y
        self.rect.x=x
        self.rect.y=y
        self.auxxderecha=False
        self.auxxizquierda=False
        self.auxyarriba=False
        self.auxyabajo=False




    def update(self):
        if self.auxxderecha==True:
            player.rect.right=640
            self.auxxderecha=False

        if player.rect.right> 640 and self.auxxderecha==False:
            self.rect.left=self.rect.left-9
            self.auxxderecha=True
#
        if self.auxxizquierda==True:
            player.rect.left=64
            self.auxxizquierda=False

        if player.rect.left< 64 and self.auxxizquierda==False:
            self.rect.right=self.rect.right+9
            self.auxxizquierda=True




#manejo de la camara en y
        if self.auxyarriba==True:
            player.rect.top=128
            self.auxyarriba=False

        if player.rect.top<128 and self.auxyarriba==False:
            self.rect.bottom=self.rect.bottom+9
            self.auxyarriba=True


#manejo de camara en x
        if self.auxyabajo==True:
            player.rect.bottom=448
            self.auxyabajo=False

        if player.rect.bottom> 448 and self.auxyabajo==False:
            self.rect.top=self.rect.top-9
            self.auxyabajo=True








class Nivel:
    def __init__ (self, infomapa,x,y):
        self.interprete=configparser.ConfigParser()
        self.interprete.read(infomapa)
        self.alto=int(self.interprete.get("nivel","alto"))
        self.ancho=int(self.interprete.get("nivel","ancho"))
        self.mapa=[]
        self.mapa=self.interprete.get("nivel","mapa").split("\n")

        self.xx=x
        self.yy=y

#asignar cada caracter a una imagen
    def get_muros(self):
        var_x=self.alto
        var_y=self.ancho
        con_y=self.yy
        muros=pygame.sprite.Group()
        for fila in self.mapa:
            con_x=self.xx

            for c in fila:
                imagen=self.interprete.get(c,"imagen")
                mro=self.interprete.get(c,"muro")
                if (mro) == "si":
                    m=Muro(imagen,con_x,con_y)
                    muros.add(m)
                con_x+=var_x
            con_y+=var_y
        return muros







class Player(pygame.sprite.Sprite):
    def __init__(self, sheet):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 0
        self.action = 0 #Acciones que puede tomar el sprite
        self.limit = 0 #Sprite que se esta ejecutando en dicha accion
        self.lim = [2,2,2,2,2,2,2,2,2,2,2,2] #Limite de cada una de las filas de acciones
        self.vida = 100
        self.sheet = sheet #Sabana de sprites
        self.image = self.sheet[self.action][self.limit] #Carga una imagen en base a las coordenadas de la matriz de sprites
        self.rect = self.image.get_rect()
        self.rect.x = 64 #Posicion en x
        self.rect.y = 338 #Posicion en y
        self.vel_x = 0
        self.vel_y = 0
        self.ls_muros=[]



        self.frame = pygame.time.Clock()

    def update(self):


        if self.vida > 100:
            self.vida = 100

        elif (self.limit > self.lim[self.action]): #Obtine el limite de la accion que se este ejecutando
            self.limit = 0                         #y lo reinicia para seguir el ciclo de animacion
#respiracion
        elif self.action == 0 or self.action == 1 or self.action == 2 or self.action == 3:
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(5)
#movimiento
        elif self.action == 4 or self.action == 5 or self.action == 6 or self.action == 7:
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(45)
#disparo
        elif self.action == 8 or self.action == 9 or self.action == 10 or self.action == 11:
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            if (self.limit > self.lim[self.action]):
                    self.action = 3 #Como solo dispara una vez, vuelve a su posicion inicial
            self.frame.tick(60)
        if self.rect.x<=0:
            self.rect.x=0
        if self.rect.y<=0:
            self.rect.y=0

#golpes con los muros

        totazo1=pygame.sprite.spritecollide(player,muros1,False)
        for b in totazo1:
            if self.vel_x>0:
                self.rect.right=b.rect.left
            else:
                self.rect.left=b.rect.right

        totazo=pygame.sprite.spritecollide(player,muros1,False)
        for b in totazo:
            if  player.vel_y>0:
                self.rect.bottom = b.rect.top
                self.rect.right=self.rect.right-64
            else:
                self.rect.top = b.rect.bottom
                self.rect.right=self.rect.right-64















#
class Bloquevida(pygame.sprite.Sprite):

    def __init__(self,pto):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([0,0])
        self.image.fill(VERDE)
        self.rect=self.image.get_rect()
        self.rect.x = pto[0]
        self.rect.y = pto[1]




    def update(self):
        self.image=pygame.Surface([player.vida,15])
        self.image.fill(VERDE)





class Salud (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cantidadVida=0


    def update(self, VidaActual):
        self.cantidadVida = VidaActual
        if self.cantidadVida > 100:
            self.cantidadVida = 100

        else:
            if self.cantidadVida <= 0:
                self.cantidadVida=0




class Modifier(pygame.sprite.Sprite):
    def __init__(self, image, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame = pygame.time.Clock()
        self.auxxderecha=False
        self.auxxizquierda=False
        self.auxyarriba=False
        self.auxyabajo=False



    def update(self):
        if self.auxxderecha==True:
            player.rect.right=640
            self.auxxderecha=False

        if player.rect.right> 640 and self.auxxderecha==False:
            self.rect.left=self.rect.left-9
            self.auxxderecha=True
#
        if self.auxxizquierda==True:
            player.rect.left=64
            self.auxxizquierda=False

        if player.rect.left< 64 and self.auxxizquierda==False:
            self.rect.right=self.rect.right+9
            self.auxxizquierda=True




#manejo de la camara en y
        if self.auxyarriba==True:
            player.rect.top=128
            self.auxyarriba=False

        if player.rect.top<128 and self.auxyarriba==False:
            self.rect.bottom=self.rect.bottom+9
            self.auxyarriba=True


#manejo de camara en x
        if self.auxyabajo==True:
            player.rect.bottom=448
            self.auxyabajo=False

        if player.rect.bottom> 448 and self.auxyabajo==False:
            self.rect.top=self.rect.top-9
            self.auxyabajo=True


class Proyectilejugador(pygame.sprite.Sprite):
    def __init__(self, list):
        pygame.sprite.Sprite.__init__(self)
        self.limit = 0
        self.list = list
        self.image = self.list[self.limit]
        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = 0
        self.frame = pygame.time.Clock()


    def update(self):

        if (self.limit > 3):
            self.limit = 0

        else:
            self.rect.x += self.vel_x  #self.rect.x = self.rect.x + self.vel_x
            self.rect.y += self.vel_y
            self.image = self.list[self.limit]
            self.limit += 1
            self.frame.tick(60)

######PROYECTIL ENEMIGO DEBIL

class Proyectileenemigodebil(pygame.sprite.Sprite):
    def __init__(self, list):
        pygame.sprite.Sprite.__init__(self)
        self.limit = 0
        self.list = list
        self.image = self.list[self.limit]
        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = 0
        self.auxxderecha=False
        self.auxxizquierda=False
        self.auxyarriba=False
        self.auxyabajo=False
        self.frame = pygame.time.Clock()

    def update(self):

        if (self.limit > 3):
            self.limit = 0


        else:
            self.rect.x += self.vel_x  #self.rect.x = self.rect.x + self.vel_x
            self.rect.y += self.vel_y
            self.image = self.list[self.limit]
            self.limit += 1
            self.frame.tick(15)

        if self.auxxderecha==True:
            player.rect.right=640
            self.auxxderecha=False

        if player.rect.right> 640 and self.auxxderecha==False:
            self.rect.left=self.rect.left-9
            self.auxxderecha=True
    #
        if self.auxxizquierda==True:
            player.rect.left=64
            self.auxxizquierda=False

        if player.rect.left< 64 and self.auxxizquierda==False:
            self.rect.right=self.rect.right+9
            self.auxxizquierda=True




    #manejo de la camara en y
        if self.auxyarriba==True:
            player.rect.top=128
            self.auxyarriba=False

        if player.rect.top<128 and self.auxyarriba==False:
            self.rect.bottom=self.rect.bottom+9
            self.auxyarriba=True


    #
        if self.auxyabajo==True:
            player.rect.bottom=448
            self.auxyabajo=False

        if player.rect.bottom> 448 and self.auxyabajo==False:
            self.rect.top=self.rect.top-9
            self.auxyabajo=True



###PROYECTIL ENEMIGO FUERTE

class Proyectileenemigofuerte(pygame.sprite.Sprite):
    def __init__(self, list):
        pygame.sprite.Sprite.__init__(self)
        self.limit = 0
        self.list = list
        self.image = self.list[self.limit]
        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = 0
        self.frame = pygame.time.Clock()
        self.auxxderecha=False
        self.auxxizquierda=False
        self.auxyarriba=False
        self.auxyabajo=False

    def update(self):

        if (self.limit > 3):
            self.limit = 0

        else:
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            self.image = self.list[self.limit]
            self.limit += 1
            self.frame.tick(15)
            #
        if self.auxxderecha==True:
            player.rect.right=640
            self.auxxderecha=False

        if player.rect.right> 640 and self.auxxderecha==False:
            self.rect.left=self.rect.left-9
            self.auxxderecha=True
    #
        if self.auxxizquierda==True:
            player.rect.left=64
            self.auxxizquierda=False

        if player.rect.left< 64 and self.auxxizquierda==False:
            self.rect.right=self.rect.right+9
            self.auxxizquierda=True




    #manejo de la camara en y
        if self.auxyarriba==True:
            player.rect.top=128
            self.auxyarriba=False

        if player.rect.top<128 and self.auxyarriba==False:
            self.rect.bottom=self.rect.bottom+9
            self.auxyarriba=True


    #manejo de camara de x
        if self.auxyabajo==True:
            player.rect.bottom=448
            self.auxyabajo=False

        if player.rect.bottom> 448 and self.auxyabajo==False:
            self.rect.top=self.rect.top-9
            self.auxyabajo=True

#torreta mira derecha debil
class Disparadordebil(pygame.sprite.Sprite):
    def __init__(self, sheet, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.action = 0
        self.limit = 4
        #ojo aqui mque el sprite es vertical
        self.lim = [4,4]
        self.temp = 7
        self.sheet = sheet
        self.image = self.sheet[self.action][self.limit]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.auxxderecha=False
        self.auxxizquierda=False
        self.auxyarriba=False
        self.auxyabajo=False

        self.frame = pygame.time.Clock()

    def update(self):

        self.temp -= 1

        if (self.limit > self.lim[self.action]):
            self.limit = 0

        elif self.action == 0:
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(8)
##################
        if self.auxxderecha==True:
            player.rect.right=640
            self.auxxderecha=False

        if player.rect.right> 640 and self.auxxderecha==False:
            self.rect.left=self.rect.left-9
            self.auxxderecha=True
    #
        if self.auxxizquierda==True:
            player.rect.left=64
            self.auxxizquierda=False

        if player.rect.left< 64 and self.auxxizquierda==False:
            self.rect.right=self.rect.right+9
            self.auxxizquierda=True




    #manejo de la camara en y
        if self.auxyarriba==True:
            player.rect.top=128
            self.auxyarriba=False

        if player.rect.top<128 and self.auxyarriba==False:
            self.rect.bottom=self.rect.bottom+9
            self.auxyarriba=True


    #manejo de camara en Y
        if self.auxyabajo==True:
            player.rect.bottom=448
            self.auxyabajo=False

        if player.rect.bottom> 448 and self.auxyabajo==False:
            self.rect.top=self.rect.top-9
            self.auxyabajo=True





#torreta  FUERTE
class Disparadorfuerte(pygame.sprite.Sprite):
    def __init__(self, sheet, x ,y,switch):
        pygame.sprite.Sprite.__init__(self)
        self.action = 0
        self.limit = 0
        self.lim = [4,4]
        self.temp = 15
        self.sheet = sheet
        self.image = self.sheet[self.action][self.limit]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.semaforo=switch
        #self.vida=10
        self.frame = pygame.time.Clock()
        self.auxxderecha=False
        self.auxxizquierda=False
        self.auxyarriba=False
        self.auxyabajo=False

    def update(self):

        self.temp -= 1

        if (self.limit > self.lim[self.action]):
            self.limit = 0

        elif self.semaforo==0:
            self.action=0
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(8)

        elif self.semaforo==1:
            self.action=1
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(8)
#######

        if self.auxxderecha==True:
            player.rect.right=640
            self.auxxderecha=False

        if player.rect.right> 640 and self.auxxderecha==False:
            self.rect.left=self.rect.left-9
            self.auxxderecha=True
            #
        if self.auxxizquierda==True:
            player.rect.left=64
            self.auxxizquierda=False

        if player.rect.left< 64 and self.auxxizquierda==False:
            self.rect.right=self.rect.right+9
            self.auxxizquierda=True




            #manejo de la camara en y
        if self.auxyarriba==True:
            player.rect.top=128
            self.auxyarriba=False

        if player.rect.top<128 and self.auxyarriba==False:
            self.rect.bottom=self.rect.bottom+9
            self.auxyarriba=True


            #manejo de camara en x
        if self.auxyabajo==True:
            player.rect.bottom=448
            self.auxyabajo=False

        if player.rect.bottom> 448 and self.auxyabajo==False:
            self.rect.top=self.rect.top-9
            self.auxyabajo=True



###caminante
class Caminanteinmortal(pygame.sprite.Sprite):
    def __init__(self, sheet, x ,y,inicio,fin):
        pygame.sprite.Sprite.__init__(self)
        self.action = 0
        self.limit = 0
        self.lim = [4,4]
        self.sheet = sheet
        self.image = self.sheet[self.action][self.limit]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.limiteinicio=inicio
        self.limitefinal=fin
        self.vel_y =3
        self.aux=0
        self.bandera=True
        self.auxxderecha=False
        self.auxxizquierda=False
        self.auxyarriba=False
        self.auxyabajo=False
        self.frame = pygame.time.Clock()
        self.dagno=100


####
    def update(self):
        '''Actualiza el objeto '''

        if (self.limit > self.lim[self.action]):
            self.limit = 0

        elif self.action == 0:
            self.rect.y += self.vel_y
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(30)

        if self.rect.y > self.limitefinal:
            self.vel_y =-5

        if self.rect.y < self.limiteinicio:
            self.vel_y =5

        if self.rect.y > self.limitefinal:
            self.vel_y =-7

        if self.rect.y < self.limiteinicio:
            self.vel_y =7

        if self.auxxderecha==True:
            player.rect.right=640
            self.auxxderecha=False

        if player.rect.right> 640 and self.auxxderecha==False:
            self.rect.left=self.rect.left-9
            self.auxxderecha=True
    #
        if self.auxxizquierda==True:
            player.rect.left=64
            self.auxxizquierda=False

        if player.rect.left< 64 and self.auxxizquierda==False:
            self.rect.right=self.rect.right+9
            self.auxxizquierda=True


            #manejo de la camara en y
        if self.auxyarriba==True:
            player.rect.top=128
            self.auxyarriba=False

        if player.rect.top<128 and self.auxyarriba==False:
            self.limiteinicio=self.limiteinicio+9
            self.limitefinal=self.limitefinal+9
            self.rect.bottom=self.rect.bottom+9
            self.auxyarriba=True


            #manejo de camara en x
        if self.auxyabajo==True:
            player.rect.bottom=448
            self.auxyabajo=False

        if player.rect.bottom> 448 and self.auxyabajo==False:
            self.limiteinicio=self.limiteinicio-9
            self.limitefinal=self.limitefinal-9
            self.rect.top=self.rect.top-9
            self.auxyabajo=True

class Caminantemortal(pygame.sprite.Sprite):
    def __init__(self, sheet, x ,y,inicio,fin):
        pygame.sprite.Sprite.__init__(self)
        self.action = 0
        self.limit = 0
        self.lim = [4,4]
        self.sheet = sheet
        self.image = self.sheet[self.action][self.limit]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.limiteinicio=inicio
        self.limitefinal=fin
        self.vel_y =7
        self.aux=0
        self.bandera=True
        self.auxxderecha=False
        self.auxxizquierda=False
        self.auxyarriba=False
        self.auxyabajo=False
        self.frame = pygame.time.Clock()




    def update(self):
        '''Actualiza el objeto '''

        if (self.limit > self.lim[self.action]):
            self.limit = 0

        elif self.action == 0:
            self.rect.y += self.vel_y
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(30)

            if self.rect.y > self.limitefinal:
                self.vel_y =-7

            if self.rect.y < self.limiteinicio:
                self.vel_y =7

        if self.auxxderecha==True:
            player.rect.right=640
            self.auxxderecha=False

        if player.rect.right> 640 and self.auxxderecha==False:
            self.rect.left=self.rect.left-9
            self.auxxderecha=True
    #
        if self.auxxizquierda==True:
            player.rect.left=64
            self.auxxizquierda=False

        if player.rect.left< 64 and self.auxxizquierda==False:
            self.rect.right=self.rect.right+9
            self.auxxizquierda=True


            #manejo de la camara en y
        if self.auxyarriba==True:
            player.rect.top=128
            self.auxyarriba=False

        if player.rect.top<128 and self.auxyarriba==False:
            self.limiteinicio=self.limiteinicio+9
            self.limitefinal=self.limitefinal+9
            self.rect.bottom=self.rect.bottom+9
            self.auxyarriba=True


            #manejo de camara en x
        if self.auxyabajo==True:
            player.rect.bottom=448
            self.auxyabajo=False

        if player.rect.bottom> 448 and self.auxyabajo==False:
            self.limiteinicio=self.limiteinicio-9
            self.limitefinal=self.limitefinal-9
            self.rect.top=self.rect.top-9
            self.auxyabajo=True


#-----------------------------------------------------------------------
if __name__ == '__main__':
    #inicializacion
    pygame.init()
    indicadorvida=True
    fin=False
    game_over=False
    Inicializadordebalas=False
    fuente = pygame.font.Font(None,36)
    #revisar

    velocidad=False
    cantidadbanderas=0

    dibujarmapa=False

    Nivel1=Nivel("mapa1.map",0,0)
    muros1=Nivel1.get_muros()




##################
    Derechayo = recorteSimple('derechayo.png',40,62)
    Izquierdayo = recorteSimple('izquierdayo.png',40,63)
    Arribayo = recorteSimple('arribayo.png',40,63)
    Abajoyo = recorteSimple('abajoyo.png',40,63)

    Yo = [Derechayo,Izquierdayo,Arribayo,Abajoyo,Derechayo,Izquierdayo,Arribayo,Abajoyo,Derechayo,Izquierdayo,Arribayo,Abajoyo]
#################
    Bala = recorteSimple('bala.png',64,64)
    Bataran = Bala
#####
    Tennis = pygame.image.load('tennis.png').convert_alpha()
    Banderamala = pygame.image.load('banderamala.png').convert_alpha()
    Vida = pygame.image.load('vida.png').convert_alpha()

    Banderabuena = pygame.image.load('banderabuena.png').convert_alpha()

######
    torretaderecha = recorteSimple('torreta derecha.png', 64, 64)
    Torretaderecha = [torretaderecha]


    torretaarriba = recorteSimple('torreta arriba.png', 64, 64)

    torretaabajo = recorteSimple('torreta abajo.png', 64, 64)
    Torretaabajoyarriba = [torretaarriba,torretaabajo]


    boom = recorteSimple('boom.png', 64, 64)
    Boom = [boom]

    piyomon = recorteSimple('piyomon.png', 64, 64)

    Piyomon = [piyomon]


    balaenemiga = recorteSimple('balaenemiga.png', 64, 64)
    baladebil = balaenemiga

    balaenemiga1 = recorteSimple('balaenemiga1.png', 64, 64)
    balafuerte = balaenemiga1

#---------------------------------------------------------------
    playerList = pygame.sprite.Group() #Para el manejo de colisiones y actualizaciones se debe crear un grupo de sprites
    player = Player(Yo)
    playerList.add(player)

    indicadores = pygame.sprite.Group()
    sPlayer = Salud()



    ModifierOne = pygame.sprite.Group()
    ModifierTwo = pygame.sprite.Group()
    ModifierThree = pygame.sprite.Group()
    ModifierFour = pygame.sprite.Group()

    bloquevidas = pygame.sprite.Group()
    b=Bloquevida([ancho-688,alto-30])
    bloquevidas.add(b)

#######COLOCAR POSICIONES DE OBJETOS

#items
    Powerup = Modifier(Vida, 1792, 640)
    #PowerUp = Modifier(Vida, 64, 128)
    Powerup1=Modifier(Vida, 768, 640)
    Powerup2=Modifier(Vida, 832, 1280)
    Powerup3=Modifier(Vida, 1536, 256)
    ModifierOne.add(Powerup)
    ModifierOne.add(Powerup1)
    ModifierOne.add(Powerup2)
    ModifierOne.add(Powerup3)


    Velocidad = Modifier(Tennis,960, 768)
    #Velocidad = Modifier(Tennis, 0, 0)
    ModifierTwo.add(Velocidad)


    Banderamala1 = Modifier(Banderamala, 1152, 576)
    ModifierThree.add(Banderamala1)

    Banderamala2 = Modifier(Banderamala, 64, 512)
    ModifierThree.add(Banderamala2)



    Banderabuena1 = Modifier(Banderabuena, 384, 1280)
    ModifierFour.add(Banderabuena1)

    Banderabuena2 = Modifier(Banderabuena, 448, 320)
    ModifierFour.add(Banderabuena2)

    Banderabuena3 = Modifier(Banderabuena, 960, 192)
    ModifierFour.add(Banderabuena3)

    Banderabuena4 = Modifier(Banderabuena, 1152, 1152)
    ModifierFour.add(Banderabuena4)

    Banderabuena5 = Modifier(Banderabuena, 2048, 128)
    ModifierFour.add(Banderabuena5)

##enemigos, las 3 lineas de abajo se ponen en el draw de arriba
    Disparadordebils = pygame.sprite.Group()
    Disparadorfuertes = pygame.sprite.Group()
    Caminantesinmortales = pygame.sprite.Group()
    Caminantesmortales = pygame.sprite.Group()

    Torretaderechaenemigo1 = Disparadordebil(Torretaderecha, 192,128)
    Torretaderechaenemigo2 = Disparadordebil(Torretaderecha, 64,832)
    Torretaderechaenemigo3 = Disparadordebil(Torretaderecha, 1920,384)

    Disparadordebils.add(Torretaderechaenemigo1)
    Disparadordebils.add(Torretaderechaenemigo2)
    Disparadordebils.add(Torretaderechaenemigo3)



    Torretaarribaenemigo1 =Disparadorfuerte(Torretaabajoyarriba, 704,1280,0)
    Torretaarribaenemigo2 =Disparadorfuerte(Torretaabajoyarriba, 1728,896,0)
    Torretaarribaenemigo3 =Disparadorfuerte(Torretaabajoyarriba, 1856,384,0)
    Torretaarribaenemigo3 =Disparadorfuerte(Torretaabajoyarriba, 1536,640,0)

    Disparadorfuertes.add(Torretaarribaenemigo1)
    Disparadorfuertes.add(Torretaarribaenemigo2)
    Disparadorfuertes.add(Torretaarribaenemigo3)

    Torretaabajoenemigo1=Disparadorfuerte(Torretaabajoyarriba, 1408,1024,1)
    Torretaabajoenemigo2=Disparadorfuerte(Torretaabajoyarriba, 1472,256,1)
    Torretaabajoenemigo3=Disparadorfuerte(Torretaabajoyarriba, 1536,960,1)
    Torretaabajoenemigo4=Disparadorfuerte(Torretaabajoyarriba, 1600,256,1)
    Torretaabajoenemigo5=Disparadorfuerte(Torretaabajoyarriba, 1600,768,1)
    Torretaabajoenemigo6=Disparadorfuerte(Torretaabajoyarriba, 1728,1024,1)
    Torretaabajoenemigo7=Disparadorfuerte(Torretaabajoyarriba, 192,192,1)

    Disparadorfuertes.add(Torretaabajoenemigo1)
    Disparadorfuertes.add(Torretaabajoenemigo2)
    Disparadorfuertes.add(Torretaabajoenemigo3)
    Disparadorfuertes.add(Torretaabajoenemigo4)
    Disparadorfuertes.add(Torretaabajoenemigo5)
    Disparadorfuertes.add(Torretaabajoenemigo6)
    Disparadorfuertes.add(Torretaabajoenemigo7)




    Piyomon1=Caminantemortal(Piyomon, 128,448,448,576)
    Piyomon2=Caminantemortal(Piyomon, 1860,128,128,320)
    Piyomon3=Caminantemortal(Piyomon, 1728,384,384,512)
    Piyomon4=Caminantemortal(Piyomon, 1024, 256,256,384)

    Caminantesmortales.add(Piyomon1)
    Caminantesmortales.add(Piyomon2)
    Caminantesmortales.add(Piyomon3)
    Caminantesmortales.add(Piyomon4)



    Boomenemigo1=Caminanteinmortal(Boom, 448,230,230,320)
    Boomenemigo2=Caminanteinmortal(Boom, 320,960,960,1088)
    Boomenemigo3=Caminanteinmortal(Boom, 512,576,576,704)
    Boomenemigo4=Caminanteinmortal(Boom, 1216,1024,1024,1152)
    Boomenemigo5=Caminanteinmortal(Boom, 1984,128,128,256)

    Caminantesinmortales.add(Boomenemigo1)
    Caminantesinmortales.add(Boomenemigo2)
    Caminantesinmortales.add(Boomenemigo3)
    Caminantesinmortales.add(Boomenemigo4)
    Caminantesinmortales.add(Boomenemigo5)


#inicialziar las acciones de los objetos

    Torretaderechaenemigo1.action = 0
    Torretaderechaenemigo2.action = 0
    Torretaderechaenemigo3.action = 0

    Torretaarribaenemigo1.action = 0
    Torretaarribaenemigo2.action = 0
    Torretaarribaenemigo3.action = 0

    Torretaabajoenemigo1.action = 0
    Torretaabajoenemigo2.action = 0
    Torretaabajoenemigo3.action = 0
    Torretaabajoenemigo4.action = 0
    Torretaabajoenemigo5.action = 0
    Torretaabajoenemigo6.action = 0

    Piyomon1.action = 0
    Piyomon2.action = 0
    Piyomon3.action = 0


    Boomenemigo1.action = 0
    Boomenemigo2.action = 0
    Boomenemigo3.action = 0
    Boomenemigo4.action = 0
    Boomenemigo5.action = 0


#bala normal mia
    Balas = pygame.sprite.Group()
#bala del enemigo
    Balasenemigas = pygame.sprite.Group()
    Balasenemigas1 = pygame.sprite.Group()
#





#BANDA SONORA
    bandasonora=pygame.mixer.Sound('batman.ogg')
    bandasonora.play(999999999)
    pause=False







############################LOGICA DE EVENTOS###############################

    while not fin:


        #captura de eventos
        #mostrador de texto de vida y bandera
        if  cantidadbanderas>= 0:
            flag='Banderas: '+str(cantidadbanderas)
            mostradorvida='Vida: '
            a=fuente.render(flag,True,BLANCO)
            win.blit(a,[608,535])

            b=fuente.render(mostradorvida,True,BLANCO)
            win.blit(b,[7,540])
            pygame.display.flip()


        for event in pygame.event.get():



            if event.type == pygame.QUIT:
                fin=True



            if event.type == pygame.KEYDOWN:
                if velocidad==False:
                    if event.key == pygame.K_RIGHT:
                        player.vel_x = 11
                        player.vel_y = 0
                        player.direction = 0
                        player.action = 4



                    if event.key == pygame.K_LEFT:
                        player.vel_x = -11
                        player.vel_y = 0
                        player.direction = 1
                        player.action = 5

                    if event.key == pygame.K_UP:
                        player.vel_x = 0
                        player.vel_y = -11
                        player.direction = 2
                        player.action = 6

                    if event.key == pygame.K_DOWN:
                        player.vel_x = 0
                        player.vel_y = 11
                        player.direction = 3
                        player.action = 7

                    if event.key == pygame.K_p:
                        if pause==False:
                            pause=True
                            win.blit(pygame.image.load('titulo.png'),[0,0])

                            pygame.display.flip()
                        else:
                            if pause==True:

                                pause=False



                    if event.key == pygame.K_SPACE:

                        if Inicializadordebalas == False: #
                            midisparo = Proyectilejugador(Bataran)
                            midisparo.rect.x = player.rect.x #El proyectil inicia con la posicion de jugador
                            midisparo.rect.y = player.rect.y
                            Balas.add(midisparo)
                            if player.direction == 0:
                                midisparo.vel_x = 12
                                player.action = 8    ###4
                            elif player.direction == 1:
                                midisparo.vel_x = -12
                                player.action = 9
                            elif player.direction == 2:
                                midisparo.vel_y = -12
                                player.action = 10
                            elif player.direction == 3:
                                midisparo.vel_y = 12
                                player.action = 11
                if velocidad==True:
                    if event.key == pygame.K_RIGHT:
                        player.vel_x = 17
                        player.vel_y = 0
                        player.direction = 0
                        player.action = 4

                    if event.key == pygame.K_LEFT:
                        player.vel_x = -17
                        player.vel_y = 0
                        player.direction = 1
                        player.action = 5

                    if event.key == pygame.K_UP:
                        player.vel_x = 0
                        player.vel_y = -17
                        player.direction = 2
                        player.action = 6

                    if event.key == pygame.K_DOWN:
                        player.vel_x = 0
                        player.vel_y = 17
                        player.direction = 3
                        player.action = 7

                    if event.key == pygame.K_p:
                        if pause==False:
                            pause=True
                        else:
                            if pause==True:
                                pause=False


                    if event.key == pygame.K_SPACE:

                        if Inicializadordebalas == False: #
                            midisparo = Proyectilejugador(Bataran)
                            midisparo.rect.x = player.rect.x #El proyectil inicia con la posicion de jugador
                            midisparo.rect.y = player.rect.y
                            Balas.add(midisparo)
                            if player.direction == 0:
                                midisparo.vel_x = 12
                                player.action = 8    ###4
                            elif player.direction == 1:
                                midisparo.vel_x = -12
                                player.action = 9
                            elif player.direction == 2:
                                midisparo.vel_y = -12
                                player.action = 10
                            elif player.direction == 3:
                                midisparo.vel_y = 12
                                player.action = 11



            if event.type == pygame.KEYUP: # Cuando suelta la tecla carga la accion de respirar
                if event.key == pygame.K_RIGHT:
                    player.action = 0

                if event.key == pygame.K_UP:
                    player.action = 2

                if event.key == pygame.K_LEFT:
                    player.action = 1

                if event.key == pygame.K_DOWN:
                    player.action = 3

        for r in Caminantesinmortales:
            r.action=0

        for r in Caminantesmortales:
            r.action=0



#manejo de balas de enemigos

        for d in Disparadordebils: #
            if (d.temp == 0):
                balamalita = Proyectileenemigodebil(baladebil)
                #aqui cambio la direccion de la BALA
                balamalita.vel_x = 15
                balamalita.rect.x = d.rect.x
                balamalita.rect.y = d.rect.y
                balamalita.add(Balasenemigas)
                        #aqui cambio la cantidad de balas en cierto
                d.temp = 7




        for d in Disparadorfuertes: #
            if (d.temp == 0):
                balamala = Proyectileenemigofuerte(balafuerte)
                        #aqui cambio la direccion de la BALA
                if d.semaforo==0:
                    balamala.vel_y = -7
                if d.semaforo==1:
                    balamala.vel_y = 7

                balamala.rect.x = d.rect.x
                balamala.rect.y = d.rect.y
                balamala.add(Balasenemigas1)
                #aqui cambio la cantidad de balas en cierto
                d.temp = 10


#### Manejo de limites
        for b in Balasenemigas:
            if b.rect.x<0 or b.rect.x>2112 or b.rect.y<0 or b.rect.y > 1344:
                Balasenemigas.remove(b)

        for b in Balasenemigas1:
            if b.rect.x<0 or b.rect.x>2112 or b.rect.y<0 or b.rect.y > 1344:
                Balasenemigas1.remove(b)

        for b in Balas:
            if b.rect.x<0 or b.rect.x>2112 or b.rect.y<0 or b.rect.y > 1344:
                Balas.remove(b)



###########LOGICA DE COLISIONES#############################
#mis balas


        for b in Balas: #Revisa cada una de las balas en la lista
            f_col = pygame.sprite.spritecollide(b, Caminantesinmortales, False)
            for e in f_col: #Revisa los objetos que quedaron en la colision
                Balas.remove(b)
        for b in Balas: #Revisa cada una de las balas en la lista
            f_col = pygame.sprite.spritecollide(b, Disparadordebils, True)
            for e in f_col: #Revisa los objetos que quedaron en la colision
                boom=pygame.mixer.Sound('boom.ogg')
                boom.play()
                Balas.remove(b)

        for b in Balas: #Revisa cada una de las balas en la lista
            f_col = pygame.sprite.spritecollide(b, Disparadorfuertes, True)
            for e in f_col: #Revisa los objetos que quedaron en la colision
                boom=pygame.mixer.Sound('boom.ogg')
                boom.play()
                Balas.remove(b)


        for b in Balas: #Revisa cada una de las balas en la lista
            f_col = pygame.sprite.spritecollide(b, Caminantesmortales, True)
            for e in f_col: #Revisa los objetos que quedaron en la colision
                grito=pygame.mixer.Sound('grito.ogg')
                grito.play()
                Balas.remove(b)

        for b in Balas: #Revisa cada una de las balas en la lista
            f_col = pygame.sprite.spritecollide(b, muros1, False)
            for e in f_col: #Revisa los objetos que quedaron en la colision
                Balas.remove(b)
#las balas del malo :(
        for b in Balasenemigas: #Revisa cada una de las balas en la lista
            f_col = pygame.sprite.spritecollide(b, muros1, False)
            for e in f_col: #Revisa los objetos que quedaron en la colision
                Balasenemigas.remove(b)


        for b in Balasenemigas1: #Revisa cada una de las balas en la lista
            f_col = pygame.sprite.spritecollide(b, muros1, False)
            for e in f_col: #Revisa los objetos que quedaron en la colision
                Balasenemigas1.remove(b)



        for b in Balasenemigas:
            l_col = pygame.sprite.spritecollide(b, playerList, False)
            for e in l_col:
                Balasenemigas.remove(b)
                player.vida -= 8
                sPlayer.update(player.vida)
                if player.vida <= 0:
                    game_over = True

        for b in Balasenemigas1:
            l_col = pygame.sprite.spritecollide(b, playerList, False)
            for e in l_col:
                Balasenemigas1.remove(b)
                player.vida -= 23
                sPlayer.update(player.vida)
                if player.vida <= 0:
                    game_over = True
#mis colisiones con los malos
        impactomortal1=pygame.sprite.spritecollide(player,Caminantesmortales, False)
        for b in impactomortal1:
            player.vida=0
            sPlayer.update(player.vida)
            if player.vida <= 0:
                game_over = True

        impactomortal2=pygame.sprite.spritecollide(player,Caminantesinmortales, False)
        for b in impactomortal2:
            player.vida=0
            sPlayer.update(player.vida)
            if player.vida <= 0:
                game_over = True

        impactodebil=pygame.sprite.spritecollide(player,Disparadordebils, False)
        for b in impactodebil:
            player.vida=player.vida-0.10
            sPlayer.update(player.vida)

            if player.vida <= 0:
                game_over = True

        impactofuerte=pygame.sprite.spritecollide(player,Disparadorfuertes, False)
        for b in impactofuerte:
            player.vida=player.vida-0.15
            sPlayer.update(player.vida)
            if player.vida <=0:
                game_over = True







#########mis colisiones con los items
#cerveza
        colModifierOne=pygame.sprite.spritecollide(player,ModifierOne, True)
        for b in colModifierOne:
            player.vida=100
            sPlayer.update(player.vida)
#velocidad
        colModifierTwo=pygame.sprite.spritecollide(player,ModifierTwo, True)
        for b in colModifierTwo:
            velocidad=True
#banderamala
        colModifierThree=pygame.sprite.spritecollide(player,ModifierThree, True)
        for b in colModifierThree:
            player.vida=player.vida-20
            sPlayer.update(player.vida)
            risa=pygame.mixer.Sound('risa.ogg')
            risa.play()
            Balas.remove(b)


            if player.vida <=0:
                game_over = True
#banderabuena
        colModifierFour=pygame.sprite.spritecollide(player,ModifierFour, True)
        for b in colModifierFour:
            tulun=pygame.mixer.Sound('win.ogg')
            tulun.play()
            cantidadbanderas=cantidadbanderas+1



#########game y win
        if not game_over:

            if pause==False:
                player.update()
                ModifierOne.update()
                ModifierTwo.update()
                ModifierThree.update()
                ModifierFour.update()
                Disparadordebils.update()
                Disparadorfuertes.update()
                Caminantesmortales.update()
                Caminantesinmortales.update()
                Balas.update()
                Balasenemigas.update()
                Balasenemigas1.update()
                muros1.update()
                bloquevidas.update()


                pygame.display.flip()


                redrawWindonw()

        else:
           win.fill(NEGRO)
           win.blit(pygame.image.load('perder.png'),[0,0])
           pygame.display.flip()

        if cantidadbanderas==5:
            for b in Caminantesinmortales:
                Caminantesinmortales.remove(b)

            texto=fuente.render("GANASTE", True, NEGRO)
            win.fill(BLANCO)
            win.blit(texto,(centro[0]-80,centro[1]))

            pygame.display.flip()
