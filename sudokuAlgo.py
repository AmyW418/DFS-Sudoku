# This file contains the methods for running a depth first search on a sudoku puzzle

import numpy as np

# get the coordinates for blank spaces in grid, return in array
# i.e. input[2][3] as 23
def getBlanks(input):
	blanks = []
	for row in range(len(input)):
		for col in range(len(input[row])):
			if (input[row][col] == 0):
				blanks.append((row*10)+col)
	return blanks

# convert blanks back to cordinates
# 23 back to 2 and 3
def unconvertBlanks(blank):
	x = blank//10
	y = blank%10
	return x, y

# check if move is valid in a 3 by 3 grid
# convert each box to the one on top left of the nine 3x3 grids and check the rest
# ie. if check [4][5], check grid starting from [3][3] to [5][5]
def check3x3(num, blank, input):
	x, y = unconvertBlanks(blank)
	corner = [0,3,6]
	while(x not in corner):
		x -= 1
	while(y not in corner):
		y -= 1
	for row in range(3):
		for col in range(3):
			if (input[x+row][y+col]==num):
				return 1
	return 0

# check if move is valid in a column
def colCheck(testval, blank, input):
	x,y = unconvertBlanks(blank)
	for row in range(9):
		if(input[row][y] == testval):
			return 1
	return 0

# check if move is valid in a row
def rowCheck(testval, blank, input):
	x,y = unconvertBlanks(blank)
	for col in range(9):
		if(input[x][col] == testval):
			return 1
	return 0

# back tracking to previously tried number, 
# reduce count, empty box/guess and proceed again with new number
def backtrack(count, input, blankSpace, x, y):
	count -= 1
	input[x][y] = 0
	if count < 0:
		return ("error")
	return dfsAlgo(blankSpace, input, count)


# Depth first search, fills blank with first number that works and continues
# if reaches a problem, back tracks one box and tries the next number.
# if problem again, keep back tracking and continue until we find one that works
def dfsAlgo(blankSpace, input, count):
	nums = [0,1,2,3,4,5,6,7,8,9]
	blank = blankSpace[count]
	x,y = unconvertBlanks(blank) 
	val = input[x][y]    #value of data at coordinates in input
	if(val==0):    # current box is empty, start trying from 1
		for num in range(len(nums)-1): 
			next = num+1
			if(rowCheck(nums[next], blank, input)==0 and colCheck(nums[next], blank, input)==0 and check3x3(nums[next], blank, input)==0):
				input[x][y] = nums[next]
				count += 1
				if (count == len(blankSpace)):
					return input
				return dfsAlgo(blankSpace, input, count)
		return backtrack(count, input, blankSpace, x, y)
	else: # current box is not empty, start trying from next number
		prev = nums.index(val)
		for numsleft in range(len(nums)-prev-1): # get whats left in options to try ** minus one cuz range starts at 0  
			next = prev+numsleft+1 #index of next number to try ** added one cuz range started at 0 and needed to compensate ^^
			if(rowCheck(nums[next], blank, input)==0 and colCheck(nums[next], blank, input)==0 and check3x3(nums[next], blank, input)==0):
				input[x][y] = nums[next]
				count += 1
				if (count == len(blankSpace)):
					return input
				return dfsAlgo(blankSpace, input, count)
		return backtrack(count, input, blankSpace, x, y)


# testing main method for Depth First Search algorithm
def main(): 
	input = [
		[1, 0, 0, 0, 0, 0, 0, 0, 3],
		[0, 0, 7, 2, 6, 0, 4, 8, 0],
		[4, 0, 0, 9, 3, 5, 0, 0, 6],
		[0, 3, 0, 4, 8, 0, 2, 0, 0],
		[0, 4, 1, 6, 0, 9, 3, 0, 0],
		[0, 0, 6, 0, 0, 0, 8, 9, 0],
		[5, 7, 8, 0, 4, 0, 0, 0, 2],
		[0, 0, 0, 3, 0, 0, 0, 7, 0],
		[2, 0, 0, 0, 0, 0, 0, 0, 5]
	]

	blankSpace = getBlanks(input) # testing if successfully got empty spaces
	final = dfsAlgo(blankSpace, input, 0)
	print(final)

main()