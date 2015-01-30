import sys, pygame
pygame.init()

class BreakIt(Exception): pass

class cell:
	def __init__(self, pos, field, surface):
		self.pos = pos
		self.mine = False
		self.revealed = False
		self.flagged = False
		self.sprite = pygame.image.load("sprites\square.png")
		self.surface = surface
		self.field = field

		x = self.pos[0]
		y = self.pos[1]
		

		#Determines type of square (corner, edge, inside)
		if (x == 0 or x == 7) and (y == 0 or y == 7):
			self.type = 'corner'
		elif x == 0 or x == 7 or y == 0 or y == 7:
			self.type = 'edge'
		else:
			self.type = 'inside'

		
	def determineneighbours(self):
		#Determines the coordinates of the squares adjacent to the square and further categorizes the square
		if self.type == 'corner':
			if self.pos == (0,0): #top left
				self.type = 'top left corner'
				self.neighbours = [self.field[x+1][y], self.field[x][y+1], self.field[x+1][y+1]]
			elif self.pos == (7,0): #top right
				self.type = 'top right corner'
				self.neighbours = [self.field[x-1][y], self.field[x-1][y+1], self.field[x][y+1]]
			elif self.pos == (0,7): #bottom left
				self.type = 'bottom left corner'
				self.neighbours = [self.field[x][y-1], self.field[x+1][y], self.field[x+1][y-1]]
			elif self.pos == (7,7): #bottom right
				self.type = 'bottom right corner'
				self.neighbours = [self.field[x-1][y-1], self.field[x-1][y], self.field[x][y-1]]
		elif self.type == 'edge':
			if y == 0 and (1 <= x and x <= 6): #top
				self.type = 'top edge'
				self.neighbours = [self.field[x-1][y], self.field[x-1][y+1], self.field[x][y+1], self.field[x+1][y+1], self.field[x+1][y]]
			elif y == 7 and (1 <= x and x <= 6): #bottom
				self.type = 'bottom edge'
				self.neighbours = [self.field[x-1][y], self.field[x-1][y-1], self.field[x][y-1], self.field[x+1][y-1], self.field[x+1][y]]
			elif x == 0 and (1 <= y and y <= 6): #left
				self.type = 'left edge'
				self.neighbours = [self.field[x][y-1], self.field[x+1][y-1], self.field[x+1][y], self.field[x+1][y+1], self.field[x][y+1]]
			elif x == 7 and (1 <= y and y <= 6): #right
				self.type = 'right edge'
				self.neighbours = [self.field[x][y-1], self.field[x-1][y-1], self.field[x-1][y], self.field[x-1][y+1], self.field[x][y+1]]
		elif self.type == 'inside':
			self.neighbours = [self.field[x-1][y-1], self.field[x][y-1], self.field[x+1][y-1], self.field[x+1][y], self.field[x+1][y+1], self.field[x][y+1], self.field[x-1][y+1], self.field[x-1][y]]

		#Determines the number of mines in adjacent squares
		self.count = 0
		for cell in self.neighbours:
			if cell.mine == True:
				self.count += 1

		#Loads the sprite of the revealed square
		path = "sprites\\" + str(self.count) + ".png"
		self.sprite_revealed = pygame.image.load(path)


	def make_mine(self):
		"""Puts a mine on the cell"""
		self.mine = True


	def determinenumber(self, field):
		"""Determines the number of mines in adjacent squares"""
		count = 0
		for cell in self.neighbours:
			if cell.mine == True:
				count += 1

	def reveal(self, field):
		"""Reveals the square"""
		if self.revealed == True or self.flagged == True:
			pass
		else:
			if self.mine == False:
				if self.count == 0:
					self.revealed = True
					self.sprite = pygame.image.load("sprites\\0.png")
					tocheck = []
					for neighbour in self.neighbours:
						if neighbour.revealed == False and neighbour not in tocheck:
							tocheck.append(neighbour)
						else:
							self.revealed = True
					newlist = []
					for i in tocheck:
						if i not in newlist:
							newlist.append(i)
					for neighbour in newlist:
						neighbour.reveal(field)
				else:
					self.revealed = True
					path = "sprites" + "\\" + str(self.count) + ".png"
					self.sprite = pygame.image.load(path)
			else:
				self.sprite = pygame.image.load("sprites\mine.png")
			drawsquare(self, self.surface)
		return None

	def flag(self, field):
		if self.revealed != True:
			if self.flagged != True:
				self.flagged = True
				self.sprite = pygame.image.load("sprites\\flag.png")
			else:
				self.flagged = False
				self.sprite = pygame.image.load("sprites\\square.png")
			drawsquare(self, self.surface)
		return None
		

#------------------------------------------------------------------------------------------------------------------


def setmines(mine_list):
	"""Puts mines on the cells specified in *args"""
	for arg in mine_list:
		grid[arg[0]][arg[1]].make_mine()


def listmines(field):
	"""lists the coordinates of all the cells with mines"""
	mines = []
	for y in range(8):
		for x in range(8):
			if field[x][y].mine == True:
				mines.append(field[x][y].pos)
	return mines


