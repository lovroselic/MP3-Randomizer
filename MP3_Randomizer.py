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
from tkinter import ttk
import os
import os.path
from fnmatch import fnmatch
import pandas as pd
import shutil
import threading
import pandasgui

_TITLE = "MP3 Randomizer"
_VERSION = "0.9.1"
_CONFIG_FILE_NAME = "Randomizer.cfg"
_PATTERN = "*.mp3"
_FILE = "Randomizer.csv"


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        self.master.minsize(1920, 1024)
        self.master.wm_title(_TITLE)
        self.fileList = None
        self.frame1 = None
        self.frame2 = None
        self.frame3 = None
        #
        # menus
        #
        setupMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Setup", menu=setupMenu)
        setupMenu.add_command(label="Set input folder", command=self.setInput)
        setupMenu.add_command(label="Set output folder", command=self.setOutput)
        setupMenu.add_separator()
        setupMenu.add_command(label="Save config", command=self.saveConfig)
        setupMenu.add_separator()
        setupMenu.add_command(label="Quit", command=self.quitApp)
        actionMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Action", menu=actionMenu)
        actionMenu.add_command(label='Find music', command=self.getFiles)
        actionMenu.add_command(label='Save list', command=self.saveList)
        actionMenu.add_command(label='Load list', command=self.loadList)
        actionMenu.add_separator()
        actionMenu.add_command(label='Randomize', command=self.randomizeFiles)
        # actionMenu.add_command(label='Analyze', command=self.analyze)
        actionMenu.add_separator()
        actionMenu.add_command(label='Copy to output', command=self.startCopy)
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
        self.progress_window = None
        self.progress_bar = None
        self.pack()
        self.create_widgets(master)
        self.loadConfig()
        self.info()
        self.loadList()

    def create_widgets(self, master):
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=50)
        #
        # Frames
        #
        configLabelFrame = tk.LabelFrame(self.master, text="Configuration")
        configLabelFrame.pack(side=tk.TOP, anchor=tk.CENTER, padx=10, pady=10)
        configFrame = tk.Frame(configLabelFrame, borderwidth=2, relief=tk.SUNKEN)
        configFrame.pack_propagate(0)
        configFrame.pack(side=tk.TOP, anchor=tk.NW, fill='both', expand=True)
        #
        # Labels
        #
        inpLabel = tk.Label(configFrame, text="Input directory:")
        inpLabel.grid(row=0, column=0, sticky=tk.W)
        outLabel = tk.Label(configFrame, text="Output directory:")
        outLabel.grid(row=1, column=0, sticky=tk.W)
        inpSource = tk.Label(configFrame, text=self._INPUT, textvariable=self._INPUT)
        inpSource.grid(row=0, column=1, sticky=tk.W)
        outSource = tk.Label(configFrame, text=self._OUTPUT, textvariable=self._OUTPUT)
        outSource.grid(row=1, column=1, sticky=tk.W)

        numberLabel = tk.Label(configFrame, text="Number of files to copy:\t")
        numberLabel.grid(row=2, column=0, sticky=tk.W)
        numberEntry = tk.Entry(configFrame, text=self._N, textvariable=self._N)
        numberEntry.grid(row=2, column=1, sticky=tk.W)

        foundLabel = tk.Label(configFrame, text="Files found:")
        foundLabel.grid(row=3, column=0, sticky=tk.W)
        foundEntry = tk.Label(configFrame, text=self._FOUND, textvariable=self._FOUND)
        foundEntry.grid(row=3, column=1, sticky=tk.W)

        selectLabel = tk.Label(configFrame, text="Files selected:")
        selectLabel.grid(row=4, column=0, sticky=tk.W)
        selectEntry = tk.Label(configFrame, text=self._SELECTED, textvariable=self._SELECTED)
        selectEntry.grid(row=4, column=1, sticky=tk.W)
        #
        # dataframe frames
        #
        frame1LabelFrame = tk.LabelFrame(self.master, text="Files available")
        frame1LabelFrame.pack(fill='both', expand=True, padx=10, pady=10, side=tk.TOP)
        self.frame1 = ttk.Frame(frame1LabelFrame, borderwidth=2, relief=tk.SUNKEN)
        self.frame1.pack(fill='both', expand=True)

        frame2LabelFrame = tk.LabelFrame(self.master, text="Selection")
        frame2LabelFrame.pack(fill='both', expand=True, padx=10, pady=10, side=tk.TOP)
        self.frame2 = ttk.Frame(frame2LabelFrame, borderwidth=2, relief=tk.SUNKEN)
        self.frame2.pack(fill='both', expand=True)

        frame3LabelFrame = tk.LabelFrame(self.master, text="Top 10 Artist selected")
        frame3LabelFrame.pack(fill='both', expand=True, padx=10, pady=10, side=tk.TOP)
        self.frame3 = ttk.Frame(frame3LabelFrame, borderwidth=2, relief=tk.SUNKEN)
        self.frame3.pack(fill='both', expand=True)

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
        global TOP
        try:
            N = int(self._N.get())
            SELECTION = DF.sample(n=N)
            # pandasgui.show(SELECTION)
            self._SELECTED.set(len(SELECTION))
            display_dataframe(self.frame2, SELECTION)
            TOP = top_artists_by_count(SELECTION)
            display_dataframe(self.frame3, TOP)
        except Exception as e:
            tk.messagebox.showinfo("Create list first", "File list not yet created.")
            print("An error occurred:", str(e))

    def analyze(self):
        global SELECTION
        try:
            pandasgui.show(SELECTION)
        except Exception as e:
            tk.messagebox.showinfo("No selection", "Randomize selection first")
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
            display_dataframe(self.frame1, DF)
        else:
            tk.messagebox.showinfo("List not made", "Saved file list does not exist.")

    def startCopy(self):
        self.progress_window = tk.Toplevel(self.master)
        self.progress_window.title("File Copy Progress")
        self.progress_window.geometry("300x100")
        self.progress_bar = ttk.Progressbar(self.progress_window, mode='determinate')
        self.progress_bar.pack(padx=10, pady=10)
        threading.Thread(target=self.copyFiles).start()

    def copyFiles(self):
        global SELECTION
        try:
            source_paths = SELECTION['Path'].tolist()
            total_files = len(source_paths)
            for i, path in enumerate(source_paths, start=1):
                filename = path.split('\\')[-1]
                out = self._OUTPUT.get() + '/' + filename
                shutil.copy(path, out)
                self.updateProgress(i, total_files)
            self.progress_window.destroy()
            tk.messagebox.showinfo("Copy Complete", "Files copied successfully.")
        except Exception as e:
            tk.messagebox.showinfo("Randomize list first", "Nothing to copy yet. Randomize list first")
            print("An error occurred:", str(e))

    def updateProgress(self, current, total):
        self.progress_bar['value'] = current
        self.progress_bar['maximum'] = total
        self.progress_window.update()


