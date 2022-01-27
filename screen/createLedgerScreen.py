import tkinter as tk
from tkinter import *

import utility as util


class CreateLedgerScreen(tk.Frame):
    def __init__(self, parent, repo, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.repo = repo
        self.parent = parent

        label_font = "arial 12 normal"

        self.ledger_name = StringVar()

        # name
        tk.Label(self.parent, text="Ledger Name ", bg=self.parent["background"], font=label_font).place(x=20, y=30)
        self.name_entry = tk.Entry(self.parent, borderwidth=0, bg=util.color_black, fg=util.color_white,
                                   font=label_font, insertbackground=util.color_white, textvariable=self.ledger_name)
        self.name_entry.place(x=128, y=30, width=200, height=24)
        self.name_entry.focus()

        # type
        tk.Label(self.parent, text="Ledger Type ", bg=self.parent["background"], font=label_font).place(x=20, y=70)
        self.type_list_box = tk.Listbox(self.parent, background=util.color_light_green, borderwidth=0,
                                        highlightthickness=0, font=label_font, selectbackground=util.color_dark_green)
        self.type_list_box.place(x=128, y=70, width=200, height=100)

        self.type_list_box.insert(0, "Revenue")
        self.type_list_box.insert(1, "Expenditure")
        self.type_list_box.insert(2, "Asset")
        self.type_list_box.insert(3, "Liability")
        self.type_list_box.insert(4, "Equity")

        # events
        self.name_entry.bind("<Tab>", lambda event: 'break')
        self.name_entry.bind("<Return>", lambda event: self.type_list_box.focus())
        self.name_entry.bind("<Escape>", lambda event: self.ledger_name.set(""))

        self.type_list_box.bind("<Tab>", lambda event: 'break')
        self.type_list_box.bind("<Return>", lambda event: self.submit())
        self.type_list_box.bind("<Escape>", lambda event: self.name_entry.focus())

    def submit(self):

        for l in self.repo.ledgers:
            if l.name == self.ledger_name.get().strip():
                modal = util.Modal(self.parent, "Ledger already exists.", util.Modal.TYPE_ALERT)
                modal.set_positive(lambda: self.rectify_error(modal, self.name_entry))
                return

        if self.ledger_name.get().strip() == "":
            modal = util.Modal(self.parent, "Invalid ledger name.", util.Modal.TYPE_ALERT)
            modal.set_positive(lambda: self.rectify_error(modal, self.name_entry))
            return

        modal = util.Modal(self.parent, "Are you sure about creating the ledger ?", util.Modal.TYPE_QUESTION)
        modal.set_positive(lambda: self.create_ledger(modal))
        modal.set_negative(lambda: self.rectify_error(modal, self.name_entry))

    def rectify_error(self, modal, widget):
        widget.focus()
        modal.destroy()

    def create_ledger(self, modal):

        try:
            self.repo.add_ledger(self.ledger_name.get(), self.type_list_box.curselection()[0])

        except IndexError:
            self.repo.add_ledger(self.ledger_name.get(), 0)

        modal.destroy()
        self.ledger_name.set("")
        self.name_entry.focus()
