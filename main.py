#Failas, atsakingas už darbą su vartotojo input'u ir gamestate objekto pavaizdavimą

import pygame
from engine import *
from chessBot import *
from multiprocessing import Process, Queue

#Aprašomos dimensijos ir konstantos, kurios bus naudojamos šachmatų lentoje
WIDTH = HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = HEIGHT
DIMENSION = 8 #Šachmatų lenta yra 8x8 dydžio
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

#Inicijuojamas chess piece images dictionary užkrauti šachmatų figūrų paveikslėlius.
def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    #Naudojant for ciklą, pereinama per kiekvieną figūrą ir užkraunamas jos paveikslėlis, padarius atitinkamo dydžio pagal šachmatų lentos langelio dydį.
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) 

#Funkcija, kuri sukuria langelius šachmatų lentoje
def drawBoard(screen):
    global colors
    colors = [pygame.Color("#FFFFE0"), pygame.Color("#556B2F")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j) % 2)] #Keičiama spalva kas langelį
            pygame.draw.rect(screen, color, pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#Naudojant lentos 2D masyvą iš GameState klasės, pavaizduojamos figūros šachmatų lentoje            
def drawPieces(screen, board):
    for i in range(DIMENSION): 
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#Funkcija, atsakinga už galimų ėjimų pavaizdavimą                
def highlightSquares(screen, gs, validMoves, selectedSquare):
    if selectedSquare != ():
        row, col = selectedSquare
        #Jeigu naudotojas paspaudė ant savo figūros, nuspalvinamas langelis mėlynai
        if gs.board[row][col][0] == ("w" if gs.whiteToMove else "b"):
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(80)
            s.fill(pygame.Color("blue"))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            #Nuspalvinami galimi ėjimai
            s.fill(pygame.Color("yellow"))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

#Funkcija, atsakinga už figūrų judėjimo animaciją
#Naudojant linijinę interpoliaciją, randamos tarpinės koordinatės, kurios bus naudojamos animacijai
#Su kiekvienu frame'u perpiešiama šachmatų lenta su figūromis, kurios juda                    
def animateMove(move, screen, gs, clock):
    global colors
    coordinates = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    fps = 5
    frameCount = (abs(dR) + abs(dC)) * fps #Visi frameai kuriuos reikia atlikti animacijai
    #Kiekvienam frame'ui atliekamas šachmatų lentos pavaizdavimas
    for frame in range(frameCount + 1):
        row, col = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen) #Perpiešiama šachmatų lenta su kiekvienu frameu
        drawPieces(screen, gs.board) #Perpiešiamos figūros
        #Pabaigos langelio spalva
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pygame.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        #Nupiešiamas pabaigos langelis
        pygame.draw.rect(screen, color, endSquare)
        #Jei ėjimas yra ėjimas su priešininko figūros suėmimu, nupiešiamas paveikslėlis, kuris buvo suimtas
        if move.pieceCaptured != "--":
            #Specialios taisyklės en passant ėjimui
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == "b" else move.endRow - 1
                endSquare = pygame.Rect(move.endCol*SQ_SIZE, enPassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #Nupiešiamas judančios figūros paveikslėlis su kiekvienu frame'u
        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        #Atnaujinamas ekranas
        pygame.display.flip()
        clock.tick(60) #FPS

#Funkcija, atsakinga už pabaigos teksto pavaizdavimą, duotą stringą nupiešia pagal parinktą stilių, su šešėliais.
def drawEndText(screen, text):
    font = pygame.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, 0, pygame.Color("Black"))
    #Pozicija, kur bus pavaizduotas tekstas "centre"
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH//2 - textObject.get_width()//2, HEIGHT//2 - textObject.get_height()//2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pygame.Color("Gray")) #Šešėlis
    screen.blit(textObject, textLocation.move(2, 2))    

#Funkcija, atsakinga už ėjimų žurnalo pavaizdavimą
def drawMoveLog(screen, gs, font):
    moveLogRect = pygame.Rect(WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    pygame.draw.rect(screen, pygame.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveText = []
    #Generuojamas žaidimo ėjimų žurnalas
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i + 1])
        moveText.append(moveString)
    
    #Pavaizduojamas žaidimo ėjimų žurnalas    
    movesPerRow = 3
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveText), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveText):
                text += "  " + moveText[i + j]
        textObject = font.render(text, True, pygame.Color("White"))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

