import tkinter as tk
from PIL import Image,ImageTk       # need: pip install pillow
import random

picpath = "1.jpg"

width,height = 200,100
root = tk.Tk()


root.overrideredirect(True)     #隐藏边框和标题

root.attributes("-transparentcolor",'white')    #透明
root.attributes("-topmost",True)                #置顶

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# x = random.randint(0,screen_width-width)        #随机位置
# y = random.randint(0,screen_height-height)

# root.geometry(f"{width}x{height}+{x}+{y}")      #窗口大小

img = Image.open(picpath)
img_width,img_height = 400,200
img = img.resize((width, height), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(img)

label = tk.Label(root,image=photo,bg="white")
label.pack()

label.bind("<Button-1>",lambda e: root.destroy())       #关闭 鼠标左键

is_show = 1
def toggle_show():
    global root
    global is_show
    if is_show:

        x = random.randint(0,screen_width-width)        #随机位置
        y = random.randint(0,screen_height-height)

        root.geometry(f"{width}x{height}+{x}+{y}")

        root.deiconify()    #显示
        is_show=0
    else:
        root.withdraw()     #隐藏
        is_show=1
    
    root.after(50,toggle_show)     #设置定时器,100毫秒后执行

toggle_show()

root.mainloop()


