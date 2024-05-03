import random


rating = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
checkMate = 1000
staleMate = 0
DEPTH = 3

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
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += rating[square[1]]
            elif square[0] == 'b':
                score -= rating[square[1]]

    return score

def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -checkMate, checkMate, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -checkMate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
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