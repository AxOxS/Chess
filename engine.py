#Failas, atsakingas už šachmatų partijos informacijos saugojimą ir manipuliavimą. Tuo pačiu atsakingas už leistinų ėjimų tikrinimą ir senų ėjimų saugojimą.

class GameState():
    def __init__(self):
        #Šachmatų lentos atvaizdavimas, naudojant du dimensinius masyvus. Kiekvienas elementas masyvuose atstoja šachmatų figūrą
        #arba tuščią langelį. kiekviena figūra pavaizduojama dviem simboliais, pirmas simbolis nurodo spalvą, o antras figūros tipą.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        
        self.moveFunctions = {"P": self.movePawn, "R": self.moveRook, "N": self.moveKnight, "B": self.moveBishop, "Q": self.moveQueen, "K": self.moveKing}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKing = (7, 4)
        self.blackKing = (0, 4)
        self.checkMate = False
        self.staleMate = False

    
    #metodas, atsakingas už ėjimų atlikimą
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKing = (move.endRow, move.endCol)
        if move.pieceMoved == "bK":
            self.blackKing = (move.endRow, move.endCol)
            
        #Pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"
        
    #Metodas, kuris atšaukia naujausią padarytą ėjimą
    def undo(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKing = (move.startRow, move.startCol)
            if move.pieceMoved == "bK":
                self.blackKing = (move.startRow, move.startCol)
    
    def movePawn(self, i, j, moves):
        if self.whiteToMove:  # White pawn moves
            if self.board[i-1][j] == "--":  # Move one square forward
                moves.append(Move((i, j), (i-1, j), self.board))
            if i == 6 and self.board[i-2][j] == "--":  # Move two squares forward from starting position
                moves.append(Move((i, j), (i-2, j), self.board))
            if j-1 >= 0 and self.board[i-1][j-1][0] == "b":  # Capture to the left
                moves.append(Move((i, j), (i-1, j-1), self.board))
            if j+1 <= 7 and self.board[i-1][j+1][0] == "b":  # Capture to the right
                moves.append(Move((i, j), (i-1, j+1), self.board))
        else:  # Black pawn moves
            if self.board[i+1][j] == "--":  # Move one square forward
                moves.append(Move((i, j), (i+1, j), self.board))
            if i == 1 and self.board[i+2][j] == "--":  # Move two squares forward from starting position
                moves.append(Move((i, j), (i+2, j), self.board))
            if j-1 >= 0 and self.board[i+1][j-1][0] == "w":  # Capture to the left 
                moves.append(Move((i, j), (i+1, j-1), self.board))
            if j+1 <= 7 and self.board[i+1][j+1][0] == "w":  # Capture to the right
                moves.append(Move((i, j), (i+1, j+1), self.board))
                
    def moveRook(self, i, j, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for step in range(1, 8):
                endRow = i + d[0]*step
                endCol = j + d[1]*step
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((i, j), (endRow, endCol), self.board))
                    elif endPiece[0] != self.board[i][j][0]:
                        moves.append(Move((i, j), (endRow, endCol), self.board))
                        break
                    else:
                        break
        
    def moveKnight(self, i, j, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = i + m[0]
            endCol = j + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != self.board[i][j][0]:
                    moves.append(Move((i, j), (endRow, endCol), self.board))
        
    def moveBishop(self, i, j, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            for step in range(1, 8):
                endRow = i + d[0]*step
                endCol = j + d[1]*step
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((i, j), (endRow, endCol), self.board))
                    elif endPiece[0] != self.board[i][j][0]:
                        moves.append(Move((i, j), (endRow, endCol), self.board))
                        break
                    else:
                        break
    
    def moveQueen(self, i, j, moves):
        self.moveRook(i, j, moves)
        self.moveBishop(i, j, moves)

    def moveKing(self, i, j, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for d in directions:
            endRow = i + d[0]
            endCol = j + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != self.board[i][j][0]:
                    moves.append(Move((i, j), (endRow, endCol), self.board))
            
    # def moveFunctions(self, i, j, moves):
    #     piece = self.board[i][j][1]
    #     if piece == "P":
    #         self.movePawn(i, j, moves)
    #     elif piece == "R":
    #         self.moveRook(i, j, moves)
    #     elif piece == "N":
    #         self.moveKnight(i, j, moves)
    #     elif piece == "B":
    #         self.moveBishop(i, j, moves)
    #     elif piece == "Q":
    #         self.moveQueen(i, j, moves)
    #     elif piece == "K":
    #         self.moveKing(i, j, moves)
    
    def squareUnderAttack(self, i, j):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == i and move.endCol == j:
                return True
        return False
    
    def inCheck(self):
        kingRow, kingCol = self.whiteKing if self.whiteToMove else self.blackKing
        
        return self.squareUnderAttack(kingRow, kingCol)
     
    def getAllValidMoves(self):
        moves = self.getAllPossibleMoves()
        validMoves = []
        for move in moves:
            self.makeMove(move)
            self.whiteToMove = not self.whiteToMove
            if not self.inCheck():
                validMoves.append(move)
            self.whiteToMove = not self.whiteToMove
            self.undo()
            
        if len(validMoves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
                
        return validMoves
    
    def getAllPossibleMoves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                playerTurn = self.board[i][j][0]
                if (playerTurn == "w" and self.whiteToMove) or (playerTurn == "b" and not self.whiteToMove):
                    # self.moveFunctions(i, j, moves)
                    piece = self.board[i][j][1]
                    self.moveFunctions[piece](i, j, moves)
        return moves

class Move():
    #Ši klasė atsakinga už ėjimų saugojimą ir tikrinimą
    #Ši klasė saugo informaciją apie ėjimą, ėjimo koordinates ir figūrą, kurią ėjimas atliekamas
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        self.isPawnPromotion = False
        if (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7):
            self.isPawnPromotion = True
    
    #Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
        
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]