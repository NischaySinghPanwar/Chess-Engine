"""
This class is responsible for storing all the information about the current state of a chess game.
It will also be responsible for determining the valid moves at the current state.
It will also keep a move log.
"""
class GameState():
    def __init__(self):
        # Board is an 8x8 2d list, each element has 2 characters.
        # The first character represents the color of the piece, 'b' or 'w'.
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N', or 'p'.
        # "--" represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
        #                       'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"  # leave the start square empty
        self.board[move.endRow][move.endCol] = move.pieceMoved  # move the piece to the end square
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players


    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure there is a move to undo
            move = self.moveLog.pop()  # get the last move from the move log
            self.board[move.startRow][move.startCol] = move.pieceMoved  # put the piece back to its original square
            self.board[move.endRow][move.endCol] = move.pieceCaptured  # put the captured piece back on the board
            self.whiteToMove = not self.whiteToMove  # switch turns back

    # all moves with checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()  # for now, we will not worry about checks
    

    
    #'''genrating all possible moves for the current player'''
    def getAllPossibleMoves(self):
        moves =[]
        for r in range(len(self.board)): #number of rows 
            for c in range(len(self.board[r])):# number oif coloumns in each row 
                turn = self.board[r][c][0] #this will give me whoes ever turn it is as i stored it in that way in the board matrix.
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1] # this will give me the type of piece which is present at that particular position.
                    if piece == 'p':
                        self.getPawnMoves(r,c,moves)
                    elif piece == 'R':
                        self.getRookMoves(r,c,moves)   
                    elif piece == 'N':
                        self.getKnightMoves(r,c,moves)
                    elif piece == 'B': 
                        self.getBishopMoves(r,c,moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r,c,moves)
                    elif piece == 'K':
                        self.getKingMoves(r,c,moves)
                    
        return moves



    def getPawnMoves(self,r,c,moves):
        pass
    def getRookMoves(self,r,c,moves):
        pass
    def getKnightMoves(self,r,c,moves):
        pass
    def getBishopMoves(self,r,c,moves):
        pass
    def getQueenMoves(self,r,c,moves):
        pass
    def getKingMoves(self,r,c,moves):
        pass
class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def getChessNotation(self):
        # You can make this like real chess notation later
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
        