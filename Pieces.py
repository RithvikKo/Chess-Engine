# chessPiece class contains methods relevant towards describing both behavior and movement of chess pieces
class ChessPiece():
    # setting attributes: color and type of chess piece
    def __init__(self, type = "none", color = "none"):
        self.type = type
        self.color = color
        # direction is for checking which way pawns move
        if self.color == "white":
            self.dir = "up"
        if self.color == "black":
            self.dir = "down"
        self.has_moved = False

    def pieceToNumber(self):
        # this converts pieces to numbers, which can easily be displayed in board
        numberPiece = self.type
        possible = {"none": 0, "pawn": 1, "knight": 2, "bishop": 3, "rook": 4, "queen": 5, "king": 6}
        return possible[numberPiece]

    # paramater is what coords the piece currently is in, where it wants to go, and the chessboard
    def pawnMovementPossible(x1, y1, x2, y2, chessboard):
    # checks to see if pawn is moving forward, relative to facing direction
        if chessboard[x1][y1].dir == "down":
            dir = 1
        else:
            dir = -1
        if y1 == y2 and x1 + dir == x2:
            # lets pawn move foward if empty
            if chessboard[x2][y2].type == "none":
                return True
        # checks if pawn can capture enemy piece diagonally
        elif x1 + dir == x2 and (y1 == y2 + 1 or y1 == y2 - 1):
            return chessboard[x2][y2].type != "none"
        return False


    def bishopMovementPossible(x1, y1, x2, y2, chessboard):
        # set represents all possible spaces the bishop can move to
        bishopMoves = set()
        # can either move up or down
        for directionY in (1, -1):
            # can either move right or left
            for directionX in (1, -1):
                # all direction generate 4 possible diagonals, of which we check
                i = 1
                while not ChessPiece.OutOfBounds(chessboard, None, None, x1+i * directionX, y1+i * directionY):
                    # as long as square is empty, bishop can move into it
                    if chessboard[x1+i * directionX][y1+i * directionY].type == "none":
                        bishopMoves.add((x1+i * directionX, y1+i * directionY))
                    else:
                        # if bishop hits a piece it can capture it, and can move no further in said diagonal
                        bishopMoves.add((x1+i * directionX, y1+i * directionY))
                        break
                    i += 1
        # check if the place we want to go to is in possible moves
        if (x2, y2) in bishopMoves:
            return True
        return False


    def knightMovementPossible(x1, y1, x2, y2, chessboard):
        # because knight moves in L shape, we use math to confirm L shape, and if so return True
        coordchanges = [abs(x1 - x2), abs(y1 - y2)]
        if (max(coordchanges) == 2 and min(coordchanges) == 1):
            return True
        return False


    def rookMovementPossible(x1, y1, x2, y2, chessboard):
        rookMoves = set()
        # rook can move up and down, so we vary the direciton by either 1 or -1
        for directionX in (1, -1):
            i = 1
            # keep on moving in direction till out of bounds
            while not ChessPiece.OutOfBounds(chessboard, None, None, x1+i * directionX, y1):
                if chessboard[x1+i * directionX][y1].type == "none":
                    rookMoves.add((x1+i * directionX, y1))
                else:
                    # if encounter piece then add that piece to possible moves and exit out
                    rookMoves.add((x1+i * directionX, y1))
                    break
                i +=1
        # rook can move side by side, so we vary the direction by either 1 or -1
        for directionY in (1, -1):
            i = 1
            # keep on moving rook till out of bounds
            while not ChessPiece.OutOfBounds(chessboard, None, None, x1, y1+i * directionY):
                if chessboard[x1][y1+i * directionY].type == "none":
                    rookMoves.add((x1, y1+i * directionY))
                else:
                    # if encounter piece, then add that position and then exit
                    rookMoves.add((x1, y1+i * directionY))
                    break
                i += 1
        # if the goal distination is in possible moves, return true
        if (x2, y2) in rookMoves:
            return True
        return False

    def queenMovementPossible(x1, y1, x2, y2, chessboard):
        # because queen movement is the same as both rook and bishop, we check if either rook or bishop is satisfied
        return ChessPiece.rookMovementPossible(x1, y1, x2, y2, chessboard) or ChessPiece.bishopMovementPossible(x1, y1, x2, y2, chessboard)

    def kingMovementPossible(x1, y1, x2, y2, chessboard):
        # because a king can only move one step, we do quick math to confirm it moved only one step
        coordChanges = [abs(x1 - x2), abs(y1 - y2)]
        if (max(coordChanges)) == 1:
            return True
        return False
    
    def pawnSkipPossible(chessboard, x1, y1, x2, y2, shouldExecute):
        # check if pawn can move forward two spaces
        piece = chessboard[x1][y1]
        returnValue = False
        # based on direction, checks which way pawn is moving
        if(x1 == 1 and piece.color == "black"):
            # if the different in vertical movement is two and we are at back row, we can pawn skip
            if(y1 == y2 and x1 + 2 == x2):
                returnValue = True
        if(x1 == 6 and piece.color == "white"):
            if(y1 == y2 and x1 - 2 == x2):
                returnValue = True
        if returnValue:
            # if execute order is given, we execute move
            if(shouldExecute):
                chessboard[x2][y2] = piece
                chessboard[x1][y1] = ChessPiece()
        return returnValue
    
    def promoteToQueen(chessboard, x1, y1, x2, y2, shouldExecute):
        # we check if the pawn movement is possible and if it reaches the end row
        if ChessPiece.pawnMovementPossible(x1, y1, x2, y2, chessboard) and (x2 == 7 or x2 == 0):
            # if execute order given, make the pawn a queen at end row
            if(shouldExecute):
                chessboard[x2][y2] = ChessPiece("queen", chessboard[x1][y1].color)
                chessboard[x1][y1] = ChessPiece()
            return True
        else:
            return False

    def castleMovementPossible(chessboard, x1, y1, x2, y2, shouldExecute):
        # get the two pieces
        king = chessboard[x1][y1]
        rook = chessboard[x2][y2]
        # checks if the two pieces are the neccessary ones (rook and king) and if they haven't moved before
        if(king.type == "king" and king.has_moved == False and rook.type == "rook" and rook.has_moved == False):
            if(king.color == rook.color and x1 == x2):
                # checks if the king is under attack - cannot castle if so
                if(ChessPiece.pieceInAttack(chessboard, x1, y1, king.color)):
                    return False
                # checks if castling left
                if(y2 == 0):
                    #checks if path is clear and the path isn't under attack
                    for y_pos in [1, 2]:
                        if ChessPiece.pieceInAttack(chessboard, x1, y_pos, king.color) or chessboard[x1][y_pos].type != "none":
                            return False
                # we can now castle if execute roder is given
                    if(shouldExecute):
                        chessboard[x1][1] = king
                        chessboard[x1][2] = rook
                        chessboard[x1][0] = ChessPiece()
                        chessboard[x1][3] = ChessPiece()
                    return True

                if(y2 == 7):
                    # checks if path is clear
                    for y_pos in [4, 5, 6]:
                        if chessboard[x1][y_pos].type != "none":
                            return False
                    # check if path is free from check
                    for y_pos in [4, 5]:
                        if ChessPiece.pieceInAttack(chessboard, x1, y_pos, king.color):
                            return False
                    # we can now castle
                    if(shouldExecute):
                        chessboard[x1][5] = king
                        chessboard[x1][4] = rook
                        chessboard[x1][7] = ChessPiece()
                        chessboard[x1][3] = ChessPiece()
                    return True
        return False 

    # checks if moving a piece would cause the king to be in check (meaning said move is not valid)
    def causingCheck(chessboard, x1, y1, x2, y2):
        # saving pieces, and then simulate moving the piece to destination
        moving_piece = chessboard[x1][y1]
        deleted_piece = chessboard[x2][y2]
        chessboard[x2][y2] = moving_piece
        chessboard[x1][y1] = ChessPiece()
        answer = False
        # now we check if the king is in check, and if so move is not valid
        for i in range(len(chessboard)):
            for j in range(len(chessboard[i])):
                # find the position of the king
                if(chessboard[i][j].type == "king" and chessboard[i][j].color == moving_piece.color):
                    # we check if the piece (the king) is under attack (in check). 
                    answer =  ChessPiece.pieceInAttack(chessboard, i, j, moving_piece.color)
        # undo our simulated moves, and return whether the move is valid
        chessboard[x1][y1] = moving_piece
        chessboard[x2][y2] = deleted_piece
        return answer
    
    # given the position of a piece, it checks if the piece can be captured by other pieces of enemy color
    def pieceInAttack(chessboard, x1, y1, friendly_color):
        # traverses all other pieces in the board
        for x in range(len(chessboard)):
            for y in range(len(chessboard[x])):
                # checks if any of those pieces can capture the other piece
                attacking_color = chessboard[x][y].color
                # checks if the attacking piece is of different color than defending piece
                if(attacking_color != friendly_color):
                    checkers = [["r", ChessPiece.captureSelf], ["r", ChessPiece.OutOfBounds]]
                    # checks if the attacking piece can move to defending piece
                    if(ChessPiece.movePossible(x, y, x1, y1, chessboard, checkers, False)):
                        return True
        return False

    # checks if a piece is capturing a piece of the same color
    def captureSelf(chessboard, x1, y1, x2, y2):
        if chessboard[x1][y1].color == chessboard[x2][y2].color or chessboard[x1][y1].type == "none":
            return True
        return False

    # checks if the piece is going out of bounds
    def OutOfBounds(chessboard, x1, y1, x2, y2):
        if x2 >= len(chessboard) or x2 < 0 or y2 >= len(chessboard) or y2 < 0:
            return True
        return False

    # checks if, given the coord of a piece as well as a destination, if the move is valid
    # takes in the coords, the board, as well as backgroundChecks
    # backgroundChecks are filter functions that check for filter cases. 
    # This can either be "r" (restrictive), meaning that it makes certain moves not allowed
    # Or it can be "e" (exception), meaning a move is allowed when it would usually not be alllowed
    # this makes chess movement more dynamic, making it very fast to implement new chess movement rules for different chess versions
    def movePossible(x1, y1, x2, y2, chessboard, backgroundChecks, shouldExecute):
        # grab the piece form the chessboard
        piece = chessboard[x1][y1]
        # checks the filter functions
        counter = 0
        for check in backgroundChecks:
            perm = check[0]
            func = check[1]
            # applies filter functions to see if chess move is not valid
            # note that distinction between "r" and "e" is used for clarity's sake, rather then code effeciency
            if perm == "r":
                counter += 1
                x = func(chessboard, x1, y1, x2, y2)
                if x == True:
                    return False
            if perm == "e":
                if func(chessboard, x1, y1, x2, y2, shouldExecute) == True:
                    return True
        # maps a chess piece to its corresponding move-checker function
        checkerPiece = ["empty", "pawn", "knight", "bishop", "rook", "queen", "king"]
        checkerFunction = [lambda x: False, ChessPiece.pawnMovementPossible, ChessPiece.knightMovementPossible, ChessPiece.bishopMovementPossible, 
            ChessPiece.rookMovementPossible, ChessPiece.queenMovementPossible, ChessPiece.kingMovementPossible]
        # check if the move is valid for the certain chess-type. For example, only a bishop can move diagonals
        checker = {checkerPiece[i] : checkerFunction[i] for i in range(len(checkerPiece))}
        # returns whether the move was valid
        result =  checker[piece.type](x1, y1, x2, y2, chessboard)
        if(result == True):
            chessboard[x1][y1].has_moved = True
        # if we are given execute order, then we move the chess piece
        if shouldExecute == True:
            chessboard[x2][y2] = piece
            chessboard[x1][y1] = ChessPiece()
        return result