from tkinter import filedialog, Text
import tkinter as tk
import os

def SayNope(num):
    counter = 0
    for x in range(200):
        counter = counter +1
        window = tk.Tk()
        window.title(str(counter) +". Hahahaha")
        canvas = tk.Canvas(window, height=25, width=300)
        canvas.pack()
        d = tk.Label(window, text=  "HAHAHAHAHAHAHA!!!! Your os is hacked")
        d.pack()

def Virus():
    root = tk.Tk()
    root.title("Alert")

    w = tk.Label(root, text="Your files are encrypted as requested.")
    w.pack()

    openFile = tk.Button(root, text="undo", padx=10, pady=5, bg="#263D42", command=SayNope)
    openFile.pack()


    canvas = tk.Canvas(root, height=200, width=300)
    canvas.pack()

    root.mainloop()

Virus()