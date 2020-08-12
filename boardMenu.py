from tkinter import *
from board import board
from negamax import deepAll as m
import role
import Point
import role as R
import requests
import time

# 创建并添加 canvas
# 创建窗口
root = Tk()
root.title("五子棋")
gaird_width = 30
gaird_count = 17

widths = gaird_width*gaird_count + 20
board.init(15)
root.maxsize(widths, widths)
root.minsize(widths, widths)
# 创建并添加Canvas
cv = Canvas(root, background='white')
def cp(x,y):
    p=Point.point
    p.x=x
    p.y=y
    board.put(p,R.com)
def hp(x,y):
    p = Point.point
    p.x=x
    p.y=y
    board.put(p,R.hum)
def cs():
    p = Point.point
    if (len(board.allSteps) > 1):
        s = time.time()
        p = m(R.com, 6)
        print(time.time()-s)
        board.put(p, R.com)
    else:
        p.x=board.currentSteps[0].x+1
        p.y=board.currentSteps[0].y+1
        cp(p.x,p.y)
    if 'score' in p.__dict__:
        return p.x,p.y,p.score
    else:
        return p.x,p.y,0
def back(x,y):
    p = Point.point
    p.x = x
    p.y = y
    board.remove(p)

# 画一个外边框为白的 , 填充棋盘颜色
def init():
    cv.pack(fill=BOTH, expand=YES)
    cv.create_rectangle(10,10,gaird_width*gaird_count + 10,gaird_width*gaird_count + 10,outline="white", fill="#CD8500")

# 在棋盘里面画 画格子
    for num in range(1,gaird_count):
        cv.create_line(num*gaird_width + 10 ,
                       gaird_width + 10,
                       num*gaird_width + 10,
                       gaird_width*(gaird_count-1) + 10,
                       width=2,
                       fill="#595959")
    for num in range(1,gaird_count):
        cv.create_line(gaird_width + 10 ,
                       num*gaird_width + 10,
                       (gaird_count-1)*gaird_width + 10,
                       num*gaird_width + 10,
                       width=2,
                       fill="#595959"
                       )

start = time.time()
def paint(event):
    global start
    start = time.time()
    python_green = "black"
    x: int = int((event.x + 0.5 * gaird_width - 10)/gaird_width);
    y: int = int((event.y + 0.5 * gaird_width - 10)/gaird_width);

    print(x,y)
    hp(x,y)
    x1, y1 = (x*gaird_width ), (y*gaird_width)
    x2, y2 = (x*gaird_width + 20), (y*gaird_width + 20)
    cv.create_oval(x1,y1,x2,y2, fill = python_green)
    x,y,s=cs()
    python_green = "white"
    print(x, y,s)
    x1, y1 = (x * gaird_width), (y * gaird_width)
    x2, y2 = (x * gaird_width + 20), (y * gaird_width + 20)
    cv.create_oval(x1, y1, x2, y2, fill=python_green)
    print(time.time()-start)

def pb(event):
    for i in board.board:
        print(str(i)+',')

def playchess():
    cv.bind("<Button-1>", paint)
    cv.bind("<Button-2>", pb)

def selefdraw():
    cv.bind("<Button-1>", sedraw)
    cv.bind("<Button-2>", pb)
def view():
    cv.bind("<Button-1>", forword)
    cv.bind("<Button-2>", pb)
    cv.bind("<Button-3>", review)
inputChess = 'hhiijhihigjfhfgehehggffgffefkiljghggdgjggjkfleijehfidhfhdjdifjejgiekgkgleicghl'
i = -2
blackTrun = True
def sedraw(event):
    global blackTrun
    if blackTrun:
        python_green = "black"
    else:
        python_green = "white"
    x: int = int((event.x + 0.5 * gaird_width - 10) / gaird_width);
    y: int = int((event.y + 0.5 * gaird_width - 10) / gaird_width);

    print("["+str(x)+","+ str(y)+"],")
    if blackTrun:
        hp(x, y)
    else:
        cp(x,y)
    x1, y1 = (x * gaird_width), (y * gaird_width)
    x2, y2 = (x * gaird_width + 20), (y * gaird_width + 20)
    cv.create_oval(x1, y1, x2, y2, fill=python_green)
    blackTrun = not blackTrun
def toInt(c):
    return ord(c) - ord('a')

def toChar(n):
    return chr(n + ord('a'))

def draw():
    init()

    for x in range(len(board.board)):
        for y in range(len(board.board[x])):
            if board.board[x][y]==R.hum:
                x1, y1 = (x * gaird_width), (y * gaird_width)
                x2, y2 = (x * gaird_width + 20), (y * gaird_width + 20)
                cv.create_oval(x1, y1, x2, y2, fill="black")
            elif board.board[x][y]==R.com:
                x1, y1 = (x * gaird_width), (y * gaird_width)
                x2, y2 = (x * gaird_width + 20), (y * gaird_width + 20)
                cv.create_oval(x1, y1, x2, y2, fill="white")

def review(event):
    global blackTrun
    global i
    print(i)
    back(toInt(inputChess[i]),toInt(inputChess[i + 1]))
    blackTrun = not blackTrun
    draw()
def forword(event):
    global blackTrun
    global i
    i += 2
    print((toInt(inputChess[i]),toInt(inputChess[i + 1])))
    if (blackTrun):
        hp(toInt(inputChess[i]),toInt(inputChess[i + 1]))
    else:
        cp(toInt(inputChess[i]), toInt(inputChess[i + 1]))
    blackTrun = not blackTrun
    draw()
init()
# <Button-1>：鼠标左击事件
# <Button-2>：鼠标中击事件
# <Button-3>：鼠标右击事件
# <Double-Button-1>：双击事件
# <Triple-Button-1>：三击事件
#view()
playchess()
#selefdraw()
message = Label(root, text = "press and drag the mouse to tap")
message.pack(side = BOTTOM)

root.mainloop()