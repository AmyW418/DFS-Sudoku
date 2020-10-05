# This file contains the gui for displaying and playing the game with pygame

import sys, pygame, time, random
from pygame.locals import *
from sudokuAlgo import getBlanks, dfsAlgo
from boards import boardsArray

pygame.font.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (169,169,169)
DARKGRAY = (115, 115, 115)
LIGHTBLUE = (77, 184, 255)
BLUE = (0, 0, 255)
DARKBLUE = (26, 163, 255)
GREEN = (47, 182, 47)
DARKGREEN = (37, 142, 37)
RED = (255, 0, 0)

# class that defines the puzzle as a whole
class Grid:

	#constructor for a Grid
	def __init__(self, rows, cols, width, height, boardnum):
		self.rows = rows
		self.cols = cols
		self.width = width
		self.height = height
		self.board = boardsArray[boardnum]
		self.square = [[Square(self.board[i][j], i, j, width/9, width/9) for j in range(cols)] for i in range(rows)]
		self.matrix = None

	#draw the overall sudoku puzzle
	def draw(self, window):
        # Draw Grid Lines
		gap = self.width / 9
		for i in range(self.rows+1):
			if i % 3 == 0: thick = 3
			else: thick = 1
			pygame.draw.line(window, BLACK, (0, i*gap+50), (self.width, i*gap+50), thick)
			pygame.draw.line(window, BLACK, (i * gap, 50), (i * gap, self.height+50), thick)
		# Draw numbers in the individual squares
		for i in range(self.rows):
			for j in range(self.cols):
				self.square[i][j].draw(window)
	
	# highlight the box in blue where user clicked
	def highlight(self, x, y):
		for i in range(self.rows):
			for j in range(self.cols):
				self.square[i][j].selected = False

		self.square[x][y].selected = True

	# detect whether a position inside the grid is clicked on UI
	def clickedbox(self, position):
		if (position[0] < self.width) and (50 < position[1] < self.height+50):
			gap = self.width / 9
			y = position[0] // gap
			x = (position[1]-50) // gap
			return (int(x), int(y))
		else:
			return None
	
	# change value of a square
	def changeVal(self, i, j, key):
		self.square[i][j].changeSqVal(key)
	
	# make copy of input grid
	def setMatrix(self):
		self.matrix = [[self.square[i][j].value for j in range(self.cols)]for i in range(self.rows)]
	
	# make a copy of grid with all inputs to prepare to check against actual solution
	def setUserSolution(self):
		for i in range(self.rows):
			for j in range(self.cols):
				if (self.square[i][j].value == 0):
					self.square[i][j].value = self.square[i][j].temp
		self.setMatrix()
		return self.matrix

	# check user solution with dfs calculated solution
	def checkUserSolution(self, userSolution, actualSolution):
		errors = 0
		for i in range(self.rows):
			for j in range(self.cols):
				if(userSolution[i][j] != actualSolution[i][j]):
					self.square[i][j].error = actualSolution[i][j]
					errors += 1
		return errors

	# call on dfs algorithm to get the solution of given board
	def getSolution(self):
		blankSpace = getBlanks(self.matrix)
		final = dfsAlgo(blankSpace, self.matrix, 0)
		return(final)
	
	# display solution on UI
	def showSolution(self, solution):
		for i in range(self.rows):
			for j in range(self.cols):
				if (self.square[i][j].value == 0):
					self.square[i][j].temp = solution[i][j]


# class that defines each box / square in the puzzle
class Square:
	
	# constructor for a Square
	def __init__(self, value, row, col, width ,height):
		self.value = value
		self.temp = 0
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.selected = False
		self.error = 0
		
	# draw the values entered for puzzle with their corresponding colors
	# Black for already there, grey for user entered, and red for errors
	def draw(self, window):
		fonts = pygame.font.SysFont("arial", 50)
		x = self.col * self.width
		y = self.row * self.height + 50
		

		if self.error != 0:
			text = fonts.render(str(self.error), 1, RED)
			window.blit(text, (x + (self.width/2 - text.get_width()/2), y + (self.height/2 - text.get_height()/2)))
		elif self.value != 0:
			text = fonts.render(str(self.value), 1, BLACK)
			window.blit(text, (x + (self.width/2 - text.get_width()/2), y + (self.height/2 - text.get_height()/2)))
		elif self.temp != 0:
			text = fonts.render(str(self.temp), 1, GRAY)
			window.blit(text, (x + (self.width/2 - text.get_width()/2), y + (self.height/2 - text.get_height()/2)))
		elif self.value == 0 and self.temp == 0:
			pygame.draw.rect(window, WHITE, (x+5,y+5, self.width-7, self.height-7))


		if self.selected:
			pygame.draw.rect(window, BLUE, (x,y, self.width, self.height), 3)
	
	# change the value of the box
	def changeSqVal(self, key):
		self.temp = key

# Handles UI for clicking New Game button
def newGameButton(window):
	pygame.draw.rect(window, GRAY, (5, 5, 110, 40))
	mouse = pygame.mouse.get_pos()
	if (5 < mouse[0] < 5+110) and (5 < mouse[1] < 5+40):
		pygame.draw.rect(window, DARKGRAY, (5, 5, 110, 40))
	
	fonts = pygame.font.SysFont("arial", 20)
	text = fonts.render("New Game", 1, WHITE)
	window.blit(text, (9.5, 12))

