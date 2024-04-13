#Failas, atsakingas už darbą su vartotojo input'u ir gamestate objekto pavaizdavimą

import pygame
from engine import GameState

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
    loadImages()
    running = True
    
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        drawGameState(screen, gs)        
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()