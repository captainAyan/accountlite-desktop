import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import utility as util


class CreateJournalEntryScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        heading_font = tkFont.Font(size=20)
        label_font = tkFont.Font(size=10)

        self.debit_account = StringVar()
        self.credit_account = StringVar()
        self.amount = StringVar()

        # debit
        tk.Label(parent, text="DR", bg=parent["background"], font=label_font).place(x=20, y=80)
        tk.Entry(parent, borderwidth=0, bg=util.color_black, fg=util.color_white, font=label_font,
                 textvariable=self.debit_account).place(x=80, y=80, width=200)

        # credit
        tk.Label(parent, text="CR", bg=parent["background"], font=label_font).place(x=20, y=110)
        tk.Entry(parent, borderwidth=0, bg=util.color_black, fg=util.color_white, font=label_font,
                 textvariable=self.credit_account).place(x=80, y=110, width=200)

        # amount
        tk.Label(parent, text="Amount", bg=parent["background"], font=label_font).place(x=20, y=140)
        tk.Entry(parent, borderwidth=0, bg=util.color_black, fg=util.color_white, font=label_font,
                 textvariable=self.amount).place(x=80, y=140, width=200)

        # narration
        tk.Label(parent, text="Narration", bg=parent["background"], font=label_font).place(x=20, y=170)
        self.narration_text = tk.Text(parent, borderwidth=0, bg=util.color_black, fg=util.color_white, font=label_font)
        self.narration_text.place(x=80, y=170, height=80, width=200)

    def submit(self):
        debit_account = self.debit_account.get()
        credit_account = self.credit_account.get()
        amount = self.amount.get()
        narration = self.narration_text.get('1.0', END)

        print(f"Debit {debit_account} Credit {credit_account} Amount {amount} Narration {narration}")


class ViewJournalEntriesScreen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        a = tk.Label(parent, text="View Journal Entries Screen", bg=parent["background"]).grid(row=0, column=0)
