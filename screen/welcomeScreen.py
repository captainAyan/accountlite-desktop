import tkinter as tk
from tkinter import *
import webbrowser

import utility as util


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, repo, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.repo = repo
        self.parent = parent

        outer_header = tk.Frame(self.parent, background=util.color_orange, highlightbackground=util.color_red,
                                highlightthickness=1)
        outer_header.place(relx=0.5, rely=0.45, anchor=CENTER, height=360, width=780)

        header = tk.Frame(outer_header, background=outer_header["background"])
        header.place(relx=0.5, rely=0.5, anchor=CENTER)

        head_text = '''Welcome to AccountLite'''
        sub_text = '''Lightweight accounting software mainly focused\ntowards Double-Entry accounting system'''

        tk.Label(header, text=head_text, bg=header["background"], font="arial 32 normal").pack()
        tk.Label(header, text=sub_text, bg=header["background"], font="arial 12 normal").pack()

        link = Label(header, text="Ayan Chakraborty - @CaptainAyan (Github)", fg="blue", cursor="hand2", bg=header["background"])
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/captainAyan"))