def getAllFiles(root, pat):
    files = []
    for path, subdir, file in os.walk(root):
        for name in file:
            if fnmatch(name, pat):
                files.append(os.path.join(path, name))
    return files


def extractFile(x):
    filename_with_extension = os.path.basename(x)
    filename_without_extension = os.path.splitext(filename_with_extension)[0]
    return filename_without_extension


def artistAndTitle(x):
    temp = x.split(' - ')
    a = temp[-1].strip()
    t = temp[0].strip()
    return a, t


def display_dataframe(frame, dataframe):
    for child in frame.winfo_children():
        child.destroy()

    treeview = ttk.Treeview(frame)
    treeview.pack(fill='both', expand=True)
    treeview['columns'] = list(dataframe.columns)
    treeview['show'] = 'headings'

    for column in dataframe.columns:
        treeview.heading(column, text=column)
    for row in dataframe.itertuples(index=False):
        treeview.insert('', 'end', values=row)

    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=treeview.yview)
    scrollbar.pack(side='right', fill='y')
    treeview.configure(yscrollcommand=scrollbar.set)


def top_artists_by_count(dataframe, n=10):
    artist_counts = dataframe['Artist'].value_counts().head(n)
    top_artists_df = pd.DataFrame({'Artist': artist_counts.index, 'Count': artist_counts.values})
    return top_artists_df


global DF
root = tk.Tk()
app = Application(master=root)
app.mainloop()
