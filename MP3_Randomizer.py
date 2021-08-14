# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 14:13:11 2021

@author: lovro
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

_TITLE = "MP3 Randomizer"
_VERSION = "0.1.0"


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        # menus
        setupMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Setup", menu=setupMenu)
        setupMenu.add_command(label="Set input folder",
                              command=self.setInput)
        setupMenu.add_command(label="Set output folder",
                              command=self.setOutput)
        setupMenu.add_separator()
        setupMenu.add_command(label="Quit",
                              command=self.quitApp)
        actionMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Action", menu=actionMenu)
        actionMenu.add_command(label='Find music', command=self.notYet)
        actionMenu.add_command(label='Randomize', command=self.notYet)
        actionMenu.add_command(label='Copy to output', command=self.notYet)
        aboutMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=aboutMenu)
        aboutMenu.add_command(label='Help', command=self.notYet)
        aboutMenu.add_separator()
        aboutMenu.add_command(label='About', command=self.about)
        # self.pack()
        # self.create_widgets()

    def create_widgets(self):
        pass

    def setInput(self):
        print("setting input")

    def setOutput(self):
        print("setting output")

    def notYet(self):
        print('not yet implemented')

    def quitApp(self):
        self.master.destroy()

    def about(self):
        messagebox.showinfo(_TITLE,
                            '{}\n v {}\nby Lovro Selic'
                            .format(_TITLE, _VERSION))


root = tk.Tk()
app = Application(master=root)
root.wm_title(_TITLE)
app.mainloop()
