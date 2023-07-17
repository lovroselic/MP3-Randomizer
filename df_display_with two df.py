# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 08:01:47 2023

@author: lovro
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd


def display_dataframe(frame, dataframe):
    # Create a Treeview widget
    treeview = ttk.Treeview(frame)
    treeview.pack(fill='both', expand=True)

    # Configure the Treeview
    treeview['columns'] = list(dataframe.columns)
    treeview['show'] = 'headings'

    # Add column headings
    for column in dataframe.columns:
        treeview.heading(column, text=column)

    # Add data rows
    for row in dataframe.itertuples(index=False):
        treeview.insert('', 'end', values=row)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=treeview.yview)
    scrollbar.pack(side='right', fill='y')
    treeview.configure(yscrollcommand=scrollbar.set)


# Create sample Pandas DataFrames
data1 = {'Name': ['John', 'Emily', 'Ryan', 'Julia'],
         'Age': [25, 28, 32, 29],
         'City': ['New York', 'Chicago', 'San Francisco', 'Los Angeles']}
df1 = pd.DataFrame(data1)

data2 = {'Name': ['Mike', 'Linda', 'Brian', 'Sarah'],
         'Age': [31, 27, 34, 26],
         'City': ['Boston', 'Seattle', 'Denver', 'Austin']}
df2 = pd.DataFrame(data2)

# Create the Tkinter window
window = tk.Tk()
window.title("DataFrame Display")

# Create Frame 1
frame1 = ttk.Frame(window)
frame1.pack(fill='both', expand=True)

# Add a label for Frame 1
label1 = ttk.Label(frame1, text="DataFrame 1")
label1.pack(pady=10)

# Call the function to display DataFrame 1 within Frame 1
display_dataframe(frame1, df1)

# Create Frame 2
frame2 = ttk.Frame(window)
frame2.pack(fill='both', expand=True)

# Add a label for Frame 2
label2 = ttk.Label(frame2, text="DataFrame 2")
label2.pack(pady=10)

# Call the function to display DataFrame 2 within Frame 2
display_dataframe(frame2, df2)

# Start the Tkinter event loop
window.mainloop()
