import sys,pygame
import random
from pygame.locals import *
 
class App:

	def __init__(self):
		self._running = True
		self._display_surf = None


	def on_init(self):
		pygame.init()

		#matriz de matirces que contienen las piezas
		self.fig =[
					#I (palo de cuatro cuadrados)
					[[[1],[1],[1],[1]], 
					[[1,1,1,1]],
					[[1],[1],[1],[1]], 
					[[1,1,1,1]],
					[[9]]],
					
					#O (cuadrado)
					[[[1,1],[1,1]], 
					[[1,1],[1,1]],
					[[1,1],[1,1]],
					[[1,1],[1,1]],
					[[5]]],	
					#S (reflejado de z)
					[[[0,1,1],[1,1,0]], 
					[[1,0],[1,1],[0,1]],
					[[0,1,1],[1,1,0]],
					[[1,0],[1,1],[0,1]],
					[[7]]],
					#Z
					[[[1,1,0],[0,1,1]], 
					[[0,1],[1,1],[1,0]],
					[[1,1,0],[0,1,1]],
					[[0,1],[1,1],[1,0]],
					[[7]]],
					#T
					[[[0,1,0],[1,1,1]], 
					[[1,0],[1,1],[1,0]],
					[[1,1,1],[0,1,0]],
					[[0,1,0],[1,1,0],[0,1,0]],
					[[7]]],
					#L
					[[[1,0],[1,0],[1,1]], 
					[[1,1,1],[1,0,0]],
					[[1,1],[0,1],[0,1]],
					[[0,0,1],[1,1,1]],
					[[7]]],
					#J (reflejado de L)
		 			[[[0,1],[0,1],[1,1]],
					[[0,0,1],[1,1,1]],
					[[1,1],[1,0],[1,0]],
					[[1,1,1],[0,0,1]],
					[[7]]]]

		#Generacion de la pantalla (matriz)
		self.pantalla = []
		for i in xrange(25):
			self.pantalla.append([])
			for j in xrange(16): 
				if i != 21 and j != 11:
					self.pantalla[i].append(0)
				elif i == 21:
					self.pantalla[i].append(2)
				elif j == 11:
					self.pantalla[i].append(2)


		self._display_surf = pygame.display.set_mode((330,660), pygame.HWSURFACE | pygame.DOUBLEBUF) #inicio de la ventana
		self._running = True
		self.pausa = False

	def on_event(self, event, keys):
		if event.type == pygame.QUIT: #salir del programa
			self._running = False
		if keys[K_ESCAPE]: #salir del programa
			self._running = False
		if keys[K_UP] and cuadrado.end == False: #pausa
			self.pausa = True
			pygame.mixer.music.pause()
			fuente = pygame.font.Font(None, 100)
			texto = fuente.render("PAUSA", 0, (0, 0, 0))
			self._display_surf.blit(texto, (45,260))
			pygame.display.flip()
			while self.pausa:
				for event in pygame.event.get():
					if event.type == KEYUP:
						pygame.time.delay(100)
						self.pausa = False
						pygame.mixer.music.unpause()
		if cuadrado.end == True:
			pygame.mixer.music.pause()
			pygame.mixer.music.stop()

	def on_loop(self, keys):
		cuadrado.posicionar()
		cuadrado.velocidad(keys)
		cuadrado.brain()
		cuadrado.caida()
		cuadrado.linea()

	def on_render(self):
		cuadrado.printeo()
		if cuadrado.end == True:
			fuente = pygame.font.Font(None, 80)
			texto = fuente.render("Perdiste", 0, (255, 0, 0))
			theApp._display_surf.blit(texto, (60,260))
			pygame.display.flip()
		fuente = pygame.font.Font(None, 30)
		texto = fuente.render(str(cuadrado.puntos), 0, (255, 255, 255))
		self._display_surf.blit(texto, (300,15))
		pygame.display.flip()


	def on_cleanup(self):
		pygame.quit()


	def on_execute(self):
		if self.on_init() == False:
			self._running = False
		clock=pygame.time.Clock()
		pygame.mixer.music.load("musica.mp3")
		pygame.mixer.music.play(-1, 0.0)

		#bucle principal
		while( self._running ):
			time = clock.tick(cuadrado.vel + cuadrado.subvel) #ACA PARA CAMBIAR LA VELOCIDAD
			#timeCuadrado = clock.tick(1000)
			keys = pygame.key.get_pressed()
			cuadrado.mover(keys)
			cuadrado.girar(keys)
			for event in pygame.event.get():
				self.on_event(event, keys)
			self.on_loop(keys)
			self.on_render()
		self.on_cleanup()


