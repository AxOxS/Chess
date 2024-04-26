import random


def findRandMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

# def findBestMove(gs, validMoves):
#     turnMultiplier = 1 if gs.whiteToMove else -1
#     opponentMinMaxScore = float('inf') if gs.whiteToMove else float('-inf')
#     bestPlayerMove = None
#     for playerMove in validMoves:
#         gs.makeMove(playerMove)
#         opponentMoves = gs.getAllValidMoves()
#         if gs.checkMate:
#             score = -turnMultiplier * 1000
#         elif gs.staleMate:
#             score = 0
#         else:
#             score = -turnMultiplier * findBestMove(gs, opponentMoves)[1]
#         if gs.whiteToMove and score < opponentMinMaxScore:
#             opponentMinMaxScore = score
#             bestPlayerMove = playerMove
#         elif not gs.whiteToMove and score > opponentMinMaxScore:
#             opponentMinMaxScore = score
#             bestPlayerMove = playerMove
#         gs.undo()
#     return bestPlayerMove, opponentMinMaxScore