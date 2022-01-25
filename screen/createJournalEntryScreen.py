import tkinter as tk
from tkinter import *
import time
import utility as util


class CreateJournalEntryScreen(tk.Frame):
    def __init__(self, parent, repo, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.repo = repo
        self.parent = parent

        label_font = "arial 12 normal"
        header_font = "arial 10 bold"

        self.debit_account = StringVar()
        self.credit_account = StringVar()
        self.amount = StringVar()
        self.narration = StringVar()

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

        self.ledger_list_box.focus()
        self.ledger_list_box.bind('<Return>', lambda event: self.list_enter())
        self.ledger_list_box.bind('<Escape>', lambda event: self.debit_account.set(""))
        self.ledger_list_box.bind("<Tab>", lambda event: 'break')  # prevent use of tab to switch entrybox

        # main area
        self.mainarea = tk.Frame(self.parent, bg=parent["background"])
        self.mainarea.pack(expand=True, fill='both', side='right', anchor='ne')

        # Header
        header = tk.Frame(self.mainarea, bg=parent["background"], height=28, highlightbackground="black",
                          highlightthickness=2)
        header.place(x=0, y=20, relwidth=1)
        tk.Label(header, text="Amount (Dr.)", bg=header["background"], font=header_font) \
            .place(relx=0.85, y=0, anchor="ne")
        tk.Label(header, text="Amount (Cr.)", bg=header["background"], font=header_font) \
            .place(relx=0.99, y=0, anchor="ne")
        tk.Label(header, text="Particular", bg=header["background"], font=header_font).place(x=20, y=0)

        # debit
        tk.Label(self.mainarea, text="Dr.", bg=self.mainarea["background"], font=label_font).place(x=20, y=60)
        tk.Entry(self.mainarea, borderwidth=0, font=label_font, textvariable=self.debit_account,
                 disabledbackground=util.color_black, disabledforeground=util.color_white, state='disabled')\
            .place(x=60, y=60, width=200, height=24)

        # credit
        tk.Label(self.mainarea, text="Cr.", bg=self.mainarea["background"], font=label_font).place(x=20, y=90)
        tk.Entry(self.mainarea, borderwidth=0, font=label_font, textvariable=self.credit_account,
                 disabledbackground=util.color_black, disabledforeground=util.color_white, state='disabled')\
            .place(x=60, y=90, width=200, height=24)

        # amounts
        self.amount_entry = tk.Entry(self.mainarea, textvariable=self.amount, borderwidth=0, bg=util.color_black,
                                     fg=util.color_white, font=label_font, insertbackground=util.color_white,
                                     justify='right')
        self.amount_entry.place(relx=0.85, y=60, width=100, height=24, anchor="ne")
        self.amount_entry.bind('<Return>', lambda event: self.narration_entry.focus())
        self.amount_entry.bind('<Escape>', lambda event: self.ledger_list_box.focus())

        # the other amount
        tk.Entry(self.mainarea, textvariable=self.amount, borderwidth=0, bg=util.color_black, fg=util.color_white,
                 font=label_font, state='disabled', justify='right')\
            .place(relx=0.99, y=90, width=100, height=24, anchor="ne")

        # narration
        tk.Label(self.mainarea, text="Narration", bg=self.mainarea["background"], font=label_font).place(x=20, y=140)
        self.narration_entry = tk.Entry(self.mainarea, borderwidth=0, bg=util.color_black, fg=util.color_white,
                                        font=label_font, insertbackground=util.color_white, textvariable=self.narration)
        self.narration_entry.place(x=100, y=140, height=80, width=200)
        self.narration_entry.bind('<Return>', lambda event: self.submit())
        self.narration_entry.bind('<Escape>', lambda event: self.amount_entry.focus())

    def create_entry(self, modal, debit, credit, amount, narration):
        print("Create the entry")
        self.debit_account.set("")
        self.credit_account.set("")
        self.amount.set("")
        self.narration.set("")
        self.ledger_list_box.focus()
        modal.destroy()
        self.repo.add_entry(amount, int(time.time()), debit, credit, narration)

    def rectify_error(self, modal, widget):
        widget.focus()
        modal.destroy()

    def submit(self):
        debit = self.debit_account.get().strip()
        credit = self.credit_account.get().strip()
        amount = util.string_to_int(self.amount.get().strip())
        narration = self.narration.get().strip()

        if narration == "":
            modal = util.Modal(self.mainarea, "Narration cannot be empty.", util.Modal.TYPE_ALERT)
            modal.set_positive(lambda: self.rectify_error(modal, self.narration_entry))
        elif amount == 0:
            modal = util.Modal(self.mainarea, "Invalid amount.", util.Modal.TYPE_ALERT)
            modal.set_positive(lambda: self.rectify_error(modal, self.amount_entry))
        elif debit == credit:
            modal = util.Modal(self.mainarea, "Debit and Credit Account cannot be the same.", util.Modal.TYPE_ALERT)
            modal.set_positive(lambda: self.rectify_error(modal, self.ledger_list_box))
        elif debit == "":
            modal = util.Modal(self.mainarea, "Debit side cannot be empty.", util.Modal.TYPE_ALERT)
            modal.set_positive(lambda: self.rectify_error(modal, self.ledger_list_box))
        elif credit == "":
            modal = util.Modal(self.mainarea, "Credit side cannot be empty.", util.Modal.TYPE_ALERT)
            modal.set_positive(lambda: self.rectify_error(modal, self.ledger_list_box))
        else:
            modal = util.Modal(self.mainarea, "Are you sure about creating the entry ?", util.Modal.TYPE_QUESTION)
            modal.set_positive(lambda: self.create_entry(modal, debit, credit, amount, narration))
            modal.set_negative(lambda: self.rectify_error(modal, self.narration_entry))

    def list_enter(self):
        if not self.debit_account.get():
            self.debit_account.set(self.ledger_list_box.get(self.ledger_list_box.curselection()))
            if self.credit_account.get():
                self.amount_entry.focus()

        elif not self.credit_account.get():
            self.credit_account.set(self.ledger_list_box.get(self.ledger_list_box.curselection()))
            self.amount_entry.focus()

        elif self.debit_account.get() and self.credit_account.get():
                self.credit_account.set(self.ledger_list_box.get(self.ledger_list_box.curselection()))
                self.amount_entry.focus()
