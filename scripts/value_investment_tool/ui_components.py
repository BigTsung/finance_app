import tkinter as tk
from tkinter import ttk

def create_label(frame, text, row, column=0, columnspan=1, sticky="w", padx=5, pady=5):
    """Helper function to create a label in the given frame."""
    tk.Label(frame, text=text, anchor="w").grid(row=row, column=column, columnspan=columnspan, sticky=sticky, padx=padx, pady=pady)

def create_separator(frame, row, columnspan=2, pady=5):
    """Helper function to create a separator in the given frame."""
    ttk.Separator(frame, orient="horizontal").grid(row=row, column=0, columnspan=columnspan, sticky="ew", pady=pady)
