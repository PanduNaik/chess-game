from tkinter import *
from PIL import ImageTk, Image
from properties import *
from pieces import *
from gamelogic import *


class ChessButton:
    def __init__(self, button, bg):
        self.button = button
        self.bg = bg

class DeadLabel:
    def __init__(self, label):
        self.label = label

buttons = {}
dead_labels = {WHITE: {'row': 0, 'col': 0}, BLACK: {'row': 0, 'col': 0}}
msg_box = None

selected = False
start = None
end = None
moves = []
check = False
kingpos = None
gameover = False

def unHighlightMoves(moves):
    for move in moves:
        buttons[move].button.configure(bg=buttons[move].bg)

def highlightMoves(moves):
    for move in moves:
        buttons[move].button.configure(bg=colors['highlight'])

def action(mark):
    global selected
    global start
    global end
    global moves
    global check
    global kingpos
    global gameover
    global msg_box

    if gameover:
        return
    
    if selected:
        end = mark
        if end != start:
            if end not in moves:
                msg_box.configure(text="Invalid Move!")
                return
            else:
                result = game.validateEnd(start, end)
                if result['valid']:
                    msg_box.configure(text=result['msg'])
                    buttons[start].button.configure(image="",
                                             width=dimensions['width']['primary'],
                                             height=dimensions['height']['primary'])
                    buttons[end].button.configure(image=result['start-icon'],
                                             width=dimensions['width']['pixels'],
                                             height=dimensions['height']['pixels'])
                    if check:
                        buttons[kingpos].button.configure(bg=buttons[kingpos].bg)
                        check = False
                        kingpos = None
                    if result['kill']:
                        r = dead_labels[result['opp-color']]['row']
                        c = dead_labels[result['opp-color']]['col']
                        dead_labels[result['opp-color']][(r,c)].label.configure(image=result['end-icon'],
                                                                       width=dimensions['width']['dead-pixels'],
                                                                       height=dimensions['height']['dead-pixels'])
                        dead_labels[result['opp-color']]['col'] += 1
                        if dead_labels[result['opp-color']]['col'] == 4:
                            dead_labels[result['opp-color']]['row'] += 1
                            dead_labels[result['opp-color']]['col'] = 0
                    if result['opp-check']:
                        check = True
                        kingpos = result['king-pos']
                        buttons[result['king-pos']].button.configure(bg=colors['check'])
                    if result['check-mate']:
                        buttons[result['king-pos']].button.configure(bg=colors['mate'])
                        gameover = True
                else:
                    msg_box.configure(text=result['msg'])
                    return
        selected = False
        buttons[start].button.configure(bg=buttons[start].bg)
        unHighlightMoves(moves)
        moves = []
    else:
        start = mark
        valid, msg, moves = game.validateStart(start)
        if valid and len(moves) != 0:
            selected = True
            buttons[start].button.configure(bg=colors['start'])
            highlightMoves(moves)
        msg_box.configure(text=msg)
            

def placePieces():
    for i in range(8):
        white_mark = chr(65+i) + str(2)
        black_mark = chr(65+i) + str(7)
        buttons[white_mark].button.configure(image=ICONS[WHITE][Pawn],
                                             width=dimensions['width']['pixels'],
                                             height=dimensions['height']['pixels'])
        buttons[black_mark].button.configure(image=ICONS[BLACK][Pawn],
                                             width=dimensions['width']['pixels'],
                                             height=dimensions['height']['pixels'])
        game.game_board[(i, 1)] = Pawn(WHITE, ICONS[WHITE][Pawn], 1)
        game.game_board[(i, 6)] = Pawn(BLACK, ICONS[BLACK][Pawn], -1)

    placers = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    for i in range(8):
        white_mark = chr(65+i) + str(1)
        black_mark = chr(65+7-i) + str(8)
        buttons[white_mark].button.configure(image=ICONS[WHITE][placers[i]],
                                             width=dimensions['width']['pixels'],
                                             height=dimensions['height']['pixels'])
        buttons[black_mark].button.configure(image=ICONS[BLACK][placers[i]],
                                             width=dimensions['width']['pixels'],
                                             height=dimensions['height']['pixels'])
        game.game_board[(i, 0)] = placers[i](WHITE, ICONS[WHITE][placers[i]])
        game.game_board[(7-i, 7)] = placers[i](BLACK, ICONS[BLACK][placers[i]])
        
