#Failas, atsakingas už darbą su vartotojo input'u ir gamestate objekto pavaizdavimą

import pygame
from engine import *
from chessBot import *

pygame.init()
WIDTH = HEIGHT = 512
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
            color = colors[((i+j) % 2)]
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
        if gs.board[row][col][0] == ("w" if gs.whiteToMove else "b"):
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(80)
            s.fill(pygame.Color("blue"))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            s.fill(pygame.Color("yellow"))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

#Funkcija, atsakinga už figūrų judėjimo animaciją                    
def animateMove(move, screen, gs, clock):
    global colors
    coordinates = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    fps = 5
    frameCount = (abs(dR) + abs(dC)) * fps
    for frame in range(frameCount + 1):
        row, col = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, gs.board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pygame.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = pygame.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, 0, pygame.Color("Black"))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH//2 - textObject.get_width()//2, HEIGHT//2 - textObject.get_height()//2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pygame.Color("Gray"))
    screen.blit(textObject, textLocation.move(2, 2))    

#Funkcija, atsakinga už šachmatų lentos pavaizdavimą         
def drawGameState(screen, gs, validMoves, usedSquare):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, usedSquare)
    drawPieces(screen, gs.board)
    
        
#Main funkcija, atsakinga už vartotojo input'ą ir grafinį pavaizdavimą
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    playerOne = False #Jei žaidžia žmogus, playerOne = True, jei žaidžia kompiuteris, playerOne = False
    playerTwo = False #Jei žaidžia žmogus, playerTwo = True, jei žaidžia kompiuteris, playerTwo = False
    
    while running:
        
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            #Pelės paspaudimų valdymas
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    #pelės x, y koordinatės 2D grafike
                    location = pygame.mouse.get_pos()
                    #row ir col nustato kuris langelis yra paspaudžiamas, taip žinosime, kuri figūra naudojama
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    #Tikrinam ar naudotojas du kartus spaudžia ant to paties langelio
                    if usedSquare == (row, col):
                        usedSquare = ()
                        mouseClicks = []
                    else:
                        usedSquare = (row, col)
                        mouseClicks.append(usedSquare)
                    #Jei naudotojas paspaudė du kartus, atliekamas ėjimas
                    if len(mouseClicks) == 2:
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
                    print(gs.moveLog)
                if e.key == pygame.K_r:
                    gs = GameState()
                    validMoves = gs.getAllValidMoves()
                    moveMade = False
                    animate = False
                    gameOver = False
                    
        #Boto logika
        if not gameOver and not humanTurn:
            BotMove = findBestMove(gs, validMoves)
            #BotMove = findRandMove(validMoves)
            if BotMove is None:
                BotMove = findRandMove(validMoves)
            gs.makeMove(BotMove)
            moveMade = True
            animate = True
                    
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs, clock)
            validMoves = gs.getAllValidMoves()
            moveMade = False
            animate = False
        
        drawGameState(screen, gs, validMoves, usedSquare) 
        
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")
               
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()