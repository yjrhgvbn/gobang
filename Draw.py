from tkinter import *
import role as R
def d(b):
    root = Tk()
    root.title("五子棋")
    gaird_width = 30
    gaird_count = 17

    widths = gaird_width * gaird_count + 20

    root.maxsize(widths, widths)
    root.minsize(widths, widths)
    # 创建并添加Canvas
    cv = Canvas(root, background='white')
    cv.pack(fill=BOTH, expand=YES)
    cv.create_rectangle(10, 10, gaird_width * gaird_count + 10, gaird_width * gaird_count + 10, outline="white",
                        fill="#CD8500")
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
    for x in range(len(b)):
        for y in range(len(b[x])):
            if b[y][x]==R.hum:
                x1, y1 = (x * gaird_width), (y * gaird_width)
                x2, y2 = (x * gaird_width + 20), (y * gaird_width + 20)
                cv.create_oval(x1, y1, x2, y2, fill="black")
            elif b[y][x]==R.com:
                x1, y1 = (x * gaird_width), (y * gaird_width)
                x2, y2 = (x * gaird_width + 20), (y * gaird_width + 20)
                cv.create_oval(x1, y1, x2, y2, fill="white")

    message = Label(root, text="press and drag the mouse to tap")
    message.pack(side=BOTTOM)

    root.mainloop()