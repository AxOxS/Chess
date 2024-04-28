import random


rating = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
checkMate = 1000
staleMate = 0


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
    turnMultiplier = 1 if gs.whiteToMove else -1
    oppMinMax = checkMate
    bestMove = None
    
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getAllValidMoves()
        random.shuffle(validMoves)
        oppMax = -checkMate
        for opponentMove in opponentMoves:
            gs.makeMove(opponentMove)
            if gs.checkMate:
                score = -turnMultiplier * checkMate
            elif gs.staleMate:
                score = staleMate
            else:
                score = -turnMultiplier * scoreBoard(gs)
            
            if score > oppMax:
                oppMax = score
            gs.undo()
        if oppMax < oppMinMax:
            oppMinMax = oppMax
            bestMove = playerMove
        gs.undo()
    return bestMove

# def findBestMove(gs, validMoves):
#     bestScore = float('-inf') if gs.whiteToMove else float('inf')
#     bestMove = None

#     for playerMove in validMoves:
#         gs.makeMove(playerMove)
#         opponentMoves = gs.getAllValidMoves()

#         if gs.checkMate:
#             score = -1000 if gs.whiteToMove else 1000
#         elif gs.staleMate:
#             score = 0
#         else:
#             _, score = findBestMove(gs, opponentMoves)
#             score = -score

#         gs.undo()

#         if gs.whiteToMove:
#             if score > bestScore:
#                 bestScore = score
#                 bestMove = playerMove
#         else:
#             if score < bestScore:
#                 bestScore = score
#                 bestMove = playerMove

#     return bestMove, bestScore