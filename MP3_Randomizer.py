# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 14:13:11 2021

@author: lovro

https://docs.python.org/3/library/dialog.html
https://www.tutorialspoint.com/python/python_gui_programming.htm
https://www.tutorialspoint.com/python/python_gui_programming.htm
"""

import tkinter as tk
import os
import os.path

_TITLE = "MP3 Randomizer"
_VERSION = "0.1.3"
_CONFIG_FILE_NAME = "Randomizer.cfg"


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        self.master.minsize(640, 400)
        #
        # menus
        #
        setupMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Setup", menu=setupMenu)
        setupMenu.add_command(label="Set input folder",
                              command=self.setInput)
        setupMenu.add_command(label="Set output folder",
                              command=self.setOutput)
        setupMenu.add_separator()
        setupMenu.add_command(label="Save config", command=self.saveConfig)
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
        self.create_widgets()
        #
        # config
        #
        self.__INPUT = None
        self.__OUTPUT = None
        self.loadConfig()
        self.pack()
        self.info()

    def create_widgets(self):
        #
        # Frames
        #
        configFrame = tk.Frame(self.master, width=400, height=100, bg='black')
        configFrame.pack_propagate(0)
        configFrame.pack(side=tk.TOP, anchor=tk.NW)
        #
        # Labels
        #
        inpLabel = tk.Label(configFrame, text="Input directory:", bg='white')
        inpLabel.grid(row=0, column=0, sticky=tk.W)
        outLabel = tk.Label(configFrame, text="Output directory:", bg='white')
        outLabel.grid(row=1, column=0, sticky=tk.W)
        inpSource = tk.Label(configFrame, text="C:/", bg='white')
        inpSource.grid(row=0, column=1, sticky=tk.W)
        outSource = tk.Label(configFrame, text="D:/", bg='white')
        outSource.grid(row=1, column=1, sticky=tk.W)
        # inpLabel.pack(side=tk.TOP, anchor=tk.NW)
        return

    def info(self):
        print("CWD:", os.getcwd())
        print("input:", self.__INPUT)
        print("output", self.__OUTPUT)
        print("\n")

    def loadConfig(self):
        if os.path.exists(_CONFIG_FILE_NAME):
            print("....")
            with open(_CONFIG_FILE_NAME, 'r') as F:
                data = F.readlines()
            [self.__INPUT, self.__OUTPUT] = data

    def saveConfig(self):
        print('\nsaving config in dir:', os.getcwd())
        with open(_CONFIG_FILE_NAME, 'w') as F:
            for cfg in [self.__INPUT, self.__OUTPUT]:
                print(cfg)
                cfg = cfg or ""
                F.write(cfg)
                F.write('\n')

    def setInput(self):
        self.__INPUT = tk.filedialog.askdirectory()
        print("setting input:", self.__INPUT)

    def setOutput(self):
        self.__OUTPUT = tk.filedialog.askdirectory()
        print("setting output:", self.__OUTPUT)

    def notYet(self):
        print('not yet implemented')

    def quitApp(self):
        self.master.destroy()

    def about(self):
        tk.messagebox.showinfo(_TITLE,
                               '{}\n v {}\nby Lovro Selic'
                               .format(_TITLE, _VERSION))


root = tk.Tk()
app = Application(master=root)
root.wm_title(_TITLE)
app.mainloop()
