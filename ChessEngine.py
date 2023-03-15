import copy
import ChienKoNgu
from select import select
from shutil import move

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocate = (7, 4)
        self.blackKingLocate = (0, 4)
        self.inCheck = False
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.pins = []
        self.checks = []
        self.currentCastlingRight = castleRight(True, True, True, True)
        self.castleRightsLog = [castleRight(self.currentCastlingRight.wks, self.currentCastlingRight.wqs,
                                            self.currentCastlingRight.bks, self.currentCastlingRight.bqs)]


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocate = (move.endRow, move.endCol)
        if move.pieceMoved == "bK":
            self.blackKingLocate = (move.endRow, move.endCol)
        # promotion
        if move.isPawnPromotion:
            piecePromote = 'Q' #input("Promote R, N, B, Q: ")
            #piecePromote = piecePromote.upper()
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + piecePromote
        # Enpassant Move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"  # capturing the pawn
        # EnpassantPossible update
        if move.pieceMoved[1] == 'p' and (abs(move.startRow - move.endRow) == 2):  # only 2 squares pawn move
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.endCol)
        else:
            self.enpassantPossible = ()  # not en passant move
        self.enpassantPossibleLog.append(self.enpassantPossible)
        # update castling right - whenever king move or rook move
        self.updateCastleRight(move)
        self.castleRightsLog.append(castleRight(self.currentCastlingRight.wks, self.currentCastlingRight.wqs,
                                                self.currentCastlingRight.bks, self.currentCastlingRight.bqs))
        # castle move
        if move.isCastleMove:
            if move.endCol-move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"



    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocate = (move.startRow, move.startCol)
            if move.pieceMoved == "bK":
                self.blackKingLocate = (move.startRow, move.startCol)
        #undo enpassant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enpassantPossibleLog.pop()
            self.enpassantPossible = copy.deepcopy(self.enpassantPossibleLog[-1])
        #undo castling right
            self.castleRightsLog.pop()
            self.currentCastlingRight = copy.deepcopy(self.castleRightsLog[-1])
        #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"

            self.checkMate = False
            self.staleMate = False

    def updateCastleRight(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False
            


    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocate[0]
            kingCol = self.whiteKingLocate[1]
        else:
            kingRow = self.blackKingLocate[0]
            kingCol = self.blackKingLocate[1]

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSqs = []
                if pieceChecking[1] == 'N':
                    validSqs = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSq = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSqs.append(validSq)
                        if validSq[0] == checkRow and validSq[1] == checkCol:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSqs:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True

        return moves


    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove:
            kingRow = self.whiteKingLocate[0]
            kingCol = self.whiteKingLocate[1]
        else:
            kingRow = self.blackKingLocate[0]
            kingCol = self.blackKingLocate[1]
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6:
                        if self.board[4][c] == "--":
                            moves.append(Move((r, c), (4, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            insideRange = range(kingCol + 1, c-1)
                            outsideRange = range(c+1, 8)
                        else:
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c-2, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == 'b' and (square[1] == 'R' or square[1] == 'Q'):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c+2, 8)
                        else:
                            insideRange = range(kingCol - 1, c+1, -1)
                            outsideRange = range(c-1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == 'b' and (square[1] == 'R' or square[1] == 'Q'):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))
        else:
            if self.board[r+1][c] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1:
                        if self.board[3][c] == "--":
                            moves.append(Move((r, c), (3, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            insideRange = range(kingCol + 1, c-1)
                            outsideRange = range(c+1, 8)
                        else:
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c-2, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == 'w' and (square[1] == 'R' or square[1] == 'Q'):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))

            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c+2, 8)
                        else:
                            insideRange = range(kingCol - 1, c+1, -1)
                            outsideRange = range(c-1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == 'w' and (square[1] == 'R' or square[1] == 'Q'):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        straightDirections = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in straightDirections:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if (0 <= endRow < 8) and (0 <= endCol < 8):
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightDirections = ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for d in knightDirections:
            endRow = r + d[0]
            endCol = c + d[1]
            if (0 <= endRow < 8) and (0 <= endCol < 8):
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        diagonalDirections = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in diagonalDirections:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if (0 <= endRow < 8) and (0 <= endCol < 8):
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingDirections = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + kingDirections[i][0]
            endCol = c + kingDirections[i][1]
            if (0 <= endRow < 8) and (0 <= endCol < 8):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    # place king on the end of square to check
                    if allyColor == 'w':
                        self.whiteKingLocate = (endRow, endCol)
                    else:
                        self.blackKingLocate = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # place king back
                    if allyColor == 'w':
                        self.whiteKingLocate = (r, c)
                    else:
                        self.blackKingLocate = (r, c)
        self.getCastleMoves(r, c, moves, allyColor)

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocate[0]
            startCol = self.whiteKingLocate[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocate[0]
            startCol = self.blackKingLocate[1]

        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePins = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePins == ():
                            possiblePins = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        if (0 <= j <= 3 and pieceType == 'R') or \
                                (4 <= j <= 7 and pieceType == 'B') or \
                                (i == 1 and pieceType == 'p' and ((enemyColor == 'b' and 4 <= j <= 5) or (enemyColor == 'w' and 6 <= j <= 7))) or \
                                (pieceType == 'Q') or (i == 1 and pieceType == 'K'):
                            if possiblePins == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePins)
                                break
                        else:
                            break
                else:
                    break

        knightDirections = ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1))
        for m in knightDirections:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if (endPiece[0] == enemyColor) and (endPiece[1] == 'N'):
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
                    break

        return inCheck, pins, checks

    def getCastleMoves(self, r, c, moves, allyColor=""):
        if self.inCheck:
            return  #can't castle while be checked
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMove(r, c, moves, allyColor)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMove(r, c, moves, allyColor)

    def getKingsideCastleMove(self, r, c, moves, allyColor=""):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if allyColor == 'w':
                self.whiteKingLocate = (r, c+1)
            else:
                self.blackKingLocate = (r, c+1)
            inCheck1, pins, checks = self.checkForPinsAndChecks()
            if allyColor == 'w':
                self.whiteKingLocate = (r, c+2)
            else:
                self.blackKingLocate = (r, c+2)
            inCheck2, pins, checks = self.checkForPinsAndChecks()
            if allyColor == 'w':
                self.whiteKingLocate = (r, c)
            else:
                self.blackKingLocate = (r, c)

            if not inCheck1 and not inCheck2:
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))

    def getQueensideCastleMove(self, r, c, moves, allyColor=""):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c-3] == "--":
            if allyColor == 'w':
                self.whiteKingLocate = (r, c-1)
            else:
                self.blackKingLocate = (r, c-1)
            inCheck1, pins, checks = self.checkForPinsAndChecks()
            if allyColor == 'w':
                self.whiteKingLocate = (r, c-2)
            else:
                self.blackKingLocate = (r, c-2)
            inCheck2, pins, checks = self.checkForPinsAndChecks()
            if allyColor == 'w':
                self.whiteKingLocate = (r, c-3)
            else:
                self.blackKingLocate = (r, c-3)
            inCheck3, pins, checks = self.checkForPinsAndChecks()
            if allyColor == 'w':
                self.whiteKingLocate = (r, c)
            else:
                self.blackKingLocate = (r, c)

            if not inCheck1 and not inCheck2 and not inCheck3:
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))

class castleRight():
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs



class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"
        self.isCastleMove = isCastleMove
        self.isCapture = (self.pieceCaptured != "--")
        self.moveID = self.startCol * 1000 + self.startRow * 100 + self.endCol * 10 + self.endRow

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getFileRank(self.startRow, self.startCol) + self.getFileRank(self.endRow, self.endCol)
    def getFileRank(self, row, col):
        return str(self.colsToFiles[col] + self.rowsToRanks[row])

    def __str__(self):
        #castleMove:
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
        endSquare = self.getFileRank(self.endRow, self.endCol)
        #pawn move
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

        #piece moves
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += "x"
        return moveString + endSquare