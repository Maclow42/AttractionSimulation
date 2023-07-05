from math import*
from vpython import*

class Objet:
	"""class définissant un objet"""

	def __init__(self, name : str, masse : int, radius : int):
		self.name = name
		self.mass = masse
		self.radius = radius

	def __repr__(self):
		return self.name

class Espace:
	"""class définissant l'espace d'étude"""

	def __init__(self, g=6.7e-11):
		self.G = g
		self.objets = {}

	def add(self, obj : Objet, VectPos : vector, VectV : vector, color : vector, make_trail=True, trail_type='points', interval=10, retain=100):
		"""ajoute un objet définit les conditions initiales d'Objet en prenant sa position, sa vitesse initiale et son angle de lancer"""

		#On ajoute au dictionnaire une sphere crée à partir des caractéristiques de l'objet passé en paramètre
		self.objets[obj] = sphere(pos=VectPos, radius=obj.radius, color=color, 
                			make_trail=make_trail, trail_type=trail_type, interval=interval, retain=retain)
		self.objets[obj].mass = obj.mass
		self.objets[obj].p = VectV * self.objets[obj].mass #On utilise la quantité de matière

		#Initialisation des conditions initiales
		self.objets[obj].posInit = VectPos
		self.objets[obj].V0 = VectV
		#Initialisation de la position
		self.objets[obj].pos = VectPos

		#self.objets[obj].id = randint(0, 1e8)

		return True

	def setPseudoRef(self, referentiel : Objet):
		#Si mle référentiel choisit n'est pas ajouté dans l'espace
		if referentiel not in self.objets:
			raise NameError('Referentiel Objet was not added in Espace.')
			return False
		#Sinon
		else:
			self.ref = referentiel
			return True

	def start(self, dt, f=200, stopIfCollision=True):
		"""Lance la simulation"""

		#Création d'un dictionnaire contenant toutes les positions des objets
		dictPos = {}
		for clef, obj in self.objets.items():
			dictPos[clef] = [obj.pos]

		#GlowScript 3.0 VPython
		scene.caption = """To rotate "camera", drag with right button or Ctrl-drag.
						To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
						  On a two-button mouse, middle is left + right.
						To pan left/right and up/down, Shift-drag.
						Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
		scene.background = color.black

		collision = False
		while collision is False:
			#Fréquence de la boucle
			rate(f)

			#On centre la scene sur le référentiel
			#Si un référentiel a été définit (sinon le programme gère seul)
			if hasattr(self, 'ref'):
				scene.center = self.objets[self.ref].pos

			#On fait le bilan des forces pour chaque objet
			for clef, obj in self.objets.items():
				#On fait une liste de toutes les forces qui s'exercent sur lui
				listF = []
				#On calcule la force avec chacun des autres objets
				for clef2, other in self.objets.items():
					#On evite qu'il interagisse avec lui-même
					if other != obj:
						d = other.pos - obj.pos
						#Si il y a collision
						if mag(d) < other.radius + obj.radius:
							collision = True
							print("Collision beetween {} and {}".format(clef, clef2))
							return dictPos
						else :
							try :
								F = self.G * obj.mass * other.mass / mag(d)**2 *d.hat
							#Si les deux objets sont en contact, la force est nulle
							except ZeroDivisionError:
								listF.append(vector(0,0,0))
							#Sinon, on ajoute la Force au BDF
							else:
								listF.append(F)
				#On calcule la somme des forces
				sF = vector(0,0,0)
				for F in listF:
					sF += F
				#On calcule la prochaine position pour chaque objet
				obj.nextp = obj.p + sF*dt
				obj.nextpos = obj.pos + (obj.p/obj.mass) * dt

			#On applique les nouvelles positions
			for clef, obj in self.objets.items():
				obj.p = obj.nextp
				obj.pos = obj.nextpos
				dictPos[clef].append(obj.pos)

		return dictPos



"""PROGRAMME"""

def randomTest():#Quelques objets
	tera = Objet("tera", 7e32, 8e10)
	giant = Objet("giant", 3e32, 8e10)
	dwarf = Objet("dwarf", 9e31, 8e10)

	sun = Objet("Sun", 2e32, 7e10)
	earth = Objet("Earth", 6e24, 8e10)
	moon = Objet("Moon", 7e22, 8e10)

	ref = Objet("Ref", 0, 0)

	#Création de l'espace
	space = Espace()

	#Ajout des objets dans l'espace
	space.add(tera, vector(9e12, 0, 0), vector(-1e3, 0, 1e3), color.red)
	space.add(dwarf, vector(-5e12, 0, 0), vector(0, -2e4, 0), color.white)
	space.add(giant, vector(9e12, 1e12, 9e12), vector(-1e3, 5e4, 1e3), color.green)
	space.add(sun, vector(-9e12, 1e12, -9e12), vector(-1e1, 5e2, 1e1), color.yellow)

	#Definition du referentiel
	space.setPseudoRef(giant)

	#Starting
	result = space.start(1e5,200)

def EarthMoon():
	#Quelques objets
	earth = Objet("Earth", 6e24, 6e3)
	moon = Objet("Moon", 7e22, 1e3)

	#Création de l'espace
	space = Espace()
	#Ajout des objets dans l'espace
	space.add(earth, vector(0, 0, 0), vector(0, 0, 0), color.blue)
	space.add(moon, vector(2e5, 0, 0), vector(0, 0, 0), color.white)

	#Definition du referentiel
	space.setPseudoRef(earth)

	#Starting
	result = space.start(1,200)

randomTest()

	