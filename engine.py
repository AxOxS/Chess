#GameState klasė, atsakinga už žaidimo būsenos saugojimą ir ėjimų atlikimą. Inicilizuoja startinę žaidimo būseną ir saugo visus ėjimus, kontroliuoja žaidėjų eiles,
#checkmate ir stalemate atvejus
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
        #Dictionary, kuriame prie kiekvienos figūros priskiriamas jos ėjimo metodas
        self.moveFunctions = {"P": self.movePawn, "R": self.moveRook, "N": self.moveKnight, "B": self.moveBishop, "Q": self.moveQueen, "K": self.moveKing}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKing = (7, 4)
        self.blackKing = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        #Castle rights, kuris saugo informaciją, kada galima castlinti ir į kurias puses
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    
    #metodas, atsakingas už ėjimų atlikimą
    def makeMove(self, move):
        #Atnaujinama lenta, atlikus ėjimą. Judanti figūra pašalinama iš pradinės pozicijos ir įdedama į naują poziciją. ėjimas pridedamas į movelog
        #Ir po ėjimo pakeičiama žaidėjo eilė
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        #Atnaujinami karaliaus koordinatės, jeigu tai buvo judanti figūra
        if move.pieceMoved == "wK":
            self.whiteKing = (move.endRow, move.endCol)
        if move.pieceMoved == "bK":
            self.blackKing = (move.endRow, move.endCol)
            
        #Pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"
            
        #En passant. Kur buvo paimtas pawn - pakeičiama į tuščią langelį
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"
        
        #Patikrinam ar galima daryti en passant ėjimą. Atkreipiam dėmesį į tai ar tai pawn ėjimas ir ar jis judėjo 2 langelius
        if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
            #Apskaičiuojamos langelio, kur bus galimas en passant ėjimas koordinatės. Langelis turi būti tame pačiame stulpelyje, kaip atakuojantis pawn ir
            #ir eilutėje už puolamo pawn
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()
        
        #Castle move
        if move.isCastleMove:
            #Tikrinam ar kingside castling
            if move.endCol - move.startCol == 2:
                #Rook pozicija perkeliama į naują poziciją ir sena pozicija pakeičiama į tuščią langelį
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            #Queenside castling
            else:
                #Rook pozicija perkeliama į naują poziciją ir sena pozicija pakeičiama į tuščią langelį
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"
        
        #Castle rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        
        
    #Metodas, kuris atšaukia naujausią padarytą ėjimą
    def undo(self):
        #Patikrinama ar yra ėjimų, kuriuos galima atšaukti, jeigu taip, su pop ištraukiamas paskutinis ėjimas iš movelog ir reversinamas šachmatų lentoje.
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            #Pakeičiama žaidėjo eilė
            self.whiteToMove = not self.whiteToMove
            #Atnaujinamos karaliaus koordinatės, jeigu tai buvo judanti figūra
            if move.pieceMoved == "wK":
                self.whiteKing = (move.startRow, move.startCol)
            if move.pieceMoved == "bK":
                self.blackKing = (move.startRow, move.startCol)
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
                
            #Castle rights undo
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            
            #Castle move undo
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"
            
            #Jeigu buvo True - pakeičiam į False.
            self.checkMate = False
            self.staleMate = False
    
    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved in ["wR", "bR"]:
            #Jei rook iš Karalienės pusės
            if move.startCol == 0:
                #Jei rook baltas
                if move.pieceMoved == "wR" and move.startRow == 7:
                    self.currentCastlingRight.wqs = False
                #Jei rook juodas
                elif move.pieceMoved == "bR" and move.startRow == 0:
                    self.currentCastlingRight.bqs = False
            #Jei rook iš Karaliaus pusės
            elif move.startCol == 7:
                #Jei rook baltas
                if move.pieceMoved == "wR" and move.startRow == 7:
                    self.currentCastlingRight.wks = False
                #Jei rook juodas
                elif move.pieceMoved == "bR" and move.startRow == 0:
                    self.currentCastlingRight.bks = False
        
        #Jeigu rook buvo paimtas - tikrinam, kurio žaidėjo rook ir ar jis buvo paimtas iš saco pradinės pozicijos. Jeigu taip - pakeičiam castling rights
        if move.pieceCaptured == "wR":
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == "bR":
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False

    #Metodas, kuris atsakingas už pawn judėjimo logiką
    def movePawn(self, i, j, moves):
        #Pagal žaidėjo spalvą nustatoma, judėjimo kryptis, pradinė koordinatė ir priešininko spalva
        direction = -1 if self.whiteToMove else 1
        start_row = 6 if self.whiteToMove else 1
        opponent_color = "b" if self.whiteToMove else "w"
        
        #Ėjimas vienu langeliu į priekį, jeigu langelis prieš figūrą yra tuščias
        if self.board[i + direction][j] == "--":
            moves.append(Move((i, j), (i + direction, j), self.board))
            #Jeigu pawn dar nejudėjo ir 2x langeliai prieš pawn tušti - galima judėti 2 langeliais
            if i == start_row and self.board[i + 2*direction][j] == "--":
                moves.append(Move((i, j), (i + 2*direction, j), self.board))
        
        #Jeigu iš kairės prieš pawn yra pirešininko figūra - galima atakuoti
        if j-1 >= 0 and self.board[i + direction][j - 1][0] == opponent_color:
            moves.append(Move((i, j), (i + direction, j - 1), self.board))
        
        ##Jeigu iš dešinės prieš pawn yra pirešininko figūra - galima atakuoti
        if j+1 <= 7 and self.board[i + direction][j + 1][0] == opponent_color:
            moves.append(Move((i, j), (i + direction, j + 1), self.board))
        
        #Patikrinam ar galima atlikti en passant ėjimą, jeigu priešais pawn yra pirešininko pawn, kuri judėjo 2 langeliais - galima atakuoti
        if i == 3 if self.whiteToMove else 4:
            #Kairėje (j-1 >= 0, prevencinė priemonė, kad netikrintų langelio, kurio nėra)
            if j-1 >= 0 and self.board[i][j - 1] == opponent_color + "P" and self.board[i + direction][j - 1] == "--" and self.board[i + 2*direction][j - 1] == "--":
                moves.append(Move((i, j), (i + direction, j - 1), self.board, enpassantPossible=True))
            #Dešinėje
            if j+1 <= 7 and self.board[i][j + 1] == opponent_color + "P" and self.board[i + direction][j + 1] == "--" and self.board[i + 2*direction][j + 1] == "--":
                moves.append(Move((i, j), (i + direction, j + 1), self.board, enpassantPossible=True))

                
    def moveRook(self, i, j, moves):
        #Kryptys, kuriomis gali judėti rook
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        #Ciklas cikle per visas kryptis ir visus galimus langelius (8*8)
        for d in directions:
            for step in range(1, 8):
                #Apskaičiuojamos koordinatės lentoje, kiekvienam galimam rook ėjimui
                endRow = i + d[0]*step
                endCol = j + d[1]*step
                #Patikrinama ar langelis yra lentos ribose
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    #Jeigu norimas užimti langelis tuščias - galima judėti, jeigu priešininko figūra - galima atakuoti, jeigu savo figūra - negalima judėti
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
    
    #Karalienė gali judėti kaip rook ir bishop viename, todėl nereikia, kurti naujo metodo
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
    
    #Metodas, kuris atsakingas už castle moves
    def getCastleMoves(self, i, j, moves):
        #Tikrinama ar langelis, kuriame yra karalius yra atakuojamas, jeigu taip - negalima castlinti (Gal nereikia)
        # if self.squareUnderAttack(i, j):
        #     return
        #Tikrinama ar galima castlinti į kairę ir į dešinę
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(i, j, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(i, j, moves)
    
    #Metodas, kuris atsakingas už kingside castling. Tikrinam ar langeliai tarp karaliaus ir rook yra tušti ir ar langeliai nėra atakuojami        
    def getKingSideCastleMoves(self, i, j, moves):
        if self.board[i][j+1] == "--" and self.board[i][j+2] == "--":
            if not self.squareUnderAttack(i, j+1) and not self.squareUnderAttack(i, j+2):
                moves.append(Move((i, j), (i, j+2), self.board, castleMove=True))
    
    #Metodas, kuris atsakingas už queenside castling. Tikrinam ar langeliai tarp karaliaus ir rook yra tušti ir ar langeliai nėra atakuojami
    def getQueenSideCastleMoves(self, i, j, moves):
        if self.board[i][j-1] == "--" and self.board[i][j-2] == "--" and self.board[i][j-3] == "--":
            if not self.squareUnderAttack(i, j-1) and not self.squareUnderAttack(i, j-2):
                moves.append(Move((i, j), (i, j-2), self.board, castleMove=True))

    #Metodas, kuris tikrina ar tam tikras langelis yra atakuojamas priešo figūrų
    def squareUnderAttack(self, i, j):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == i and move.endCol == j:
                return True
        return False
    
    #Metodas, kuris tikrina ar žaidėjo karalius yra atakuojamas
    def inCheck(self):
        kingRow, kingCol = self.whiteKing if self.whiteToMove else self.blackKing
        
        return self.squareUnderAttack(kingRow, kingCol)
    
    #Metodas, kuris grąžina visus galimus ėjimus, kurie yra validūs. 
    def getAllValidMoves(self):
        # for log in self.castleRightsLog:
        #     print(log.wks, log.bks, log.wqs, log.bqs, end=", ")
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        
        moves = self.getAllPossibleMoves()
        
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKing[0], self.whiteKing[1], moves)
        else:
            self.getCastleMoves(self.blackKing[0], self.blackKing[1], moves)
        
        validMoves = []
        #Patikrinam ar po ėjimo karalius nebus atakuojamas. Jeigu bus - ėjimas nevalidus
        for move in moves:
            self.makeMove(move)
            self.whiteToMove = not self.whiteToMove
            if not self.inCheck():
                validMoves.append(move)
            self.whiteToMove = not self.whiteToMove
            self.undo()
        
        #Jeigu nėra galimų ėjimų ir karalius yra atakuojamas - checkmate, jeigu nėra galimų ėjimų ir karalius nėra atakuojamas - stalemate  
        if len(validMoves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        
        #Grąžinamos originalios enpassant ir castle rights reikšmės
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return validMoves
    
    #Metodas, kuris grąžina visus galimus ėjimus. Naudojant ciklą cikle pereinam per visus lentos langelius ir tikrinam ar figūra priklauso žaidėjui ir ar to žaidėjo eilė.
    #Jei taip, kviečiamas atitinkamas figūros ėjimo metodas. Tai padaroma su visomis figūromis
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
    #Ši klasė saugo informaciją apie ėjimą, ėjimo koordinates ir figūrą, kuria ėjimas atliekamas
    
    #Mappinam lentos koordinates į pitono koordinates
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {value: key for key, value in ranksToRows.items()} #Apverčiamos key value poros į value key poras
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {value: key for key, value in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board, enpassantPossible = False, castleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #Kiekvienas ėjimas turi savo unikalų ID, kuris yra sudarytas iš 4 skaičių. Pirmi du skaičiai nurodo pradinę koordinatę, o kiti du - galutinę koordinatę
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        self.isPawnPromotion = (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7)
        self.isEnpassantMove = enpassantPossible
        if self.isEnpassantMove:
            self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"
        self.isCastleMove = castleMove
    
    #Overriding the equals method. Tikrinam ar other yra Move objektas ir ar jie turi vienodus moveID, jeigu ne - grąžinama False.
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    #Metodas, kuris grąžina ėjimo notaciją. Notacija yra sudaryta iš pradinės ir galutinės koordinatės (naudojama tik konsolėje)    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
    
    #Overriding the string method. Naudosim pavaizduoti tikrai chess notacijai
    def __str__(self):
        #Castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
        endSquare = self.getRankFile(self.endRow, self.endCol)
        #Pawn moves
        if self.pieceMoved[1] == "P":
            if self.pieceCaptured != "--":
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
            
        #Other pieces
        moveString = self.pieceMoved[1]
        if self.pieceCaptured != "--":
            moveString += "x"
        return moveString + endSquare

#Klasė, kuri saugo informaciją apie castle rights. Kiekvienas objektas saugo informaciją apie tai, ar galima castlinti į kairę ar į dešinę 
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
    