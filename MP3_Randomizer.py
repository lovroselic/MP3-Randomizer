# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 14:13:11 2021

@author: lovro

https://docs.python.org/3/library/dialog.html
https://www.tutorialspoint.com/python/python_gui_programming.htm
https://www.tutorialspoint.com/python/python_gui_programming.htm
"""

import tkinter as tk
import tkinter.filedialog
import os
import os.path
from fnmatch import fnmatch
import pandas as pd

_TITLE = "MP3 Randomizer"
_VERSION = "0.3.0"
_CONFIG_FILE_NAME = "Randomizer.cfg"
_PATTERN = "*.mp3"


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        self.master.minsize(800, 600)
        self.master.wm_title(_TITLE)
        self.fileList = None
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
        actionMenu.add_command(label='Find music', command=self.getFiles)
        actionMenu.add_command(label='Randomize', command=self.notYet)
        actionMenu.add_command(label='Copy to output', command=self.notYet)
        aboutMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=aboutMenu)
        aboutMenu.add_command(label='Help', command=self.notYet)
        aboutMenu.add_separator()
        aboutMenu.add_command(label='About', command=self.about)
        #
        # config
        #
        self._INPUT = tk.StringVar(value='')
        self._OUTPUT = tk.StringVar(value='')
        self._N = tk.StringVar(value='999')
        self._FOUND = tk.StringVar(value='0')
        self.pack()
        self.create_widgets(master)
        self.loadConfig()
        self.info()

    def create_widgets(self, master):
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=50)
        #
        # Frames
        #
        configFrame = tk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        configFrame.pack_propagate(0)
        configFrame.pack(side=tk.LEFT, anchor=tk.NW)
        #
        # Labels
        #
        inpLabel = tk.Label(configFrame, text="Input directory:")
        inpLabel.grid(row=0, column=0, sticky=tk.W)
        outLabel = tk.Label(configFrame, text="Output directory:")
        outLabel.grid(row=1, column=0, sticky=tk.W)
        inpSource = tk.Label(configFrame,
                             text=self._INPUT,
                             textvariable=self._INPUT)
        inpSource.grid(row=0, column=1, sticky=tk.W)
        outSource = tk.Label(configFrame,
                             text=self._OUTPUT,
                             textvariable=self._OUTPUT)
        outSource.grid(row=1, column=1, sticky=tk.W)

        numberLabel = tk.Label(configFrame,
                               text="Number of files:")
        numberLabel.grid(row=2, column=0, sticky=tk.W)
        numberEntry = tk.Entry(configFrame,
                               text=self._N,
                               textvariable=self._N)
        numberEntry.grid(row=2, column=1, sticky=tk.W)

        foundLabel = tk.Label(configFrame, text="Files found:")
        foundLabel.grid(row=3, column=0, sticky=tk.W)
        foundEntry = tk.Label(configFrame,
                              text=self._FOUND,
                              textvariable=self._FOUND)
        foundEntry.grid(row=3, column=1, sticky=tk.W)

    def info(self):
        print("CWD:", os.getcwd())
        print("input:", self._INPUT.get())
        print("output:", self._OUTPUT.get())
        print("N:", self._N.get())
        print("\n")

    def loadConfig(self):
        if os.path.exists(_CONFIG_FILE_NAME):
            with open(_CONFIG_FILE_NAME, 'r') as F:
                data = F.readlines()
            for i, cfg in enumerate([self._INPUT, self._OUTPUT, self._N]):
                cfg.set(data[i].strip('\n'))

    def saveConfig(self):
        with open(_CONFIG_FILE_NAME, 'w') as F:
            for cfg in [self._INPUT, self._OUTPUT, self._N]:
                F.write(cfg.get())
                F.write('\n')

    def setInput(self):
        self._INPUT.set(
            tk.filedialog.askdirectory(initialdir=self._INPUT.get()))

    def setOutput(self):
        self._OUTPUT.set(
            tk.filedialog.askdirectory(initialdir=self._OUTPUT.get()))

    def notYet(self):
        print('not yet implemented')

    def quitApp(self):
        self.master.destroy()

    def about(self):
        tk.messagebox.showinfo(_TITLE,
                               '{}\n v {}\nby Lovro Selic'
                               .format(_TITLE, _VERSION))

    def getFiles(self):
        global DF
        # global TEST
        self.fileList = getAllFiles(self._INPUT.get(), _PATTERN)
        # TEST = self.fileList
        self._FOUND.set(len(self.fileList))
        DF = pd.DataFrame({'path': self.fileList})


def getAllFiles(root, pat):
    files = []
    for path, subdir, file in os.walk(root):
        for name in file:
            if fnmatch(name, pat):
                files.append(os.path.join(path, name))
    return files


global DF
root = tk.Tk()
app = Application(master=root)
app.mainloop()
