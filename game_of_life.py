from random import sample, random
from tkinter import Tk, Canvas, Scale, Button, Label, N, ALL
import copy

def grid_init(p):
    map=[(row,col) for col in range(n_col) for row in range(n_row)]
    cells_number=int(n_row*n_col*p)
    cells=sample(map,cells_number)
    states = [[0] * n_col for _ in range(n_row)]
    for (i,j) in cells:
        states[i][j]=1
    return states

def neighbors(i, j):
    return [(a,b) for (a, b) in
            [(i, j+1),(i, j-1), (i-1, j), (i+1,j),
             (i+1, j+1), (i+1, j-1), (i-1, j+1), (i-1, j-1)]
            if a in range(n_row) and b in range(n_col)]

def neighbors_number_alive(states, i, j):
    return sum(states[a][b] for (a, b) in neighbors(i, j))

def fill_cell(states, row, col):
        A=(unit*col, unit*row)
        B=(unit*(col+1), unit*(row+1))
        state=states[row][col]
        color=COLORS[state]
        cnv.create_rectangle(A, B, fill=color, outline='')

def fill(states):
    for row in range(n_row):
        for col in range(n_col):
            fill_cell(states, row, col)

def upgrade_grid(states):
    new_states = copy.deepcopy(states)
    for row in range(n_row):
        for col in range(n_col):
            if states[row][col] == 0:
                if neighbors_number_alive(states, row, col) == 3:
                    new_states[row][col] = 1
            else:
                if neighbors_number_alive(states, row, col) not in [2, 3]:
                    new_states[row][col] = 0
    states[:] = new_states[:]

def init():
    global states, is_running
    is_running=False
    p=int(curseur.get())/100
    curseur["state"]='normal'
    states=grid_init(p)
    cnv.delete(ALL)
    fill(states)

def run():
    global is_running
    if is_running:
        upgrade_grid(states)
        cnv.delete(ALL)
        fill(states)
        cnv.after(100, run)

def start_cell(event):
    global is_running
    i, j = event.y//unit, event.x//unit
    if states[i][j] == 0:
        states[i][j] = 1
        fill_cell(states, i, j)

def start():
    global is_running
    is_running=True
    curseur["state"]='disabled'
    run()

def stop():
    global is_running
    is_running=False

def new_density(states, p):
    n=len(states)
    cells= [(i,j) for i in range(n_row) for j in range(n_col) if states[i][j]==1]
    no_cell=[(i,j) for i in range(n_row) for j in range(n_col) if states[i][j]==0]
    new_cells=int(n_row*n_col*p)
    before=len(cells)
    delta=abs(new_cells-before)
    if new_cells>=before:
        for (i, j) in sample(no_cell, delta):
            states[i][j]=1
    else:
        for (i, j) in sample(cells, delta):
            states[i][j]=0

def random_start(percent):
    cnv.delete("all")
    p=float(percent)/100
    n_cell=int(n_col*n_row*p)
    new_density(states,p)
    fill(states)

# ------------------ Settings ------------------

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
titlebar_height = root.winfo_height() - root.winfo_reqheight()
root.geometry("%dx%d+0+0" % (screen_width, screen_height - titlebar_height))
root.attributes('-topmost', True)
root.title("Conway's Game of Life")

n_col = 135
n_row = 100
unit = screen_height//n_row
COLORS = ["white", "black"]

# ------------------ Main ------------------

cnv = Canvas(root, width=unit*n_col-2, height=unit*n_row-2, background="ivory")
cnv.grid(row=0, column=0, rowspan=100)

button1=Button(root,text="New",  font='Arial 15 bold',\
            command=init, width=8)
button1.grid(row=0, column=1, sticky=N)

button2=Button(root,text="Start",  font='Arial 15 bold',\
               command=start, width=8)
button2.grid(row=1, column=1, sticky=N)

curseur = Scale(root, orient = "vertical", command=random_start, from_=100,
      to=0, length=200, tickinterval= 25,  label='Density')
curseur.set(10)
curseur.grid(row=2, column=1, sticky=N, pady=100)

label1=Label(root,text="You can put density to 0 and",  font='Arial 6 bold', width=30)
label1.grid(row=3, column=1, sticky=N)
label2=Label(root,text="click to add your own config",  font='Arial 6 bold', width=30)
label2.grid(row=4, column=1, sticky=N)

cnv.bind("<Button-1>", start_cell)

init()

root.mainloop()