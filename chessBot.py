import random

rating = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}

Queens = [[1, 1, 1, 3, 1, 1, 1, 1],
          [1, 2, 3, 3, 3, 1, 1, 1],
          [1, 4, 3, 3, 3, 4, 2, 1],
          [1, 2, 3, 3, 3, 2, 2, 1],
          [1, 2, 3, 3, 3, 2, 2, 1],
          [1, 4, 3, 3, 3, 4, 2, 1],
          [1, 1, 2, 3, 3, 1, 1, 1],
          [1, 1, 1, 3, 1, 1, 1, 1]]

Rooks = [[4, 3, 4, 4, 4, 4, 3, 4],
         [4, 4, 4, 4, 4, 4, 4, 4],
         [1, 1, 2, 3, 3, 2, 1, 1],
         [1, 2, 3, 4, 4, 3, 2, 1],
         [1, 2, 3, 4, 4, 3, 2, 1],
         [1, 1, 2, 3, 3, 2, 1, 1],
         [4, 4, 4, 4, 4, 4, 4, 4],
         [4, 3, 4, 4, 4, 4, 3, 4]]

Bishops = [[4, 3, 2, 1, 1, 2, 3, 4],
           [3, 4, 3, 2, 2, 3, 4, 3],
           [2, 3, 4, 3, 3, 4, 3, 2],
           [1, 2, 3, 4, 4, 3, 2, 1],
           [1, 2, 3, 4, 4, 3, 2, 1],
           [2, 3, 4, 3, 3, 4, 3, 2],
           [3, 4, 3, 2, 2, 3, 4, 3],
           [4, 3, 2, 1, 1, 2, 3, 4]]

Knights = [[1, 1, 1, 1, 1, 1, 1, 1],
           [1, 2, 2, 2, 2, 2, 2, 1],
           [1, 2, 3, 3, 3, 3, 2, 1],
           [1, 2, 3, 4, 4, 3, 2, 1],
           [1, 2, 3, 4, 4, 3, 2, 1],
           [1, 2, 3, 3, 3, 3, 2, 1],
           [1, 2, 2, 2, 2, 2, 2, 1],
           [1, 1, 1, 1, 1, 1, 1, 1]]

whitePawns = [[8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [5, 6, 6, 7, 7, 6, 6, 5],
              [2, 3, 3, 5, 5, 3, 3, 2],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 1, 1, 0, 0, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawns = [[0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 0, 0, 1, 1, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [2, 3, 3, 5, 5, 3, 3, 2],
              [5, 6, 6, 7, 7, 6, 6, 5],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8]]


pieceScores = {"Q": Queens, "R": Rooks, "B": Bishops, "N": Knights, "wP": whitePawns, "bP": blackPawns}

checkMate = 1000
staleMate = 0
DEPTH = 1

def findRandMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -checkMate
        else:
            return checkMate
    elif gs.staleMate:
        return staleMate

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--": #and square[1] in pieceScores:
                pieceScore = 0
                if square[1] != "K":
                    if square[1] == "P":
                        pieceScore = pieceScores[square][row][col]
                    else:
                        pieceScore = pieceScores[square[1]][row][col]
                if square[0] == 'w':
                    score += rating[square[1]] + pieceScore * 0.1
                elif square[0] == 'b':
                    score -= rating[square[1]] + pieceScore * 0.1

    return score

def findBestMove(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    #random.shuffle(validMoves)
    counter = 0
    findMoveMinMaxAlphaBeta(gs, validMoves, DEPTH, -checkMate, checkMate, 1 if gs.whiteToMove else -1)
    print(counter)
    returnQueue.put(nextMove)

def findMoveMinMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -checkMate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllValidMoves()
        score = -findMoveMinMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undo()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore