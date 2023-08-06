from tkinter.ttk import *
from tkinter import messagebox as box
import ttk_themes

def func():
    data = entry.get()
    messagebox.showinfo("", data)

window = ttk_themes.themed_tk('radiance')

frame = Frame(window)
frame.pack()

entry = Entry(frame)
entry.pack()

button = Button(text="Go", command=func)
button.pack()

if __name__ == '__main__':
    window.mainloop()