#Funkcija, atsakinga už šachmatų lentos pavaizdavimą         
def drawGameState(screen, gs, validMoves, usedSquare, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, usedSquare)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)
    
        
#Main funkcija, atsakinga už vartotojo input'ą ir grafinį pavaizdavimą
def main():
    pygame.init()
    moveLogFont = pygame.font.SysFont("Arial", 14, False, False)
    screen = pygame.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("black"))
    gs = GameState()
    validMoves = gs.getAllValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    #Sekamas paskutinis naudotojo paspaudimas (row, col koordinatės)
    usedSquare = ()
    #Sekama iš kur į kur naudotojas nori atlikti ėjimą
    mouseClicks = []
    gameOver = False
    playerOne = True #Jei žaidžia žmogus, playerOne = True, jei žaidžia kompiuteris, playerOne = False
    playerTwo = False #Jei žaidžia žmogus, playerTwo = True, jei žaidžia kompiuteris, playerTwo = False
    BotThinking = False #Jei botas galvoja, BotThinking = True, jei ne, BotThinking = False
    moveFinder = None #Kintamasis, kuris bus naudojamas kaip procesas, kuris ieškos geriausio ėjimo
    moveUndone = False #Kintamasis, kuris nurodo ar ėjimas buvo atšauktas
    
    while running:
        
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            #Pelės paspaudimų valdymas
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver:
                    #pelės x, y koordinatės 2D grafike
                    location = pygame.mouse.get_pos()
                    #row ir col nustato kuris langelis yra paspaudžiamas, taip žinosime, kuri figūra naudojama
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    #Tikrinam ar naudotojas du kartus spaudžia ant to paties langelio
                    if usedSquare == (row, col) or col >= 8:
                        usedSquare = ()
                        mouseClicks = []
                    else:
                        usedSquare = (row, col)
                        mouseClicks.append(usedSquare)
                    #Jei naudotojas paspaudė du kartus, atliekamas ėjimas
                    if len(mouseClicks) == 2 and humanTurn:
                        move = Move(mouseClicks[0], mouseClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                print(move.getChessNotation())
                                usedSquare = ()
                                mouseClicks = []
                        if not moveMade:
                            mouseClicks = [usedSquare]
            #Klavišų paspaudimų valdymas
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    gs.undo()
                    moveMade = True
                    animate = False
                    gameOver = False
                    if BotThinking:
                        moveFinder.terminate()
                        BotThinking = False
                    moveUndone = True
                    
                    #print(gs.moveLog)
                if e.key == pygame.K_r:
                    gs = GameState()
                    validMoves = gs.getAllValidMoves()
                    moveMade = False
                    animate = False
                    gameOver = False
                    if BotThinking:
                        moveFinder.terminate()
                        BotThinking = False
                    moveUndone = True
                    
        #Boto logika
        if not gameOver and not humanTurn and not moveUndone:
            if not BotThinking:
                BotThinking = True
                returnQueue = Queue() #Perduodami duomenys tarp procesų
                #Pradedamas procesas, kuris ieškos geriausio ėjimo
                moveFinder = Process(target=findBestMove, args=(gs, validMoves, returnQueue))
                moveFinder.start() #Pradedamas procesas
                
            #Tikrinama ar procesas baigė darbą
            if not moveFinder.is_alive():
                BotMove = returnQueue.get()
                if BotMove is None:
                    BotMove = findRandMove(validMoves)
                gs.makeMove(BotMove)
                moveMade = True
                animate = True
                BotThinking = False
                    
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs, clock)
            validMoves = gs.getAllValidMoves()
            moveMade = False
            animate = False
            moveUndone = False
        
        drawGameState(screen, gs, validMoves, usedSquare, moveLogFont) 
        
        if gs.checkMate or gs.staleMate:
            gameOver = True
            text = "Stalemate" if gs.staleMate else "Black wins by checkmate" if gs.whiteToMove else "White wins by checkmate"
            drawEndText(screen, text)
               
        clock.tick(MAX_FPS)
        #Arnaujinta informacija iš buferio perkeliama į ekraną
        pygame.display.flip()


if __name__ == "__main__":
    main()