class Cuadrado(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_cuadrado = pygame.image.load("cuadrado.jpg")
		self.fondo = pygame.image.load("fondo.jpg")
		self.c2 = pygame.image.load("c2.jpg")
		self.barra = pygame.image.load("barra.jpg")
		self.rect = self.image_cuadrado.get_rect()
		self.nueva_p = True
		self.enx = 0
		self.printeado = False
		self.figura = 0
		self.pos_x = 5
		self.pos_y = 0
		self.angulo = 0
		self.vel = 4
		self.cnt_linea = [0]*23
		self.puntos = 0
		self.comprobar = 0
		self.end = False
		self.subvel = 0


	#Funcion que piensa todo
	def brain(self):
		#Perder
		for i in xrange (3):
			for j in xrange(len(theApp.pantalla[0])):
				if theApp.pantalla[i][j] == 2 and j != 11:
					self.end = True
					break
		if self.end == False:
			colision = 1
			brr = theApp.fig[self.figura][4][0][0] #variable de borrado
			for n in xrange(brr) :
				for k in xrange(brr) :
					if theApp.pantalla[self.pos_y+n-((brr-1)/2)][self.pos_x+k-((brr-1)/2)] != 2:
						theApp.pantalla[self.pos_y+n-((brr-1)/2)][self.pos_x+k-((brr-1)/2)] = 0
			n=len(theApp.fig[self.figura][self.angulo])-1
			while n >= 0:
				for k in xrange(len(theApp.fig[self.figura][self.angulo][n])) :
					if theApp.pantalla[self.pos_y+n+1][self.pos_x+k] == 2 and theApp.fig[self.figura][self.angulo][n][k] == 1:
						colision = 2
						break
				n -= 1
			for n in xrange(len(theApp.fig[self.figura][self.angulo])) :
				for k in xrange(len(theApp.fig[self.figura][self.angulo][n])) :
					if theApp.pantalla[self.pos_y+n][self.pos_x+k] != 2:
						theApp.pantalla[self.pos_y+n][self.pos_x+k] = theApp.fig[self.figura][self.angulo][n][k]*colision
						if theApp.pantalla[self.pos_y+n][self.pos_x+k] == 2:
							self.cnt_linea[self.pos_y+n] += 1
	#		print self.cnt_linea
			if colision == 2 :
				self.nueva_p = True
			aumentar_velocidad = self.puntos - 5*self.comprobar
			if aumentar_velocidad == 3:
				self.comprobar += 1
				self.vel += 1

	def linea(self):
		if self.end == False:
			n = 21
			while n >= 0:
				n -= 1
				#print self.cnt_linea
				if self.cnt_linea[n] == 11:
					s = n
					self.puntos += 1
					while s >= 0:
						for k in xrange(len(theApp.pantalla[0])):
							theApp.pantalla[s][k] = theApp.pantalla[s-1][k]
							self.cnt_linea[s] = self.cnt_linea[s-1]
						s -= 1
					

	def mover(self, keys):
		if self.end == False:
			if keys[K_RIGHT] and self.pos_x < 12 and theApp.pantalla[self.pos_y][self.pos_x+len(theApp.fig[self.figura][self.angulo][0])] != 2: 
				self.pos_x += 1
			if keys[K_LEFT] and self.pos_x > 0 and theApp.pantalla[self.pos_y][self.pos_x-1] != 2:
				self.pos_x -= 1
			
					
	def girar(self, keys):
		if self.end == False:
			if keys[K_SPACE]:
				if self.angulo < 3:
					self.angulo += 1
				else:
					self.angulo = 0

	def caida(self):
		if self.end == False:
			self.pos_y += 1
			
	def posicionar(self) :
		if self.nueva_p == True and self.end == False:
			self.figura = random.randint(0,6)
			self.angulo = random.randint(0,3)
			self.pos_x = 5
			self.pos_y = 0
			self.nueva_p = False

	def velocidad(self, keys):
		if self.end == False:
			if keys[K_DOWN]:
				self.subvel = 15
			if not keys[K_DOWN]:
				self.subvel = 0

	def printeo(self) :
		for i in xrange(len(theApp.pantalla)):
			for k in xrange(len(theApp.pantalla[0])):
				if theApp.pantalla[i][k] == 1:
					theApp._display_surf.blit(self.image_cuadrado,(30*k,30*i))
				elif theApp.pantalla[i][k] == 2:
					theApp._display_surf.blit(self.c2,(30*k,30*i))
				elif theApp.pantalla[i][k] == 0:
					theApp._display_surf.blit(self.fondo,(30*k,30*i))
				if i==21 and theApp.pantalla[i][k] == 2:
					theApp._display_surf.blit(self.barra,(30*k,30*i))
		self.printeado = True


if __name__ == "__main__" :
	cuadrado = Cuadrado()
	theApp = App()
	theApp.on_execute()

