from Pieces import ChessPiece
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "quiet"
import pygame as p

# setting Constants for size of chessboard, size of screen, and FPS rate
WIDTH = 700
HEIGHT = 700
SQUARE = 8
SQUAREHEIGHT = int(HEIGHT / SQUARE)
SQUAREWIDTH = int(WIDTH / SQUARE)
MAX_FPS = 15

# store image file of chess pieces into array
images = []
for i in range(SQUARE):
    row = [0 for j in range(SQUARE)]
    images.append(row)


class ChessBoard():
  def __init__(self, gameType):
    # Sets the game type of chess
    self.gameType = gameType
    self.chessboard = []
    self.piece_to_image = {"white" : {}, "black": {}}
    self.turn_number = 1
  
  def movePossible(self, x1, y1, x2, y2, shouldExecute):
    # returns whether a move from x1, y1, to x2, y2, is possible , ChessPiece.causingCheck
    # boundaries are special factors that may enable or limit unusual moves
    boundaries = [["r", ChessPiece.OutOfBounds], ["e", ChessPiece.castleMovementPossible], ["r", ChessPiece.captureSelf], 
    ["r", ChessPiece.causingCheck], ["e", ChessPiece.pawnSkipPossible], ["e", ChessPiece.promoteToQueen]]
    # we first check if the piece that is moving is moving in the correct turn order (black cannot make the first move)
    if(self.correctTurn(x1, y1)):
      return ChessPiece.movePossible(x1, y1, x2, y2, self.chessboard, boundaries, shouldExecute)

  def initializeBoard(self):
    # sets the board
    self.chessboard = []
    # initialialy filling it with empty pieces
    for i in range(8):
      blank_row = []
      for j in range(8):
        blank_row.append(ChessPiece("none", "none"))
      self.chessboard.append(blank_row)
    pieces_row = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook"]
    white_row = [ChessPiece(x, "white") for x in pieces_row]
    black_row = [ChessPiece(x, "black") for x in pieces_row]
    # if game type is regular then fill it with standard pieces
    if self.gameType == "regular":
      self.chessboard[7] = white_row
      self.chessboard[0] = black_row 
      blackPawnRow = [ChessPiece("pawn", "black")] * 8
      whitePawnRow = [ChessPiece("pawn", "white")] * 8
      self.chessboard[1]= blackPawnRow
      self.chessboard[6] = whitePawnRow
    
  # printing chessboard if want to see board in console
  def printChessBoard(self):
    print(" ________________")
    for row in self.chessboard:
      print("|", end=" ")
      print("".join(map(lambda x: str(x.pieceToNumber()) + " ", row)), end="")
      print("|")
    print(" ________________")
 
  # checks if, given the moving piece, we can move it given the turn order (as black cannot move two turns in a row)
  def correctTurn(self, x, y):
    pieceColor = self.chessboard[x][y].color
    if(self.turn_number % 2 == 1):
      correctColor = "white"
    else:
      correctColor = "black"
    if(pieceColor == correctColor):
      return True
    else:
      return False

  # given a position and a piece, it inserts it accordingly - used when user wants to make custom board
  def insertPiece(self, piece, color, x1, y1):
    chess_piece = ChessPiece(piece, color)
    self.chessboard[x1][y1] = chess_piece

  # given the piece name and color, it finds the corresponding image and loads it up
  def loadPieces(self):
    colors = {"black" : "dt", "white" : "lt"}
    chess_pieces = {"king" : "k", "queen" : "q", "rook" : "r", "bishop" : "b", "knight" : "n", "pawn" : "p"}
    for color in colors:
      for piece_type in chess_pieces:
        image = p.image.load("images/Chess_" + chess_pieces[piece_type] + colors[color] + "60.png")
        image = p.transform.scale(image, (SQUAREHEIGHT, SQUAREWIDTH))
        self.piece_to_image[color][piece_type] = image
  
  # displays the pieces on board
  def displayPieces(self, screen):
    # iterate through the chess pieces, and displays it on modified position on board
    for i in range(len(self.chessboard)):
      for j in range(len(self.chessboard[i])):
        piece = self.chessboard[i][j]
        if(piece.type != "none"):
          image = self.piece_to_image[piece.color][piece.type]
          screen.blit(image, (j * SQUAREWIDTH, i * SQUAREHEIGHT))
  
  # displays the background and uses for loop to create square grid
  def displayBackground(self, screen):
    light_color= p.Color(181, 136, 99)
    dark_color = p.Color(240, 217, 181)
    for i in range(SQUARE):
      for j in range(SQUARE):
        if((i + j) % 2 == 0):
          # draw white square
          color = light_color
        else:
          color = dark_color
        p.draw.rect(screen, color, p.Rect(j * SQUAREHEIGHT, i * SQUAREWIDTH, SQUAREHEIGHT, SQUAREWIDTH))
  
  # displays the game
  def displayGame(self, screen):
    self.displayBackground(screen)
    self.displayPieces(screen)

  # checks if the user is dragging a piece
  def checkDragging(self, screen, clock):
    # based on the position of the mouse, we convert it to the chessboard grid
    y, x = p.mouse.get_pos()
    x = int(x / SQUAREWIDTH)
    y = int(y / SQUAREHEIGHT)
    # we pick up the supposed piece
    piece = self.chessboard[x][y]
    if(piece.type == "none"):
      return
    # we initially set that chessboard grid area to empty to enable piece movement
    self.chessboard[x][y] = ChessPiece()
    # while we are continiously dragging the chess piece around we update the position in the UI
    while(p.mouse.get_pressed()[0]):
      for e in p.event.get():
        if(not p.mouse.get_pos()[0]):
          break
      # we store the position of the user pointer
      new_y, new_x = p.mouse.get_pos()
      self.displayGame(screen)
      # we display the chess piece where the mouse is
      chess_image = self.piece_to_image[piece.color][piece.type]
      screen.blit(chess_image, (new_y - SQUAREHEIGHT // 2, new_x - SQUAREWIDTH // 2))
      clock.tick(MAX_FPS)
      p.display.flip()
    # we check move the piece back into its original place
    self.chessboard[x][y] = piece
    # given the new position we try to move the piece (given by the user pointer) and the old position, we check if said move is valid
    # we set it to execute via True the moves, if it is valid
    if(self.movePossible(x, y, int(new_x / SQUAREWIDTH), int(new_y / SQUAREHEIGHT), True)):
      # if move is valid, increment turn number
      self.turn_number += 1
  
  def drawGameState(self):
    # set the background screen
    p.init()
    screen = p.display.set_mode((WIDTH + 200, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    # continously run untill the user exit the game
    running = True
    while running:
      self.displayGame(screen)
      # if we detect a press, then that means they are moving piece so we call said function
      if(p.mouse.get_pressed()[0]):
        self.checkDragging(screen, clock)
      for e in p.event.get():
        if e.type == p.QUIT:
          running = False
      clock.tick(MAX_FPS)
      p.display.flip()
 
firstGame = ChessBoard("regular")
firstGame.initializeBoard()
firstGame.loadPieces()
firstGame.drawGameState()