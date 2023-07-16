# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 14:13:11 2021

@author: lovro

https://docs.python.org/3/library/dialog.html
https://www.tutorialspoint.com/python/python_gui_programming.htm
https://www.tutorialspoint.com/python/python_gui_programming.htm
https://www.youtube.com/playlist?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk
https://docs.python.org/3/library/tk.html
"""

import tkinter as tk
import tkinter.filedialog
import os
import os.path
from fnmatch import fnmatch
import pandas as pd
import shutil
import pandasgui

_TITLE = "MP3 Randomizer"
_VERSION = "0.5.0"
_CONFIG_FILE_NAME = "Randomizer.cfg"
_PATTERN = "*.mp3"
_FILE = "Randomizer.csv"


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
        actionMenu.add_command(label='Save list', command=self.saveList)
        actionMenu.add_command(label='Load list', command=self.loadList)
        actionMenu.add_separator()
        actionMenu.add_command(label='Randomize', command=self.randomizeFiles)
        actionMenu.add_command(label='Copy to output', command=self.copyFiles)
        aboutMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=aboutMenu)
        aboutMenu.add_command(label='Help', command=self.help)
        aboutMenu.add_separator()
        aboutMenu.add_command(label='About', command=self.about)
        #
        # config
        #
        self._INPUT = tk.StringVar(value='')
        self._OUTPUT = tk.StringVar(value='')
        self._N = tk.StringVar(value='999')
        self._FOUND = tk.StringVar(value='0')
        self._SELECTED = tk.StringVar(value='0')
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
                               text="Number of files to copy:\t")
        numberLabel.grid(row=2, column=0, sticky=tk.W)
        numberEntry = tk.Entry(configFrame,
                               text=self._N,
                               textvariable=self._N)
        numberEntry.grid(row=2, column=1, sticky=tk.W)

        foundLabel = tk.Label(configFrame, text="Files found:")
        foundLabel.grid(row=3, column=0, sticky=tk.W)
        foundEntry = tk.Label(configFrame, text=self._FOUND, textvariable=self._FOUND)
        foundEntry.grid(row=3, column=1, sticky=tk.W)

        selectLabel = tk.Label(configFrame, text="Files selected:")
        selectLabel.grid(row=4, column=0, sticky=tk.W)
        selectEntry = tk.Label(configFrame, text=self._SELECTED, textvariable=self._SELECTED)
        selectEntry.grid(row=4, column=1, sticky=tk.W)

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
        tk.messagebox.showinfo("Saved", "Config saved.")

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
        tk.messagebox.showinfo(_TITLE, '{}\n v {}\nby Lovro Selic'.format(_TITLE, _VERSION))

    def getFiles(self):
        global DF
        self.fileList = getAllFiles(self._INPUT.get(), _PATTERN)
        self._FOUND.set(len(self.fileList))
        DF = pd.DataFrame({'Path': self.fileList})
        DF['Filenane'] = DF['Path'].apply(extractFile)
        DF[['Artist', 'Title']] = DF['Filenane'].apply(artistAndTitle).apply(pd.Series)
        column_order = ['Title', 'Artist', 'Filenane', 'Path']
        DF = DF[column_order]
        tk.messagebox.showinfo("Found files", "Found {} mp3".format(len(DF)))

    def randomizeFiles(self):
        global SELECTION
        try:
            N = int(self._N.get())
            SELECTION = DF.sample(n=N)
            # print(SELECTION)
            pandasgui.show(SELECTION)
            self._SELECTED.set(len(SELECTION))
        except Exception as e:
            tk.messagebox.showinfo("Create list first", "File list not yet created.")
            print("An error occurred:", str(e))

    def help(self):
        tk.messagebox.showinfo("Help", "There is no help, sorry.")

    def saveList(self):
        try:
            DF.to_csv(_FILE, index=False)
            tk.messagebox.showinfo("Saved", "List saved.")
        except Exception as e:
            tk.messagebox.showinfo("Create list first", "File list not yet created.")
            print("An error occurred:", str(e))

    def loadList(self):
        global DF
        if os.path.exists(_FILE):
            DF = pd.read_csv(_FILE)
            self.fileList = DF["Path"].tolist()
            self._FOUND.set(len(self.fileList))
        else:
            tk.messagebox.showinfo("List not made", "Saved file list does not exist.")

    def copyFiles(self):
        global SELECTION
        try:
            source_paths = SELECTION['Path'].tolist()
            for path in source_paths:
                filename = path.split('\\')[-1]
                out = self._OUTPUT.get() + '/' + filename
                shutil.copy(path, out)
        except Exception as e:
            tk.messagebox.showinfo("Randomize list first", "Nothing to copy yet. Randomize list first")
            print("An error occurred:", str(e))


def getAllFiles(root, pat):
    files = []
    for path, subdir, file in os.walk(root):
        for name in file:
            if fnmatch(name, pat):
                files.append(os.path.join(path, name))
    return files


def extractFile(x):
    f = x.split('\\')[-1]
    return f.split('.')[0]


def artistAndTitle(x):
    temp = x.split(' - ')
    a = temp[-1].strip()
    t = temp[0].strip()
    return a, t


global DF
root = tk.Tk()
app = Application(master=root)
app.mainloop()
