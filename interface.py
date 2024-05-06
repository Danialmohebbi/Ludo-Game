from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from logic import Ludo
class CustomLabel:
    """Creates a label for the image for a piece and number of pieces of the current block of a piece
    """
    def __init__(self, id, window):
        self.id = id
        self.label = Label(window)
        self.counter_label = Label(window)
        self.counting = 1
        self.x = 0
        self.y = 0
class Window:
    """Creates The Window of the game
    """
    def __init__(self,ludo):
        self.game = ludo
        self.window = Tk()
        self.window.title('Ludo')
        self.background_image = PhotoImage(file="Board.png")
        self.background_label = Label(self.window, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        self.window.geometry('1600x1000')
        self.window.resizable(False, False)
        self.curr_player = 0
        self.play = Button(self.window, text="Start", command=self.enter_data)
        self.play.grid(row=1, column=0)
        self.announcer_label = Label(self.window, text=f'it is {self.game.players[self.curr_player].color} turn.')
        self.announcer_label.place(x=750,y=30)
        self.dice_label = Label(self.window)
        self.dice_label.place(x=750,y=10)
        self.dice1 = self.game.dice()
        self.dice_label.configure(text=f'{self.game.players[self.curr_player].color} has gotten {self.dice1} on the dice!!!')

        self.pieces_pics = ['red_piece-removebg-preview.png',
                            'green_piece.png',
                            'blue_piece.png',
                            'yellow_piece.png']
        self.labels = [
            [CustomLabel(1, self.window), CustomLabel(2, self.window), CustomLabel(3, self.window), CustomLabel(4, self.window)],
            [CustomLabel(1, self.window), CustomLabel(2, self.window), CustomLabel(3, self.window), CustomLabel(4, self.window)],
            [CustomLabel(1, self.window), CustomLabel(2, self.window), CustomLabel(3, self.window), CustomLabel(4, self.window)],
            [CustomLabel(1, self.window), CustomLabel(2, self.window), CustomLabel(3, self.window), CustomLabel(4, self.window)]
        ]
        mainloop()
    def enter_data(self):
        """
        Gets the which piece to move as an Int from the player
        And moves the piece
        """
        movable_pieces = [piece if not piece.won else None for piece in self.game.players[self.curr_player].pieces]
        if self.dice1 < 6:
            for piece in movable_pieces:
                if piece.started:
                    break
            else:
                self.curr_player = (self.curr_player + 1) % len(self.game.players)
                self.announcer_label.configure(text=f'it is {self.game.players[self.curr_player].color} turn.')
                self.dice1 = self.game.dice()
                self.dice_label.configure(text=f'{self.game.players[self.curr_player].color} has gotten {self.dice1} on the dice!!!')
                return
        for player in self.game.players:
            if len(player.win_piece) == 4:
                    self.victory(player)
                    return
        s_holder = f'Choose one of the following pieces: '
        for i in range(len(movable_pieces)):
            if movable_pieces[i] == None:
                continue
            s_holder += ' '+ str(movable_pieces[i].id)[-1]
        input_piece = simpledialog.askinteger(title='Available Pieces', prompt=s_holder)
        if input_piece >= 5 or input_piece < 1:
            messagebox.showerror(message='Each Player has 4 pieces!!!')
            self.enter_data()
            return
        choosed_piece = movable_pieces[input_piece - 1]
        if choosed_piece == None:
            self.enter_data()
            return
        while self.dice1 > 0:
            if choosed_piece.started:
                self.game.move(choosed_piece.id)
            elif not choosed_piece.started and (not choosed_piece.won) and self.dice1 == 6:
                self.game.start(choosed_piece.id)
                self.dice1 -= 6
            self.dice1 -= 1
        for player in self.game.players:
            for piece in player.pieces:
                self.update(piece)
        self.curr_player = (self.curr_player + 1) % len(self.game.players)
        self.announcer_label.configure(text=f'it is {self.game.players[self.curr_player].color} turn.')
        self.dice1 = self.game.dice()
        self.dice_label.configure(text=f'{self.game.players[self.curr_player].color} has gotten {self.dice1} on the dice!!!')
    def victory(self, player):
        """
            Ends the program
        Args:
            player (Player): the player that has won
        """
        self.window.quit()
        message = f"{player.color} has Won the game"
        messagebox.showinfo("Player Won and Game Ended", message) 
    def update(self, piece): 
        """Updates the pieces labels and the number label that have started and not won

        Args:
            piece (Piece): the piece to be updated
        """
        piece_label = self.labels[int(str(piece.id)[0]) - 1][int(str(piece.id)[-1])-1] 
        if piece.x == -1 and piece.y == -1 or not piece.started or piece.won:
            piece_label.label.place_forget()
            piece_label.counter_label.place_forget()
        if piece.started:
                    piece_label.x = 300 + ((piece.x + 1) * 60)
                    piece_label.y = 60 + ((piece.y) * 60)
                    path = self.pieces_pics[int(str(piece.id)[0]) - 1]
                    piece_img = PhotoImage(file=path)
                    piece_label.label.configure(image=piece_img)
                    piece_label.label.image = piece_img
                    piece_label.label.place(x=piece_label.x, y=piece_label.y)
                    x = self.game.board[piece.y][piece.x][1:].count(int(str(piece.id)[0])) 
                    fonting = None
                    if x == 1:
                        fonting = 10
                    elif x == 2:
                        fonting = 15
                    elif x == 3:
                        fonting = 20
                    elif x == 4:
                        fonting = 25                       
                    piece_label.counter_label.configure(text = f'{x}', font=('times', fonting))
                    piece_label.counter_label.place(x=piece_label.x + 20, y = piece_label.y - 20)

        