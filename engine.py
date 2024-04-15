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
        
        self.whiteToMove = True
        self.moveLog = []
    
    #metodas, atsakingas už ėjimų atlikimą
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        
    #Metodas, kuris atšaukia naujausią padarytą ėjimą
    def undo(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    
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
        pass
    def moveKnight(self, i, j, moves):
        pass
    def moveBishop(self, i, j, moves):
        pass
    def moveQueen(self, i, j, moves):
        pass
    def moveKing(self, i, j, moves):
        pass
            
    def moveFunctions(self, i, j, moves):
        piece = self.board[i][j][1]
        if piece == "P":
            self.movePawn(i, j, moves)
        elif piece == "R":
            self.moveRook(i, j, moves)
        elif piece == "N":
            self.moveKnight(i, j, moves)
        elif piece == "B":
            self.moveBishop(i, j, moves)
        elif piece == "Q":
            self.moveQueen(i, j, moves)
        elif piece == "K":
            self.moveKing(i, j, moves)
    
    def getAllValidMoves(self):
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                playerTurn = self.board[i][j][0]
                if (playerTurn == "w" and self.whiteToMove) or (playerTurn == "b" and not self.whiteToMove):
                    self.moveFunctions(i, j, moves)
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
    
    #Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
        
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]