import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta

import utility as util


class EditLedgerScreen(tk.Frame):
    def __init__(self, parent, repo, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.repo = repo
        self.parent = parent

        self.selected_ledger_index = 0

        label_font = "arial 12 normal"
        header_font = "arial 12 bold"

        # ledger selection list
        ledger_list_frame = tk.Frame(self.parent, bg=util.color_light_green, width=180)
        ledger_list_frame.pack(expand=False, fill='y', side='right', anchor='nw')

        tk.Label(ledger_list_frame, text="LEDGER LIST", justify=CENTER, bg=util.color_dark_green, fg=util.color_white,
                 font="arial 10 bold").place(x=0, y=0, relwidth=1)
        self.ledger_list_box = tk.Listbox(ledger_list_frame, background=ledger_list_frame["background"], borderwidth=0,
                                          highlightthickness=0, font=label_font, selectbackground=util.color_dark_green)
        self.ledger_list_box.place(x=0, y=20, relwidth=1, relheight=0.9)

        for l in self.repo.ledgers:
            self.ledger_list_box.insert(l.id, l.name)

        # main area
        self.mainarea = tk.Frame(self.parent, bg=parent["background"])
        self.mainarea.pack(expand=True, fill='both', side='right', anchor='ne')

        # current name
        self.current_name = StringVar(value="-")

        tk.Label(self.parent, text="Current Name", bg=self.parent["background"], font=label_font) \
            .place(x=20, y=34)
        tk.Label(self.parent, textvariable=self.current_name, bg=self.parent["background"],
                 font=header_font).place(x=128, y=34)

        # name
        self.ledger_name = StringVar()
        tk.Label(self.parent, text="Ledger Name ", bg=self.parent["background"], font=label_font).place(x=20, y=64)
        self.name_entry = tk.Entry(self.parent, borderwidth=0, bg=util.color_black, fg=util.color_white,
                                   font=label_font, insertbackground=util.color_white, textvariable=self.ledger_name)
        self.name_entry.place(x=128, y=64, width=200, height=24)
        self.name_entry.focus()

        # type
        tk.Label(self.parent, text="Ledger Type ", bg=self.parent["background"], font=label_font).place(x=20, y=94)
        self.type_list_box = tk.Listbox(self.parent, background=util.color_light_green, borderwidth=0,
                                        highlightthickness=0, font=label_font, selectbackground=util.color_dark_green)
        self.type_list_box.place(x=128, y=98, width=200, height=100)

        self.type_list_box.insert(0, "Revenue")
        self.type_list_box.insert(1, "Expenditure")
        self.type_list_box.insert(2, "Asset")
        self.type_list_box.insert(3, "Liability")
        self.type_list_box.insert(4, "Equity")

        # events
        self.name_entry.bind("<Tab>", lambda event: 'break')
        self.name_entry.bind("<Return>", lambda event: self.type_list_box.focus())
        self.name_entry.bind("<Escape>", lambda event: self.ledger_list_box.focus())

        self.type_list_box.bind("<Tab>", lambda event: 'break')
        self.type_list_box.bind("<Return>", lambda event: self.submit())
        self.type_list_box.bind("<Escape>", lambda event: self.name_entry.focus())

        self.ledger_list_box.bind("<Return>", lambda event: self.change_current_account())
        self.ledger_list_box.focus()

    def change_current_account(self):
        try:
            self.selected_ledger_index = self.ledger_list_box.curselection()[0]

        except IndexError:
            self.selected_ledger_index = 0

        self.current_name.set(self.repo.ledgers[self.selected_ledger_index].name.capitalize() + " A/c")
        self.name_entry.focus()

    def submit(self):
        for l in self.repo.ledgers:
            if l.name == self.ledger_name.get().strip():
                modal = util.Modal(self.parent, "Ledger already exists.", util.Modal.TYPE_ALERT)
                modal.set_positive(lambda: self.rectify_error(modal, self.name_entry))
                return

        if self.ledger_name.get().strip() == "":
            self.ledger_name.set(self.repo.ledgers[self.selected_ledger_index].name)

        modal = util.Modal(self.parent, "Are you sure about changing the ledger ?", util.Modal.TYPE_QUESTION)

        try:
            new_type = self.type_list_box.curselection()[0]
        except IndexError:
            new_type = 0

        modal.set_positive(lambda: self.save_ledger(self.ledger_name.get(), new_type, modal))

        modal.set_negative(lambda: self.rectify_error(modal, self.name_entry))

    def save_ledger(self, name, _type, modal):
        self.repo.save_edited_ledger(self.repo.ledgers[self.selected_ledger_index].id, name, _type)
        self.ledger_list_box.focus()

        self.current_name.set("-")

        self.ledger_name.set("")

        self.ledger_list_box.delete(0,END)
        for l in self.repo.ledgers:
            self.ledger_list_box.insert(l.id, l.name)

        modal.destroy()

    def rectify_error(self, modal, widget):
        widget.focus()
        modal.destroy()