def generateChessBoard():
    for i in range(8):
        label_bottom = Label(leftPanel,
                             text=chr(65+i),
                             width=dimensions['width']['primary'],
                             height=dimensions['height']['secondary'],
                             bg=colors['label'],
                             relief="ridge")
        label_left = Label(leftPanel,
                             text=str(i+1),
                             width=dimensions['width']['secondary'],
                             height=dimensions['height']['primary'],
                             bg=colors['label'],
                             relief="ridge")
        label_bottom.grid(row=8, column=i+1, sticky=W)
        label_left.grid(row=7-i, column=0, sticky=W)
        for j in range(8):
            color = colors['black']
            relief = "raised"
            if (i+j)&1:
                color = colors['white']
                relief = "flat"
            mark = chr(65+i)+str(j+1)
            b = Button(leftPanel,
                       bg=color,
                       relief=relief,
                       width=dimensions['width']['primary'],
                       height=dimensions['height']['primary'],
                       cursor="hand2",
                       command=lambda j=mark: action(j))
            buttons[mark] = ChessButton(b, color)
            buttons[mark].button.grid(row=7-j, column=i+1, sticky=W)
    placePieces()

def generateAdditionalFeatures():
    global msg_box
    
    dead_label = Label(rightPanel,
                       text="Dead Pieces",
                       width=dimensions['width']['dead-label'],
                       height=dimensions['height']['dead-label'],
                       relief="ridge",
                       bg=colors['bg']['dead-label'],
                       fg=colors['fg'])
    dead_label.grid(row=0, column=9, columnspan=8, sticky=W)
    dead_label_white = Label(rightPanel,
                       text="White",
                       width=dimensions['width']['white-dead-label'],
                       height=dimensions['height']['dead-label'],
                       relief="groove",
                       bg=colors['bg']['white-dead-label'])
    dead_label_white.grid(row=1, column=9, columnspan=4, sticky=W)
    dead_label_black = Label(rightPanel,
                       text="Black",
                       width=dimensions['width']['black-dead-label'],
                       height=dimensions['height']['dead-label'],
                       relief="groove",
                       bg=colors['bg']['black-dead-label'],
                       fg=colors['fg'])
    dead_label_black.grid(row=1, column=13, columnspan=4, sticky=W)
    for i in range(4):
        label_color = WHITE
        bg = colors['bg']['white-dead']
        for j in range(8):
            if  j > 3:
                label_color = BLACK
                bg = colors['bg']['black-dead']
            label = Label(rightPanel,
                          width=dimensions['width']['dead'],
                          height=dimensions['height']['dead'],
                          relief="ridge",
                          bg=bg)
            dead_labels[label_color][(i, j%4)] = DeadLabel(label)
            dead_labels[label_color][(i, j%4)].label.grid(row=i+2, column=9+j, sticky=W)
    msg_label = Label(rightPanel,
                      text="Message:",
                      bg=colors['bg']['main'])
    msg_label.grid(row=6, column=9,pady=(40,10), sticky=W)
    msg_box = Label(rightPanel,
                    text="Welcome to my Chess Game!",
                    width=dimensions['width']['msg-box'],
                    height=dimensions['height']['msg-box'],
                    bd=1,
                    relief="solid",
                    bg=colors['bg']['msg-box'])
    msg_box.grid(row=7, column=9, padx=15, columnspan=8, sticky=W)
            
    

    
root = Tk()
root.wm_title("Chess Game")
root.configure(bg=colors['bg']['main'])
leftPanel = Frame(root, bg=colors['bg']['main'])
leftPanel.pack(side=LEFT)
rightPanel = Frame(root, bg=colors['bg']['main'])
rightPanel.pack(side=RIGHT)
ICONS = {
            WHITE: {
                    Pawn: ImageTk.PhotoImage(Image.open("icons/pawn-white-64.png")),
                    Rook: ImageTk.PhotoImage(Image.open("icons/rook-white-64.png")),
                    Knight: ImageTk.PhotoImage(Image.open("icons/knight-white-64.png")),
                    Bishop: ImageTk.PhotoImage(Image.open("icons/bishop-white-64.png")),
                    King: ImageTk.PhotoImage(Image.open("icons/king-white-64.png")),
                    Queen: ImageTk.PhotoImage(Image.open("icons/queen-white-64.png"))
                    },
            BLACK: {
                    Pawn: ImageTk.PhotoImage(Image.open("icons/pawn-black-64.png")),
                    Rook: ImageTk.PhotoImage(Image.open("icons/rook-black-64.png")),
                    Knight: ImageTk.PhotoImage(Image.open("icons/knight-black-64.png")),
                    Bishop: ImageTk.PhotoImage(Image.open("icons/bishop-black-64.png")),
                    King: ImageTk.PhotoImage(Image.open("icons/king-black-64.png")),
                    Queen: ImageTk.PhotoImage(Image.open("icons/queen-black-64.png"))
                    }
            }
game = Game()
generateChessBoard()
generateAdditionalFeatures()
root.mainloop()
