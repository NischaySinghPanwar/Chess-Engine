"""
This is our driver file for the chess game.
It will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Chess import ChessEngine

WIDTH = HEIGHT = 512  # 400 is another option
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations later on
IMAGES = {}

''' 
Initialize a global dictionary of images. This will be called exactly once in the main.
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: We can access an image by saying 'IMAGES['wp']'

'''
The main driver for our code. This will handle user input and updating the graphics.
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()#very expensive to call it every time.
    moveMade = False  # flag variable for when a move is made

    loadImages()  # only do this once, before the while loop
    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = []  # keep track of player clicks (two tuples: [(6,4), (4,4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # the user clicked the same square twice
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear player clicks
                    print("Deselected square")
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                    print(f"Selected square: {sqSelected}, piece: {gs.board[row][col]}")
                    
                if len(playerClicks) == 2:  # after the 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(f"Attempting move: {move.getChessNotation()}")
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True # we have made a move
                        sqSelected = ()  # reset user clicks
                        playerClicks = []
                        print("Valid move made!")
                    else:
                        # Reset to just the current square selection
                        sqSelected = (row, col)
                        playerClicks = [sqSelected]
                        print("Invalid move! Starting new selection.")

            #Key handler        
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
        # Call drawGameState to render the board and pieces
        if moveMade:
            validMoves = gs.getValidMoves()#very expensive to call it every time.
            moveMade = False
        drawGameState(screen, gs, sqSelected, validMoves)
        
        clock.tick(MAX_FPS)
        p.display.flip()
    
'''
Responsible for all the graphics within a current game state.
'''
def drawGameState(screen, gs, sqSelected, validMoves):
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, gs, sqSelected, validMoves)  # highlight selected square and valid moves
    drawPieces(screen, gs.board)  # draw pieces on top of those squares

'''
Draw the squares on the board. The top left square is always light.
'''
def drawBoard(screen):
    colors = [p.Color("#EEEED2"), p.Color("#769656")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Highlight selected square and show valid moves
'''
def highlightSquares(screen, gs, sqSelected, validMoves):
    if sqSelected != ():
        r, c = sqSelected
        # Highlight selected square with green overlay
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)  # transparency value -> 0 transparent; 255 opaque
        s.fill(p.Color('green'))
        screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
        
        # Draw small circles on all valid move positions for the selected piece
        for move in validMoves:
            if move.startRow == r and move.startCol == c:
                # Calculate center of the destination square
                centerX = move.endCol * SQ_SIZE + SQ_SIZE // 2
                centerY = move.endRow * SQ_SIZE + SQ_SIZE // 2
                # Draw a small circle
                p.draw.circle(screen, p.Color('darkgrey'), (centerX, centerY), 14)

'''
Draw the pieces on the board using the current GameState.board
'''

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()