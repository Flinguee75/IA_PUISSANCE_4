import numpy as np
import random
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

Nombre_Ligne = 6
Nombre_Collones = 7

JOUEUR = 0
AI = 1

VIDE = 0
JOUEUR_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def crée_plateau():
	plateau = np.zeros(( Nombre_Ligne,Nombre_Collones))
	return plateau

def poser_piece(plateau, row, col, piece):
	plateau[row][col] = piece

def est_libre(plateau, col):
	return np.all(plateau[ Nombre_Ligne-1][col] == 0)

def ligne_suivante(plateau, col):
	for r in range( Nombre_Ligne):
		if np.all(plateau[r][col] == 0):
			return r

def print_plateau(plateau):
	print(np.flip(plateau, 0))

def coup_gagnant(plateau, piece):
	# Check alignement horizontal
	for c in range(Nombre_Collones-3):
		for r in range( Nombre_Ligne):
			if plateau[r][c] == piece and plateau[r][c+1] == piece and plateau[r][c+2] == piece and plateau[r][c+3] == piece:
				return True

	# Check alignement vertical
	for c in range(Nombre_Collones):
		for r in range( Nombre_Ligne-3):
			if plateau[r][c] == piece and plateau[r+1][c] == piece and plateau[r+2][c] == piece and plateau[r+3][c] == piece:
				return True

	#  Check alignement diagonale ascendant
	for c in range(Nombre_Collones-3):
		for r in range( Nombre_Ligne-3):
			if plateau[r][c] == piece and plateau[r+1][c+1] == piece and plateau[r+2][c+2] == piece and plateau[r+3][c+3] == piece:
				return True

		#  Check alignement diagonale descendant
	for c in range(Nombre_Collones-3):
		for r in range(3,  Nombre_Ligne):
			if plateau[r][c] == piece and plateau[r-1][c+1] == piece and plateau[r-2][c+2] == piece and plateau[r-3][c+3] == piece:
				return True

def evaluation_plateau(window, piece):
	score = 0
	opp_piece = JOUEUR_PIECE
	if piece == JOUEUR_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(VIDE) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(VIDE) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(VIDE) == 1:
		score -= 4

	return score

