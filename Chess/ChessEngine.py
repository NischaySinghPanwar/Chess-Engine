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
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pin = []
        self.checks = []


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"  # leave the start square empty
        self.board[move.endRow][move.endCol] = move.pieceMoved  # move the piece to the end square
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players
        # update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)


    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure there is a move to undo
            move = self.moveLog.pop()  # get the last move from the move log
            self.board[move.startRow][move.startCol] = move.pieceMoved  # put the piece back to its original square
            self.board[move.endRow][move.endCol] = move.pieceCaptured  # put the captured piece back on the board
            self.whiteToMove = not self.whiteToMove  # switch turns back

    # all moves with checks
    def getValidMoves(self):
        moves =[]
        self.inCheck, self.pin, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) ==1: #only 1 check, block or move king
                moves = self.getAllPossibleMoves()
                #to block check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0] #check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = [] #squares that pieces can move to
                #if knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow,checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i) #check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                #get rid of any moves that don't block check or move king
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[1] != 'K': #move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: #double check, king has to move
                self.getKingMoves(kingRow,kingCol,moves)
        else:
            moves = self.getAllPossibleMoves()
        return moves
        
    

    
    '''genrating all possible moves for the current player'''
    def getAllPossibleMoves(self):
        moves =[]
        for r in range(len(self.board)): #number of rows 
            for c in range(len(self.board[r])):# number oif coloumns in each row 
                turn = self.board[r][c][0] #this will give me whoes ever turn it is as i stored it in that way in the board matrix.
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1] # this will give me the type of piece which is present at that particular position.
                    self.moveFunctions[piece](r,c,moves) #calls the appropriate move function based on piece type
        return moves

    def checkForPinsAndChecks(self):
        pins =[]
        checks =[]
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        #check outward from king for pins and checks, keep track of pins
        directions = ((-1,0),(1,0),(0,-1),(0,1),(1,1),(1,-1),(-1,1),(-1,-1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () #reset possible pins
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    endPiece = self.board[endRow][endCol]
                    # empty square -> keep scanning
                    if endPiece == "--":
                        continue
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == (): #1st allied piece could be pinned
                            possiblePin = (endRow,endCol,d[0],d[1])
                        else: #2nd allied piece, no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        #5 possibilities in this conditional
                        #1.) orthogonally away from king and piece is rook
                        #2.) diagonally away from king and piece is bishop
                        #3.) 1 square away diagonally from king and piece is pawn
                        #4.) any direction and piece is queen
                        #5.) any direction 1 square away and piece is king (this is to prevent king to king moves)
                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or \
                           (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <=5))) or  \
                           (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): #no piece blocking, so check
                                inCheck = True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break
                            else: #piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else: #off board
                    break
        #check for knight checks
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow,endCol,m[0],m[1]))
        return inCheck, pins, checks


    def getPawnMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range (len(self.pin)-1,-1,-1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                piecePinned = True
                pinDirection = (self.pin[i][2],self.pin[i][3])
                self.pin.remove(self.pin[i])
                break
        if self.whiteToMove:
            if self.board[r-1][c] == "--": #1 square move
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r == 6 and self.board[r-2][c] == "--": #2 square move
                        moves.append(Move((r,c),(r-2,c),self.board))
            # Capture moves
            if c-1>=0 and r-1 >= 0:
                # capture to the left
                dr, dc = -1, -1
                if self.board[r-1][c-1][0] == 'b':
                    # allow capture only if not pinned or capture is along pin direction
                    if not piecePinned or pinDirection == (dr, dc) or pinDirection == (-dr, -dc):
                        moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1<=7 and r-1 >= 0:
                # capture to the right
                dr, dc = -1, 1
                if self.board[r-1][c+1][0] == 'b':
                    if not piecePinned or pinDirection == (dr, dc) or pinDirection == (-dr, -dc):
                        moves.append(Move((r,c),(r-1,c+1),self.board))
        else: #black pawn moves
            if self.board[r+1][c] == "--": #1 square move
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--": #2 square move
                    moves.append(Move((r,c),(r+2,c),self.board))
            # Capture moves
            if c-1>=0 and r+1 <= 7:
                if self.board[r+1][c-1][0] == 'w': #capture white piece to the left
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1<=7 and r+1 <= 7:
                if self.board[r+1][c+1][0] == 'w': #capture white piece to the right
                    moves.append(Move((r,c),(r+1,c+1),self.board))
 #all possible move of Bishop
    def getBishopMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range (len(self.pin)-1,-1,-1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                piecePinned = True
                pinDirection = (self.pin[i][2],self.pin[i][3])
                self.pin.remove(self.pin[i])
                break
        directions = ((-1,-1),(-1,1),(1,-1),(1,1)) #up left , up right , down left , down right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            # if this piece is pinned, only allow moves along the pin direction (or opposite)
            if piecePinned and not (d[0] == pinDirection[0] and d[1] == pinDirection[1]) and not (d[0] == -pinDirection[0] and d[1] == -pinDirection[1]):
                continue
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break 
    #all possible move of Rook
    def getRookMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range (len(self.pin)-1,-1,-1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                piecePinned = True
                pinDirection = (self.pin[i][2],self.pin[i][3])
                self.pin.remove(self.pin[i])
                break
        directions = ((-1,0),(0,-1),(1,0),(0,1)) #up , left , down , right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            # if pinned, only allow moves along the pin direction (or opposite)
            if piecePinned and not (d[0] == pinDirection[0] and d[1] == pinDirection[1]) and not (d[0] == -pinDirection[0] and d[1] == -pinDirection[1]):
                continue
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break
        
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    #all possible move of King
    def getKingMoves(self,r,c,moves):
            directions = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
            allyColor = "w" if self.whiteToMove else "b"
            enemyColor = "b" if self.whiteToMove else "w"
            for i in range(8):
                endRow = r+directions[i][0]
                endCol = c+directions[i][1]
                if 0<= endRow <8 and 0<= endCol<8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        # Check if the square is attacked
                        if not self.squareUnderAttack(endRow, endCol, enemyColor):
                            moves.append(Move((r,c),(endRow,endCol),self.board))

        # Class-level method
    def squareUnderAttack(self, row, col, enemyColor):
            # Check if a square is attacked by any enemy piece
            # This is a simplified version, you may want to optimize
            directions = ((-1,0),(1,0),(0,-1),(0,1),(1,1),(1,-1),(-1,1),(-1,-1))
            for d in directions:
                for i in range(1,8):
                    endRow = row + d[0]*i
                    endCol = col + d[1]*i
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece[0] == enemyColor:
                            type = endPiece[1]
                            if (0 <= directions.index(d) <= 3 and type == 'R') or \
                               (4 <= directions.index(d) <= 7 and type == 'B') or \
                               (type == 'Q'):
                                return True
                            break
                        elif endPiece != "--":
                            break
                    else:
                        break
            # Check for knight attacks
            knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
            for m in knightMoves:
                endRow = row + m[0]
                endCol = col + m[1]
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == enemyColor and endPiece[1] == 'N':
                        return True
            # Check for pawn attacks
            if enemyColor == 'b':
                pawnMoves = ((1,-1),(1,1))
            else:
                pawnMoves = ((-1,-1),(-1,1))
            for m in pawnMoves:
                endRow = row + m[0]
                endCol = col + m[1]
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == enemyColor and endPiece[1] == 'p':
                        return True
            return False
#all possible move of Knight
    def getKnightMoves(self,r,c,moves):  # Fixed typo: maoves -> moves
        # Knights cannot move if pinned
        piecePinned = False
        for i in range(len(self.pin)-1, -1, -1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                piecePinned = True
                # remove this pin so other functions don't see it twice
                self.pin.remove(self.pin[i])
                break
        if piecePinned:
            return
        directions = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)) #8 possible moves for a knight
        allyColor="w" if self.whiteToMove else "b"
        for m in directions:
            endRow = r+m[0]
            endCol = c+m[1]
            if 0<= endRow <8  and 0<=endCol<8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Can move to empty squares or capture enemy pieces
                    moves.append(Move((r,c),(endRow,endCol),self.board))

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
        print(self.moveID)


    #overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation(self):
        # You can make this like real chess notation later
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
        