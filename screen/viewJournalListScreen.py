import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta

import utility as util


class ViewJournalListScreen(tk.Frame):
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
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings', selectmode="browse")

        self.tree.heading('id', text='No.')
        self.tree.column('id', minwidth=0, width=60, stretch=NO)

        self.tree.heading('date', text='Date')
        self.tree.column('date', minwidth=0, width=100, stretch=NO)

        self.tree.heading('debit', text='Debit')
        self.tree.column('debit', minwidth=0, width=200, stretch=NO)

        self.tree.heading('credit', text='Credit')
        self.tree.column('credit', minwidth=0, width=200, stretch=NO)

        self.tree.heading('amount', text='Amount')
        self.tree.column('amount', minwidth=0, width=150, anchor="e", stretch=NO)

        self.tree.heading('narration', text='Narration')
        self.tree.column('narration', minwidth=0, width=300)

        self.tree.place(x=0, y=0, relwidth=1, relheight=1)

        self.tree.pack(anchor=N, fill=BOTH, expand=True, side=BOTTOM)

        filter_frame = Frame(self.parent, bg=util.color_yellow, height=66)
        filter_frame.pack(anchor=N, fill=X, expand=False, side=TOP)

        self.from_date = StringVar(value=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))

        tk.Label(filter_frame, text="From Date ", bg=filter_frame["background"], font=label_font) \
            .place(x=10, y=10)
        self.from_date_entry = tk.Entry(filter_frame, textvariable=self.from_date, bg=util.color_black,
                                        fg=util.color_white, font=header_font, insertbackground=util.color_white)
        self.from_date_entry.place(x=128, y=10)

        self.to_date = StringVar(value=(datetime.now()).strftime("%Y-%m-%d"))

        tk.Label(filter_frame, text="To Date ", bg=filter_frame["background"], font=label_font) \
            .place(x=10, y=34)
        self.to_date_entry = tk.Entry(filter_frame, textvariable=self.to_date, bg=util.color_black,
                                      fg=util.color_white, font=header_font, insertbackground=util.color_white)
        self.to_date_entry.place(x=128, y=34)

        self.from_date_entry.focus()
        self.from_date_entry.bind('<Return>', lambda event: self.to_date_entry.focus())

        self.to_date_entry.bind('<Escape>', lambda event: self.from_date_entry.focus())
        self.to_date_entry.bind('<Return>', lambda event: self.render_journal_list())

    def render_journal_list(self):
        self.tree.delete(*self.tree.get_children())

        try:
            from_date = datetime.strptime(self.from_date.get(), '%Y-%m-%d')
        except ValueError:
            modal = util.Modal(self.parent, "'From Date' date is not formatted correctly.", util.Modal.TYPE_ALERT)
            modal.set_positive(lambda: self.rectify_error(modal, self.from_date_entry))
            return

        try:
            to_date = datetime.strptime(self.to_date.get(), '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        except ValueError:
            modal = util.Modal(self.parent, "'To Date' is not formatted correctly.", util.Modal.TYPE_ALERT)
            modal.set_positive(lambda: self.rectify_error(modal, self.to_date_entry))
            return

        journals = []
        for j in reversed(self.repo.journals):

            if from_date.timestamp() <= j.time < to_date.timestamp():
                journals.append(("#" + str(j.id), datetime.fromtimestamp(j.time).strftime('%Y-%m-%d'),
                                 j.debit.name.capitalize() + " A/c", j.credit.name.capitalize() + " A/c",
                                 util.format_currency(j.amount, self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                      self.repo.meta_data_dict['CURRENCY']),
                                 j.narration))

                self.tree.insert('', tk.END, values=journals[len(journals) - 1])

    def rectify_error(self, modal, widget):
        widget.focus()
        modal.destroy()