def score_position(plateau, piece):
	score = 0

	## Score collones centrales
	center_array = [int(i) for i in list(plateau[:, Nombre_Collones//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range( Nombre_Ligne):
		row_array = [int(i) for i in list(plateau[r,:])]
		for c in range(Nombre_Collones-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluation_plateau(window, piece)

	## Score Vertical
	for c in range(Nombre_Collones):
		col_array = [int(i) for i in list(plateau[:,c])]
		for r in range( Nombre_Ligne-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluation_plateau(window, piece)

	## Score diagonale ascendante
	for r in range( Nombre_Ligne-3):
		for c in range(Nombre_Collones-3):
			window = [plateau[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluation_plateau(window, piece)
		
	## Score diagonale descdante

	for r in range( Nombre_Ligne-3):
		for c in range(Nombre_Collones-3):
			window = [plateau[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluation_plateau(window, piece)

	return score

def est_terminé(plateau):
	return coup_gagnant(plateau, JOUEUR_PIECE) or coup_gagnant(plateau, AI_PIECE) or len(get_positions_valides(plateau)) == 0

def minimax_alphabeta(plateau, depth, alpha, beta, maximizingJOUEUR):
	positions_valides = get_positions_valides(plateau)
	#print(positions_valides)
	est_fini = est_terminé(plateau)
	if depth == 0 or est_fini:
		if est_fini:
			if coup_gagnant(plateau, AI_PIECE):
				return (None, 100000000000000)
			elif coup_gagnant(plateau, JOUEUR_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(plateau, AI_PIECE))
	if maximizingJOUEUR:
		value = -math.inf
		column = random.choice(positions_valides)
		for col in positions_valides:
			row = ligne_suivante(plateau, col)
			b_copy = plateau.copy()
			poser_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax_alphabeta(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing JOUEUR
		value = math.inf
		column = random.choice(positions_valides)
		for col in positions_valides:
			row = ligne_suivante(plateau, col)
			b_copy = plateau.copy()
			poser_piece(b_copy, row, col, JOUEUR_PIECE)
			new_score = minimax_alphabeta(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value
	
def minimax(plateau, depth, maximizingJOUEUR):
    positions_valides = get_positions_valides(plateau)
    est_fini = est_terminé(plateau)
    
    if depth == 0 or est_fini:
        if est_fini:
            if coup_gagnant(plateau, AI_PIECE):
                return (None, 100000000000000)
            elif coup_gagnant(plateau, JOUEUR_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(plateau, AI_PIECE))
    
    if maximizingJOUEUR:
        value = -math.inf
        column = random.choice(positions_valides)
        
        for col in positions_valides:
            row = ligne_suivante(plateau, col)
            b_copy = plateau.copy()
            poser_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
        
        return column, value
                
    else: # Minimizing JOUEUR
        value = math.inf
        column = random.choice(positions_valides)
        
        for col in positions_valides:
            row = ligne_suivante(plateau, col)
            b_copy = plateau.copy()
            poser_piece(b_copy, row, col, JOUEUR_PIECE)
            new_score = minimax(b_copy, depth-1, True)[1]
            
            if new_score < value:
                value = new_score
                column = col
        
        return column, value


def get_positions_valides(plateau):
	positions_valides = []
	for col in range(Nombre_Collones):
		if est_libre(plateau, col):
			positions_valides.append(col)
	return positions_valides


def dessiner_plateau(plateau):
	for c in range(Nombre_Collones):
		for r in range( Nombre_Ligne):
			pygame.draw.rect(ecran, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(ecran, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(Nombre_Collones):
		for r in range( Nombre_Ligne):		
			if plateau[r][c] == JOUEUR_PIECE:
				pygame.draw.circle(ecran, RED, (int(c*SQUARESIZE+SQUARESIZE/2), hauteur-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif plateau[r][c] == AI_PIECE: 
				pygame.draw.circle(ecran, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), hauteur-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

Mini_ALphaBeta=0
Mini=0    

for i in range(10):
   
    plateau = crée_plateau()
    pion=42
    game_over = False

    pygame.init()

    SQUARESIZE = 100

    largeur = Nombre_Collones * SQUARESIZE
    hauteur = ( Nombre_Ligne+1) * SQUARESIZE

    size = (largeur, hauteur)

    RADIUS = int(SQUARESIZE/2 - 5)

    ecran = pygame.display.set_mode(size)
    dessiner_plateau(plateau)
    pygame.display.update()

    font = pygame.font.SysFont("monospace", 75)

    tour = random.randint(JOUEUR, AI)
    
    col=random.randint(0,6)
    row=ligne_suivante(plateau,col)
    if tour==JOUEUR:
        poser_piece(plateau,row,col,JOUEUR_PIECE)
        pion-=1
    else:
        poser_piece(plateau,row,col,AI_PIECE)
        pion-=1
    tour += 1
    tour = tour % 2

    while not game_over and pion>0:
        
        if tour == JOUEUR  and not game_over and pion>0:
            col,minimax_score= minimax_alphabeta(plateau, 2, -math.inf, math.inf, True)

            if est_libre(plateau, col):
                row = ligne_suivante(plateau, col)
                poser_piece(plateau, row, col, JOUEUR_PIECE)
                pion-=1
                if coup_gagnant(plateau, JOUEUR_PIECE):
                    label = font.render("JOUEUR 1 wins!!", 1, RED)
                    Mini_ALphaBeta+=1
                    ecran.blit(label, (40,10))

                    game_over = True

                tour += 1
                tour = tour % 2 

                #print_plateau(plateau)
                dessiner_plateau(plateau)

        # # Ask for JOUEUR 2 Input
        if tour == AI and not game_over and pion>0:				
            #col = random.randint(0, Nombre_Collones-1)
            #col = pick_best_move(plateau, AI_PIECE)
            col, minimax_score = minimax(plateau, 2 , True)
            if est_libre(plateau, col):
                #pygame.time.wait(500)
                row = ligne_suivante(plateau, col)
                poser_piece(plateau, row, col, AI_PIECE)
                pion-=1
                if coup_gagnant(plateau, AI_PIECE): 
                    label = font.render("JOUEUR 2 wins!!", 1, YELLOW)
                    Mini+=1
                    ecran.blit(label, (40,10))
                    game_over = True

                #print_plateau(plateau)
                dessiner_plateau(plateau)

                tour += 1
                tour = tour % 2

    if game_over or pion<0:
        game_over=True
        pygame.quit()
print("Alpha Beta a gagné ",Mini_ALphaBeta," fois")
print("Minimax a gagné ",Mini," fois")

