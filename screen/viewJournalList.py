import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime

import utility as util


class ViewJournalList(tk.Frame):
    def __init__(self, parent, repo, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.repo = repo
        self.parent = parent

        label_font = "arial 12 normal"
        header_font = "arial 12 bold"

        style = ttk.Style()

        style.theme_use("default")
        style.configure("Treeview", background=util.color_light_green, foreground=util.color_black,
                        fieldbackground=util.color_light_green, font=label_font, borderwidth=0, rowheight=40)
        style.map('Treeview', background=[('selected', util.color_dark_green)])

        style.configure("Treeview.Heading", background=util.color_dark_green, foreground=util.color_white,
                        font=header_font, borderwidth=1)

        columns = ('id', 'date', 'debit', 'credit', 'amount', 'narration')
        tree = ttk.Treeview(self.parent, columns=columns, show='headings', selectmode="browse")

        tree.heading('id', text='No.')
        tree.column('id', minwidth=0, width=20)

        tree.heading('date', text='Date')
        tree.column('date', minwidth=0, width=100)

        tree.heading('debit', text='Debit')
        tree.column('debit', minwidth=0, width=100)

        tree.heading('credit', text='Credit')
        tree.column('credit', minwidth=0, width=100)

        tree.heading('amount', text='Amount')
        tree.column('amount', minwidth=0, width=150, anchor="e")

        tree.heading('narration', text='Narration')
        tree.column('narration', minwidth=0, width=300)

        tree.place(x=0, y=0, relwidth=1, relheight=1)

        journals = []
        for j in reversed(repo.journals):

            journals.append(("#" + str(j.id), datetime.fromtimestamp(j.time).strftime('%Y-%m-%d'),
                             j.debit.name.capitalize() + " A/c", j.credit.name.capitalize() + " A/c",
                             util.format_currency(j.amount, repo.meta_data_dict['CURRENCY_FORMAT'],
                                                  repo.meta_data_dict['CURRENCY']),
                             j.narration))

            tree.insert('', tk.END, values=journals[len(journals) - 1])
