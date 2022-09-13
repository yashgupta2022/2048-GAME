
#=========================================================================================
#                                    GAME LOGIC
#=========================================================================================
import random
score = 0

def start_game():
    return [[0 for i in range (4)]for j in range(4)]

def add_random_tile(mat):
    i = random.randint(0,3)
    j = random.randint(0,3)
    while mat[i][j]!=0:
        i = random.randint(0,3)
        j = random.randint(0,3)
    mat[i][j]= 2
    return

def current_status(mat):
    #GAME WON
    for i in range(4):
        for j in range(4):
            if mat[i][j]==2048:
                return 1
    
    #GAME LEFT - IF ANY CELLS ARE EMPTY
    for i in range(4):
        for j in range(4):
            if mat[i][j]== 0:
                return 0
    #GAME LEFT - ALL CELLS ARE FILLED
    #If any cell has identical cell in next row
    for i in range(3):
        for j in range(4):
            if mat[i][j]== mat[i+1][j]:
                return 0
    #If any cell has identical cell in next column
    for i in range(4):
        for j in range(3):
            if mat[i][j]== mat[i][j+1]:
                return 0   
    #GAME OVER
    return -1

#FUNCTIONS FOR MOVES
def compress(mat):
    isChanged =False
    compressed_Mat = []
    for i in range(4):
        x=0
        compressed_Mat.append([0]*4)
        for j in range(4):
            if mat[i][j]!=0:
                compressed_Mat[i][x] = mat[i][j]
                if j!=x: #Cell is Moved => Changed
                    isChanged = True
                x+=1
    return compressed_Mat,isChanged

def merge(mat):
    global score
    isChanged=False
    for i in range(4):
        for j in range(3):
            if mat[i][j]==mat[i][j+1] and mat[i][j]!=0:
                mat[i][j] = mat[i][j] + mat[i][j+1]
                score +=mat[i][j]
                mat[i][j+1] = 0
                isChanged = True # Merger => Change
    return mat,isChanged

def reverse(mat):
    reverse_Mat=[]
    for i in range(4):
        reverse_Mat.append([])
        for j in range(4):
            reverse_Mat[i].append(mat[i][3-j])
    return reverse_Mat

def transpose(mat):
    transpose_Mat=[]
   
    for i in range(4):
        transpose_Mat.append([])
        for j in range(4):
            transpose_Mat[i].append(mat[j][i])
    return transpose_Mat

#ALL MOVES
def move_left(mat):
    mat,bool1 = compress(mat)
    mat,bool2 = merge(mat)
    mat,bool3 = compress(mat)
    isChanged = bool1 or bool2 or bool3
    return mat,isChanged

def move_right(mat):
    mat = reverse(mat)
    mat,isChanged = move_left(mat)
    mat = reverse(mat)
    return mat,isChanged

def move_up(mat):
    mat = transpose(mat)
    mat,isChanged = move_left(mat)
    mat = transpose(mat)
    return mat,isChanged

def move_down(mat):
    mat = transpose(mat)
    mat,isChanged = move_right(mat)
    mat = transpose(mat)
    return mat,isChanged

#=========================================================================================
#                                    COLORS AND FONT
#=========================================================================================
Game_BGC = "#92877d"
Empty_Cell_BGC = "#9e948a"

Cell_BGC = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                         16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                         128: "#edcf72", 256: "#edcc61", 512: "#edc850",
                         1024: "#edc53f", 2048: "#edc22e"}

Cell_Text_Color = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2",
                   256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2",
                   2048: "#f9f6f2"}

FONT = ("Verdana", 40, "bold")

#=========================================================================================
#                                    User Interface - Tkinter
#=========================================================================================
from tkinter import Frame, Label, CENTER,Button,messagebox

class Game2048(Frame):
    def __init__(self):
        Frame.__init__(self) #Frame of UI

        self.grid() #Create grid
        self.master.title('2048') 
        self.master.bind("<Left>", self.key_press)
        self.master.bind("<Right>", self.key_press)
        self.master.bind("<Up>", self.key_press)
        self.master.bind("<Down>", self.key_press)
        self.commands ={37 : move_left,38: move_up ,39: move_right, 40: move_down}

        
        self.grid_cells = []
        self.init_game()
        self.init_matrix()

        self.update_grid_cells() # cell bgc and text color

        self.mainloop() #runs the UI
    
    def init_game(self):

        background = Frame(self, bg=Game_BGC,
                           width=400, height=400)
        background.grid()
        
        #RESET BUTTON
        reset_btn =Button(background,text="RESET",fg="black",bg=Cell_BGC[2],font = ("Verdana", 15, "bold"),
                justify=CENTER, width=10, height=2,command=self.reset)
        reset_btn.grid(row=0,column=0,padx=10,pady=10)

        #EXIT BUTTON
        exit_btn = Button(background, text="EXIT",fg="black",bg=Cell_BGC[2],font = ("Verdana", 15, "bold"),
                justify=CENTER, width=10, height=2, command=self.close)
        exit_btn.grid(row=0,column=1,padx=10,pady=10)

        #SCORE DISPLAY
        global label1
        label1 = Label(background, text="SCORE : "+str(score),fg="red",bg=Cell_BGC[2],font = ("Verdana", 15, "bold"),
                justify=CENTER, width=15, height=2)
        label1.grid(row=0,column=3,padx=10,pady=10)

        
        for i in range(1,5):
            row = []
            for j in range(4):
                cell = Frame(background,bg=Empty_Cell_BGC,
                             width=100, height=100)
                cell.grid(row=i, column=j, 
                          padx=10,pady=10)
                label = Label(master=cell, text="",
                          bg=Empty_Cell_BGC,
                          justify=CENTER, font=FONT, width=5, height=2)
                label.grid()
                row.append(label)

            self.grid_cells.append(row)
        
    def init_matrix(self):
        self.matrix = start_game()
        add_random_tile(self.matrix)
        add_random_tile(self.matrix)

    def update_grid_cells(self):
        label1.config(text="SCORE : "+str(score))
        for i in range(4):
            for j in range(4):
                new = self.matrix[i][j]
                if new == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=Empty_Cell_BGC)
                else:
                    self.grid_cells[i][j].configure(text=str(new),
                            bg=Cell_BGC[new],fg=Cell_Text_Color[new])
        
        self.update_idletasks()

    def reset(self):
        self.init_matrix()
        self.update_grid_cells()

    def close(self):
        self.quit()

    def key_press(self, event):
        key = (event.keycode)
        if key in self.commands:
            self.matrix, changed = self.commands[key](self.matrix)
            if changed:
                add_random_tile(self.matrix)
                self.update_grid_cells()
                changed = False
                if current_status(self.matrix) == 1:
                    res=messagebox.askokcancel("GAME OVER", "YOU WIN\nDo You Want to RETRY")
                    if res==True:
                        self.reset()
                    else:
                        self.close()
                    
                if current_status(self.matrix) == -1:
                    res=messagebox.askokcancel("GAME OVER", "YOU LOST\nDo You Want to RETRY")
                    if res==True:
                        self.reset()
                    else:
                        self.close()
                        
#=========================================================================================
play = Game2048()
#=========================================================================================
    