def clickNewGame(position):
	if(5 < position[0] < 5+110) and (5 < position[1] < 5+40):
		return True

# Handles UI for clicking solution button
def solutionButton(window):
	pygame.draw.rect(window, LIGHTBLUE, (10, 602, 100, 40))
	mouse = pygame.mouse.get_pos()
	if (10 < mouse[0] < 10+100) and (602 < mouse[1] < 602+40):
		pygame.draw.rect(window, DARKBLUE, (10, 602, 100, 40))
	fonts = pygame.font.SysFont("arial", 20)
	text = fonts.render("Solution", 1, BLACK)
	window.blit(text, (25, 610))

def clickSolution(position):
	if(10 < position[0] < 10+100) and (602 < position[1] < 602+40):
		return True

# Handles UI for clicking submit button
def submitButton(window):
	pygame.draw.rect(window, GREEN, (430, 602, 100, 40))
	mouse = pygame.mouse.get_pos()
	if (430 < mouse[0] < 430+100) and (602 < mouse[1] < 602+40):
		pygame.draw.rect(window, DARKGREEN, (430, 602, 100, 40))
	
	fonts = pygame.font.SysFont("arial", 20)
	text = fonts.render("Submit", 1, BLACK)
	window.blit(text, (450, 610))

def clickSubmit(position):
	if(430 < position[0] < 430+100) and (602 < position[1] < 602+40):
		return True

# checks the solved board to get errors
def checkSolved(board, userfinal):
	for i in range(board.rows):
		for j in range(board.cols):	
			if (board.square[i][j].value == 0 and board.square[i][j].temp==0):
				return None
			else:
				userfinal[i][j] = board.square[i][j]
	return userfinal

# check if there are any empty spaces
def notFinished(window, done):
	if done == 1:
		fonts = pygame.font.SysFont("arial", 20)
		text = fonts.render("There are still empty spaces!", 1, BLACK)
		window.blit(text, (145, 607))

# calculate and show time player used
def timer(window,time):
    fnt = pygame.font.SysFont("arial", 20)
    text = fnt.render("Time:  " + ftime(time), 1, (0,0,0)) 
    window.blit(text,(410, 15))

def ftime(seconds):
	sec = seconds%60
	min = seconds//60
	hour = min//60
	if (min == 0) and (hour == 0):
		time = str(sec) + ' sec'
	elif (min > 0) and (hour == 0):
		if (sec < 10):
			time =  str(min) + ":0" + str(sec)
		else:
			time =  str(min) + ":" + str(sec)
	elif (hour > 0):
		time = str(hour)+":" + str(min) + ":" + str(sec)
	return time

# show the amount of errors user had
def showErrors(window, errors):
	fnt = pygame.font.SysFont("arial", 20)
	text = fnt.render("Errors:  " + str(errors), 1, (0,0,0)) 
	if errors != -1:
		window.blit(text,(230, 15))

# main function for running the game
def main():
	window = pygame.display.set_mode((540,650))
	window.fill(WHITE)
	pygame.display.set_caption("Sudoku")
	board = Grid(9, 9, 540, 540, 0)
	run = True
	key = None
	start = time.time()	
	highlighted = []
	done = -1
	errors = -1

	while run:	
		userfinal = [[0 for i in range(9)] for j in range(9)]
		play_time = round(time.time() - start)
		strikes = 1
		

		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				done = -1
				clickpos = pygame.mouse.get_pos()
				
				squarepos = board.clickedbox(clickpos)
				if squarepos:
					board.highlight(squarepos[0], squarepos[1])

				newGamepos = clickNewGame(clickpos)
				if newGamepos:
					errors = -1
					boardnum = random.randint(0, len(boardsArray)-1)
					board = Grid(9, 9, 540, 540, boardnum)
					start = time.time()

				solutionpos = clickSolution(clickpos)
				if solutionpos:
					if errors == -1:
						board.setMatrix()
						solution = board.getSolution()
						board.showSolution(solution)

				submitpos = clickSubmit(clickpos)
				if submitpos:
					userfinal = checkSolved(board, userfinal)
					if userfinal:
						done = 0
						if errors == -1:
							board.setMatrix()
							solution = board.getSolution()
							userSolution = board.setUserSolution()
							errors = board.checkUserSolution(userSolution, solution)
					else: 
						done = 1

				highlighted = []
				for i in range(board.rows):
					for j in range(board.cols):
						if(board.square[i][j].selected == True):
							highlighted.append((i, j))
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					key = 1
				if event.key == pygame.K_2:
					key = 2
				if event.key == pygame.K_3:
					key = 3
				if event.key == pygame.K_4:
					key = 4
				if event.key == pygame.K_5:
					key = 5
				if event.key == pygame.K_6:
					key = 6
				if event.key == pygame.K_7:
					key = 7
				if event.key == pygame.K_8:
					key = 8
				if event.key == pygame.K_9:
					key = 9
				if event.key == pygame.K_BACKSPACE:
					key = 0
				
		if highlighted and key != None:
			board.changeVal(highlighted[0][0],highlighted[0][1], key)
			key = None

		
		window.fill(WHITE)
		newGameButton(window)
		solutionButton(window)
		submitButton(window)
		notFinished(window, done)
		board.draw(window)
		showErrors(window, errors)
		timer(window,play_time)
		pygame.display.update()

main()