def checkmine(square):
	"""Returns true if the square contains a mine"""
	return square.mine


def drawsquare(square, surface):
	"""Draws the square"""
	squarex = (square.pos[0]*16) + 7
	squarey = (square.pos[1]*16) + 30
	surface.blit(square.sprite, (squarex, squarey))
	pygame.display.flip()

def press(square, surface):
	"""Presses the square the mouse is click+holding"""
	squarex = (square.pos[0]*16) + 7
	squarey = (square.pos[1]*16) + 30
	pressed_sprite = pygame.image.load("sprites\\square_pressed.png")
	surface.blit(pressed_sprite, (squarex, squarey))
	pygame.display.flip()

def depress(square, surface):
	"""Depresses the square the mouse has moved from"""
	squarex = (square.pos[0]*16) + 7
	squarey = (square.pos[1]*16) + 30
	pressed_sprite = pygame.image.load("sprites\\square.png")
	surface.blit(pressed_sprite, (squarex, squarey))
	pygame.display.flip()

#------------------------------------------------------------------------------------------------------------------

#Create the grid
grid = [[[] for i in range(8)] for k in range(8)]

#Graphics initializations
screensize = width, height = 142, 165
screen = pygame.display.set_mode(screensize)
grey = 192, 192, 192
screen.fill(grey)

#Populate the grid
for y in range(8):
	for x in range(8):
		grid[x][y] = cell((x,y), grid, screen)
		drawsquare(grid[x][y], screen)

#Places mines on the grid
#NOTE: This must run before the codeblock generating neighbours for each cell
minelist = [(3, 0), (5, 0), (3, 1), (1, 3), (4, 3), (1, 4), (2, 4), (6, 4), (1, 6), (5, 7)]
setmines(minelist)
print "There are mines at ", listmines(grid)

#Generates neighbours for each cell
for y in range(8):
	for x in range(8):
		grid[x][y].determineneighbours()


#Main game loop
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mousepos = pygame.mouse.get_pos()
			mousex, mousey = mousepos[0]-7, mousepos[1]-30
			if 0 <= mousex and mousex <= 128 and 0 <= mousey and mousey <= 128:
				squarex, squarey = (mousex)/16, (mousey)/16
				if grid[squarex][squarey].revealed == False and grid[squarex][squarey].flagged == False:
					press(grid[squarex][squarey], screen)
					dontdepress = False
				else:
					dontdepress = True
				try:
					while 1:
						for event in pygame.event.get():
							if event.type != pygame.MOUSEBUTTONUP:
								mousepos = pygame.mouse.get_pos()
								mousex, mousey = mousepos[0]-7, mousepos[1]-30
								if 0 <= mousex and mousex <= 127 and 0 <= mousey and mousey <= 127:
									if 'oldsquarex' not in globals():
										pass
									else:
										if grid[oldsquarex][oldsquarey].revealed == True or grid[oldsquarex][oldsquarey].flagged == True:
											print "oldsquarex is in globals"
											dontdepress = True
									oldsquarex, oldsquarey = squarex, squarey
									squarex, squarey = (mousex)/16, (mousey)/16
									print("({0}, {1})".format(squarex, squarey))
									if grid[squarex][squarey].revealed == False and grid[squarex][squarey].flagged == False:
										if squarex != oldsquarex or squarey != oldsquarey:
											if dontdepress == True:
												dontdepress = False
											else:
												depress(grid[oldsquarex][oldsquarey], screen)
											press(grid[squarex][squarey], screen)
										else:
											oldsquarex, oldsquarey = squarex, squarey
											squarex, squarey = (mousex)/16, (mousey)/16
											press(grid[squarex][squarey], screen)
							else:
								raise BreakIt
				except BreakIt:
					pass
						
				if event.button == 1:
					print("({0}, {1})".format(squarex, squarey))
					grid[squarex][squarey].reveal(grid)
				elif event.button == 3:
					grid[squarex][squarey].flag(grid)



while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif pygame.mouse.get_pressed()[0] == True or pygame.mouse.get_pressed()[2] == True:
			mousepos = pygame.mouse.get_pos()
			mousex, mousey = mousepos[0]-7, mousepos[1]-30
			if 0 <= mousex and mousex <= 128 and 0 <= mousey and mousey <= 128:
				squarex = (mousex)/16
				squarey = (mousey)/16
				if 0 <= squarex and squarex <= 7 and 0 <= squarey and squarey <= 7:
					if pygame.mouse.get_pressed()[0] == True:
						print("({0}, {1})".format(squarex, squarey))
						grid[squarex][squarey].reveal(grid)
					elif pygame.mouse.get_pressed()[2] == True:
						#grid[squarex][squarey].flag(grid)
						print grid[squarex][squarey].revealed
			pygame.display.flip()


"""
TODO:

Make single-left-clicking revealed/flagged squares does nothing

Merge functions press() and depress() into one function, with the press/depress state as an argument

Click numbers to reveal squares

Randomized mine placement

New game

Reset board

Intermediate, Expert, Custom difficulties

"""