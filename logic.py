# %%

import random
class Player:
    """This will the player class it will create a player depanding on the color that it got passed
it will contain an id unique to its color
pieces unique to its color
a self.color to represent the player color
self.win_piece array to hold the pieces that have reached the end
    """
    def __init__(self, color):
      if color == 'red':
          self.id = 10
          self.pieces = [Piece(101, False, True), Piece(102, False, True), Piece(103, False, True), Piece(104, False, True)]
          self.color = 'red'
          self.win_piece = []
      elif color == 'blue':
          self.id = 30
          self.pieces = [Piece(301, True, True), Piece(302, True, True), Piece(303, True, True), Piece(304, True, True)]
          self.color = 'blue'
          self.win_piece = []
      elif color == 'yellow':
          self.id = 40
          self.pieces = [Piece(401, True, False), Piece(402, True, False), Piece(403, True, False), Piece(404, True, False)]
          self.color = 'yellow'
          self.win_piece = []
      elif color == 'green':
          self.id = 20
          self.pieces = [Piece(201,False, False), Piece(202,False, False), Piece(203, False, False), Piece(204, False, False)]
          self.color = 'green'
          self.win_piece = []

class Piece:
    """this is the piece class where it's called Four times when a player is a created
each piece created for a player gets passed an id unique to that piece and direction1 and direction2  which are boolean value, which will use to find the next move
True True => up, False False => down, True False => left, False True => right
the piece will also have x,y for their position and an i which is the index of the piece in the block. for example lets take piece 102
[1,102,1] the i of 102 is 1 - it will be used for deleting the piece and it's generated id from the current block
piece will also have a started and won boolean values which is self-explantory."""
    def __init__(self, id, direction1, direction2):
        self.id = id
        self.direction1 = direction1
        self.direction2 = direction2
        self.x = -1
        self.y = -1
        self.i = 0
        self.started = False
        self.won = False
        
