import random
import time


pieceScore = {"K": 0, "Q": 90, "R": 50, "B": 35, "N": 30, "p": 10}

knightScore =  [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScore =  [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScore =   [[1, 1, 1, 3, 1, 1, 1, 1],
                [1, 2, 3, 3, 3, 1, 1, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 2, 3, 3, 3, 1, 1, 1],
                [1, 1, 1, 3, 1, 1, 1, 1]]

rookScore =    [[4, 3, 4, 4, 4, 4, 3, 4],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScore =   [[8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [1, 2, 3, 3, 3, 3, 2, 1],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScore =   [[0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [1, 2, 3, 3, 3, 3, 2, 1],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8]]

piecePosScores =  {'N': knightScore, 'B': bishopScore, 'Q': queenScore, 'R': rookScore, "wp": whitePawnScore, "bp": blackPawnScore}


CHECKMATE = 100000
STALEMATE = 0
MAX_DEPTH = 4

''' Find random move for AI '''
def findRandomMove(validMoves):
    if len(validMoves) > 0:
        return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMoveMinimax(gs, validMoves):
    global nextMove
    global nodes
    nextMove = None
    alpha = -CHECKMATE
    beta = CHECKMATE
    nodes = 0
    start_time = time.time()
    findMoveMinimax(gs, validMoves, MAX_DEPTH, alpha, beta, gs.whiteToMove)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    print(nodes)
    return nextMove


def findMoveMinimax(gs, validMoves, depth, alpha, beta, whiteToMove):
    global nextMove
    global nodes
    nodes += 1
    if depth == 0 or gs.checkMate or gs.staleMate:
        return scoreBoard(gs)
    random.shuffle(validMoves)
    if whiteToMove:
        maxScore = -CHECKMATE
        random.shuffle(validMoves)
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinimax(gs, nextMoves, depth - 1, alpha, beta, False)
            gs.undoMove()
            if score > maxScore:
                maxScore = score
                if depth == MAX_DEPTH:
                    nextMove = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return maxScore
    else:
        minScore = CHECKMATE
        random.shuffle(validMoves)
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinimax(gs, nextMoves, depth - 1, alpha, beta, True)
            gs.undoMove()
            if score < minScore:
                minScore = score
                if depth == MAX_DEPTH:
                    nextMove = move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return minScore

def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE  #black win
        else:
            return CHECKMATE   #white win
    elif gs.staleMate:
        return STALEMATE
    # if not checkmate or stalemate:
    score = 0
    for row in range(8):
        for col in range(8):
            square = gs.board[row][col]
            if square != "--":
                piecePosScore = 0
                if square[1] != "K":
                    if square[1] == "p":
                        piecePosScore = piecePosScores[square][row][col]
                    else:
                        piecePosScore = piecePosScores[square[1]][row][col]
                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePosScore
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePosScore
    return score


