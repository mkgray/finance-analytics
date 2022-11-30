from tkinter import Tk, Button, Label, ttk
from tkinter.filedialog import askdirectory

from finance_analytics import FinanceAnalytics

from financeanalytics.dataloader import DataLoader
from financeanalytics.dataquality import DataQuality
from financeanalytics.statementprocessor import StatementProcessor

from pathlib import Path

import logging
from tqdm import tqdm

import pandas as pd

import argparse


root = Tk()
root.title("Finance Analytics")
root.iconbitmap("../assets/icons/finance_analytics_logo.ico")

def get_directory():
    global root_dir
    root_dir = askdirectory(title="Choose Root Folder for Financial Statement Processing")
    label_root_folder.config(text="Root Folder: {}".format(root_dir))

    # Output directory by default is the same as the root directory
    global output_dir
    output_dir = root_dir
    label_output_location.config(text="Output Location: {}/extracted_transactions.xlsx".format(root_dir))

    # Enable output directory choosing and processing functions once input location determined
    #button_choose_out.config(state="normal") # disabled until feature is completed
    button_run.config(state="normal")

def get_output():
    output_dir = askdirectory(title="Choose Output Folder for Storing Processed Results")
    label_output_location.config(text="Output Location: {}/extracted_transactions.xlsx".format(root_dir))

def run_processing():
    FinanceAnalytics(root_dir)

# Initialize Buttons
button_choose_root = Button(root, text="Choose Root Folder", command=get_directory, padx=20)
button_choose_out = Button(root, text="Choose Output Location", command=get_output, state="disabled", padx=7)
button_run = Button(root, text="Run", command=run_processing, state="disabled", padx=15)
button_quit = Button(root, text="Quit", command=root.quit, padx=13)

# Initialize Labels
label_root_folder = Label(root, text="Root Folder: ", anchor="w")
label_output_location = Label(root, text="Output Location: ", anchor="w")

# Initialize Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")

# Place widgets
button_choose_root.grid(row=0, column=0, columnspan=2)
button_choose_out.grid(row=1, column=0, columnspan=2)
button_run.grid(row=2, column=0)
button_quit.grid(row=2, column=4)

label_root_folder.grid(row=0, column=2, columnspan=3)
label_output_location.grid(row=1, column=2, columnspan=3)

progress_bar.grid(row=2, column=1, columnspan=3)

# Run main loop
root.mainloop()