class Ludo:
    def __init__(self, num):
        """it will create players depanding on the num
        """
        self.state = True 
        try:
            if num == 2:
                self.players = [Player('red'), Player('green')]
            elif num == 3:
                self.players = [Player('red'), Player('green'), Player('blue')]
            elif num == 4:
                self.players = [Player('red'), Player('green'), Player('blue'), Player('yellow')]
            else:
                raise Exception(num < 2 or num > 4)
        except Exception:
            print('The game only supports 2-4 Players!')
        self.board = [
            [[0], [0], [0],[0], [0], [0],[1],[20],[1],[0],[0],[0],[0],[0],[0]],
         [[0],[10],[0],[10],[0],[0],[1],[20],[20],[0],[0],[20],[0],[20],[0]],
         [[0],[0],[0],[0],[0],[0],[1],[20],[1],[0],[0],[0],[0],[0],[0]],
         [[0],[10],[0],[10],[0],[0],[1],[20],[1],[0],[0],[20],[0],[20],[0]],
         [[0],[0],[0],[0],[0],[0],[1],[20],[1],[0],[0],[0],[0],[0],[0]],
         [[0],[0],[0],[0],[0],[0],[1],[20],[1],[0],[0],[0],[0],[0],[0]],
         [[1],[10],[1],[1],[1],[1],[1000],[1002],[1000],[1],[1],[1],[1],[1],[1]],
         [[10],[10],[10],[10],[10],[10],[1001],[1000],[1003],[40],[40],[40],[40],[40],[40]],
         [[1],[1],[1],[1],[1],[1],[1000],[1004],[1000],[1],[1],[1],[1],[40],[1]],
         [[0],[0],[0],[0],[0],[0],[1],[30],[1],[0],[0],[0],[0],[0],[0]],
         [[0],[30],[0],[30],[0],[0],[1],[30],[1],[0],[0],[10],[0],[10],[0]],
         [[0],[0],[0],[0],[0],[0],[1],[30],[1],[0],[0],[0],[0],[0],[0]],
         [[0],[30],[0],[30],[0],[0],[1],[30],[1],[0],[0],[10],[0],[10],[0]],
         [[0],[0],[0],[0],[0],[0],[30],[30],[1],[0],[0],[0],[0],[0],[0]],
         [[0],[0],[0],[0],[0],[0],[1],[30],[1],[0],[0],[0],[0],[0],[0]]
         ]

    def dice(self):
        """
        a dice that generates a number between 1,6
        """
        return random.randint(1,6) 
    def move_calc(self, piece, next_x, next_y, adjusted=False):
            """
            moves the piece to the next block, assinging the new x,y to the piece x and y\\
            Args:
                piece (Piece): the current playing piece
                next_x (int): the x coordinate of the next block
                next_y (int): the y coordinate of the next block
                adjusted (bool, optional): if next block contains a piece of a diffrent player than the current player, This is set to True. Defaults to False.
            """
            if piece.x != -1 and piece.y != -1:
                del self.board[piece.y][piece.x][piece.i + 1] 
                del self.board[piece.y][piece.x][piece.i] 
            if adjusted: 
                for player in self.players:
                    for holder_piece in player.pieces:
                        if str(holder_piece.id) in self.board[next_y][next_x]:
                            holder_piece.started = False
                            holder_piece.x = -1
                            holder_piece.y = -1
                            del self.board[next_y][next_x][-2] 
                            del self.board[next_y][next_x][-1] 
            piece.i = len(self.board[next_y][next_x]) 
            self.board[next_y][next_x].append(str(piece.id))  
            self.board[next_y][next_x].append(int(str(piece.id)[0]))  
            piece.x = next_x; piece.y = next_y   

    
    def overlapping(self, piece, next_x, next_y):
        """Checks if the next Block is occupied

        Args:
            piece (Piece): the current playing piece
            next_x (int): the x coordinate of the next block
            next_y (int): the y coordinate of the next block

        Conditions:
            Calls self.move_calc normally if next block empty or contains the same player piece
            Calls an adjusted self.move_calc if next block contains 1 piece of another player piece
            return if next block contains 2 or more pieces of another player
        """
        if len(self.board[next_y][next_x]) == 1:
            self.move_calc(piece, next_x, next_y)
            return False
        else: 
            if int(self.board[next_y][next_x][-1]) == int(str(piece.id)[0]): 
                self.move_calc(piece, next_x, next_y)
                return False
            elif int(self.board[next_y][next_x][-1]) != int(str(piece.id)[0]) and self.board[next_y][next_x][1:].count(self.board[next_y][next_x][-1]) == 1: 
                self.move_calc(piece, next_x, next_y,adjusted= True)
            elif int(self.board[next_y][next_x][-1]) != int(str(piece.id)[0]) and self.board[next_y][next_x][1:].count(self.board[next_y][next_x][-1]) >= 2:
                return
    def start(self, piece_id):
        """moves the piece out of their cell and to the beggning position corresponding to their color

        Args:
            piece_id (Int): the current playing piece id
        """
        for player in self.players:
            for piece in player.pieces:
                if piece.id == piece_id:
                        if player.id == 10:
                            if len(self.board[6][1]) != 1:
                                return
                            self.move_calc(piece, 1, 6)
                            piece.started = True 
                        elif player.id == 20:
                            if len(self.board[1][8]) != 1:
                                return
                            self.move_calc(piece, 8, 1)
                            piece.started = True
                        elif player.id == 30:     
                            if len(self.board[13][6]) != 1:
                                return                   
                            self.move_calc(piece, 6, 13)
                            piece.started = True
                        elif player.id == 40:
                            if len(self.board[8][13]) != 1:
                                return
                            self.move_calc(piece, 13, 8)
                            piece.started = True
    def right(self, piece):
            """Adjusts the next_y, next_x of the block accordingly before passing it to the overlapping function

            Args:
                piece (Piece): the current playing piece id
            """
            next_x, next_y = piece.x + 1, piece.y
            if next_x > 14: 
                next_x = piece.x
                next_y += 1 
                piece.direction1 = False 
                piece.direction2 = False
            if self.board[piece.y][next_x] == [1000]: 
                next_y -= 1 
                piece.direction1 = True 
            elif self.board[piece.y][next_x] == [0]: 
                next_y += 1
                next_x = piece.x
                piece.direction1 = False
                piece.direction2 = False
            self.overlapping(piece, next_x, next_y)
                 
    def up(self,piece):
        """Adjusts the next_y, next_x of the block accordingly before passing it to the overlapping function

        Args:
            piece (Piece): the current playing piece id
        """
        next_x, next_y = piece.x, piece.y - 1
        if next_y == -1:
            next_y = piece.y
            next_x = piece.x + 1
            piece.direction1 = False
        elif self.board[next_y][next_x] == [1000]:
            next_x -= 1
            piece.direction2 = False
        elif self.board[next_y][piece.x] == [0]:
            next_x += 1
            next_y = piece.y
            piece.direction1 = False
        self.overlapping(piece, next_x, next_y)


    def down(self, piece):
        """Adjusts the next_y, next_x of the block accordingly before passing it to the overlapping function

        Args:
            piece (Piece): the current playing piece id
        """
        next_x, next_y = piece.x, piece.y + 1
        if next_y > 14:
            next_y = piece.y
            next_x -= 1
            piece.direction1 = True
        elif self.board[next_y][next_x] == [1000]:
            next_x += 1
            piece.direction2 = True
        elif self.board[next_y][next_x] == [0]:
            next_x -= 1
            next_y = piece.y
            piece.direction1 = True
        self.overlapping(piece, next_x, next_y)


    def left(self, piece):
        """Adjusts the next_y, next_x of the block accordingly before passing it to the overlapping function

        Args:
            piece (Piece): the current playing piece id
        """
        next_x, next_y = piece.x - 1, piece.y
        if self.board[next_y][next_x] == [1000]:
            next_y += 1
            piece.direction1 = False
        elif self.board[piece.y][next_x] == [0]:
            next_y -= 1
            next_x = piece.x
            piece.direction2 = True
        elif next_x == -1:
            next_x = piece.x
            next_y -= 1
            piece.direction2 = True
        self.overlapping(piece, next_x, next_y)


    def check_end_line(self,player, piece):
        """Checks if the piece has reached their corresponding color block and it's end 

        Args:
            player (Player): the current player
            piece (Piece): the current playing piece

        Conditions:
            if piece out of bound returns None
            if pieces each their corresponding last color block they get added to their player win pieces list
            if player win pieces is of length 4 returns True
        """
        if piece.started and not piece.won:
            if (piece.x + 1) > 14 or (piece.x - 1) == -1 or (piece.y + 1) > 14 or (piece.y - 1) == -1:
                return 
            elif (player.id == 10 and self.board[piece.y][piece.x + 1] == [1001]) or (player.id == 20 and self.board[piece.y + 1][piece.x] == [1002])  or (player.id == 40 and self.board[piece.y][piece.x - 1] == [1003]) or (player.id == 30 and self.board[piece.y - 1][piece.x] == [1004]):
                player.win_piece.append(piece)
                del self.board[piece.y][piece.x][piece.i + 1]
                del self.board[piece.y][piece.x][piece.i]
                piece.started = False
                piece.won = True
            if len(player.win_piece) == 4:
                print(f' {player.color} WON ')
                self.state = False
                return True


    def move(self, piece_id):
        """moves the chosen piece based on its available direction

        Args:
            piece_id (Int):  the current playing piece id
        """
        for player in self.players:
                for piece in player.pieces:
                    if piece.id == piece_id:
                        if piece.started:                   
                            if player.id == self.board[piece.y][piece.x][0] and player.id == 10:                                
                                if self.check_end_line(player,piece):
                                    return
                                else:
                                    self.right(piece)
                            elif player.id == self.board[piece.y][piece.x][0] and player.id == 20:                                
                                if self.check_end_line(player,piece):
                                    return
                                else:
                                    self.down(piece)
                            elif player.id == self.board[piece.y][piece.x][0] and player.id == 30:                                
                                if self.check_end_line(player,piece):
                                    return
                                else:
                                    self.up(piece)
                            elif player.id == self.board[piece.y][piece.x][0] and player.id == 40:                                
                                if self.check_end_line(player,piece):
                                    return
                                else:
                                    self.left(piece)
                            elif not piece.direction1 and piece.direction2:
                                self.right(piece)

                            elif piece.direction1 and not piece.direction2:
                                self.left(piece)
                            elif piece.direction1 and piece.direction2:
                                self.up(piece)
                            elif not piece.direction1 and not piece.direction2:
                                self.down(piece)
    


# %%
