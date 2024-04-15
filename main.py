#Failas, atsakingas už darbą su vartotojo input'u ir gamestate objekto pavaizdavimą

import pygame
from engine import *

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

#Funkcija, atsakinga už šachmatų lentos pavaizdavimą         
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)
        
#Main funkcija, atsakinga už vartotojo input'ą ir grafinį pavaizdavimą
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("black"))
    gs = GameState()
    validMoves = gs.getAllValidMoves()
    moveMade = False
    loadImages()
    running = True
    #Sekamas paskutinis naudotojo paspaudimas (row, col koordinatės)
    usedSquare = ()
    #Sekama iš kur į kur naudotojas nori atlikti ėjimą
    mouseClicks = []
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            #Pelės paspaudimų valdymas
            elif e.type == pygame.MOUSEBUTTONDOWN:
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
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    print(move.getChessNotation())
                    usedSquare = ()
                    mouseClicks = []
            #Klavišų paspaudimų valdymas
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    gs.undo()
                    moveMade = True
                    print(gs.moveLog)
                    
        if moveMade:
            validMoves = gs.getAllValidMoves()
            moveMade = False
        
        drawGameState(screen, gs)        
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()