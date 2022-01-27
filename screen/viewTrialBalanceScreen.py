import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta

import utility as util


class ViewTrialBalanceScreen(tk.Frame):
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

        columns = ('id', 'name', 'type', 'balance')
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings', selectmode="browse")

        self.tree.heading('id', text='No.')
        self.tree.column('id', minwidth=0, width=60, stretch=NO)

        self.tree.heading('name', text='Name')
        self.tree.column('name', minwidth=0, width=100)

        self.tree.heading('type', text='Type')
        self.tree.column('type', minwidth=0, width=200, stretch=NO)

        self.tree.heading('balance', text='Balance')
        self.tree.column('balance', minwidth=0, width=200, anchor="e", stretch=NO)

        self.tree.place(x=0, y=0, relwidth=1, relheight=1)

        self.tree.pack(anchor=N, fill=BOTH, expand=True, side=BOTTOM)

        filter_frame = Frame(self.parent, bg=util.color_yellow, height=66)
        filter_frame.pack(anchor=N, fill=X, expand=False, side=TOP)

        self.as_on_date = StringVar(value=(datetime.now()).strftime("%Y-%m-%d"))

        tk.Label(filter_frame, text="As On Date ", bg=filter_frame["background"], font=label_font) \
            .place(x=10, y=10)
        self.as_on_date_entry = tk.Entry(filter_frame, textvariable=self.as_on_date, bg=util.color_black,
                                         fg=util.color_white, font=header_font, insertbackground=util.color_white)
        self.as_on_date_entry.place(x=128, y=10)

        self.total = StringVar(value="-")

        tk.Label(filter_frame, text="Total ", bg=filter_frame["background"], font=label_font) \
            .place(x=10, y=34)
        tk.Label(filter_frame, textvariable=self.total, bg=filter_frame["background"], font=header_font) \
            .place(x=128, y=34)

        self.as_on_date_entry.focus()
        self.as_on_date_entry.bind('<Return>', lambda event: self.render_trial_balance())

    def render_trial_balance(self):
        self.tree.delete(*self.tree.get_children())

        ledger_types = ["Revenue Account",
                        "Expenditure Account",
                        "Asset Account",
                        "Liability Account",
                        "Equity Account"]

        total = 0

        try:
            as_on_date = datetime.strptime(self.as_on_date.get(), '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        except ValueError:
            modal = util.Modal(self.parent, "'As On Date' date is not formatted correctly.", util.Modal.TYPE_ALERT)
            modal.set_positive(lambda: self.rectify_error(modal, self.as_on_date_entry))
            return

        ledger_dict = {}
        for l in self.repo.ledgers:
            ledger_dict[l.id] = 0

        for j in self.repo.journals:

            if as_on_date.timestamp() <= j.time:
                break

            if j.time < as_on_date.timestamp():
                ledger_dict[j.debit.id] = ledger_dict[j.debit.id] + j.amount
                ledger_dict[j.credit.id] = ledger_dict[j.credit.id] - j.amount

        for k in self.repo.ledgers:
            balance = ledger_dict[k.id]

            # calculation of absolute value
            if balance < 0:
                balance = balance * -1

            total += balance

            balance_text = util.format_currency(balance, self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                self.repo.meta_data_dict['CURRENCY'])

            # add parenthesis to -ve balances of debit accounts and +ve balances of credit accounts
            if (ledger_dict[k.id] < 0 and (k.type == 1 or k.type == 2)) or \
                    (ledger_dict[k.id] > 0 and (k.type == 0 or k.type == 3 or k.type == 4)):
                balance_text = "(" + balance_text + ")"

            i = ("#" + str(k.id), k.name.capitalize() + " A/c", ledger_types[k.type], balance_text)

            self.tree.insert('', tk.END, values=i)

        self.total.set(util.format_currency(int(total/2), self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                            self.repo.meta_data_dict['CURRENCY']))

    def rectify_error(self, modal, widget):
        widget.focus()
        modal.destroy()
