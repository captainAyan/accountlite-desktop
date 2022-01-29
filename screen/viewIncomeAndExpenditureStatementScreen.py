import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta

import utility as util


class ViewIncomeAndExpenditureStatementScreen(tk.Frame):
    def __init__(self, parent, repo, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.repo = repo
        self.parent = parent

        label_font = "arial 12 normal"
        header_font = "arial 12 bold"

        style = ttk.Style()

        style.theme_use("default")
        style.configure("Treeview", background=util.color_yellow, foreground=util.color_black,
                        fieldbackground=util.color_yellow, font=label_font, borderwidth=0, rowheight=40)
        style.map('Treeview', background=[('selected', util.color_dark_green)])

        style.configure("Treeview.Heading", background=util.color_dark_green, foreground=util.color_white,
                        font=header_font, borderwidth=1)

        columns = ('id', 'name', 'amount1', 'amount2')
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings', selectmode="browse")

        self.tree.heading('id', text='No.')
        self.tree.column('id', minwidth=0, width=60, stretch=NO)

        self.tree.heading('name', text='Name')
        self.tree.column('name', minwidth=0, width=100)

        self.tree.heading('amount1', text='Amount')
        self.tree.column('amount1', minwidth=0, width=200, anchor="e", stretch=NO)

        self.tree.heading('amount2', text='Amount')
        self.tree.column('amount2', minwidth=0, width=200, anchor="e", stretch=NO)

        self.tree.place(x=0, y=0, relwidth=1, relheight=1)

        self.tree.pack(anchor=N, fill=BOTH, expand=True, side=BOTTOM)

        self.tree.tag_configure('title', font=header_font, background=util.color_dark_green, foreground=util.color_white)
        self.tree.tag_configure('total', font=header_font)

        filter_frame = Frame(self.parent, bg=util.color_yellow, height=42)
        filter_frame.pack(anchor=N, fill=X, expand=False, side=TOP)

        self.for_the_year_ended_on = StringVar(value=(datetime.now()).strftime("%Y-%m-%d"))

        tk.Label(filter_frame, text="For The Year Ended On ", bg=filter_frame["background"], font=label_font).place(x=10, y=10)
        self.for_the_year_ended_on_entry = tk.Entry(filter_frame, textvariable=self.for_the_year_ended_on,
                                                    bg=util.color_black, fg=util.color_white, font=header_font,
                                                    insertbackground=util.color_white)
        self.for_the_year_ended_on_entry.place(x=192, y=10)
        self.for_the_year_ended_on_entry.focus()
        self.for_the_year_ended_on_entry.bind('<Return>', lambda event: self.render_trial_balance())

    def render_trial_balance(self):
        self.tree.delete(*self.tree.get_children())

        try:
            as_on_date = datetime.strptime(self.for_the_year_ended_on.get(), '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        except ValueError:
            modal = util.Modal(self.parent, "'For The Year Ended On' date is not formatted correctly.", util.Modal.TYPE_ALERT)
            modal.set_positive(lambda: self.rectify_error(modal, self.for_the_year_ended_on_entry))
            return

        ledger_balance_dict = {}
        for l in self.repo.ledgers:
            ledger_balance_dict[l.id] = 0

        for j in self.repo.journals:

            if as_on_date.timestamp() <= j.time:
                break

            if j.time < as_on_date.timestamp():
                ledger_balance_dict[j.debit.id] = ledger_balance_dict[j.debit.id] + j.amount
                ledger_balance_dict[j.credit.id] = ledger_balance_dict[j.credit.id] - j.amount

        # Revenue
        self.tree.insert('', tk.END, values=("", "Revenue [A]", "", ""), tags=('title',))
        total_revenue = 0
        for k in self.repo.ledgers:
            if k.type == 0:
                total_revenue -= ledger_balance_dict[k.id]
                balance_text = util.format_currency(-ledger_balance_dict[k.id],
                                                    self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                    self.repo.meta_data_dict['CURRENCY'])

                i = ("#" + str(k.id), k.name.capitalize() + " A/c", balance_text, "")
                self.tree.insert('', tk.END, values=i)

        self.tree.insert('', tk.END, values=("", "Total", "",
                                             util.format_currency(total_revenue,
                                                                  self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                                  self.repo.meta_data_dict['CURRENCY'])),
                         tags=('total',))

        # Expenses
        self.tree.insert('', tk.END, values=("", "Expenditure [B]", "", ""), tags=('title',))
        total_expenditure = 0
        for k in self.repo.ledgers:
            if k.type == 1:
                total_expenditure += ledger_balance_dict[k.id]
                balance_text = util.format_currency(ledger_balance_dict[k.id],
                                                    self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                    self.repo.meta_data_dict['CURRENCY'])

                i = ("#" + str(k.id), k.name.capitalize() + " A/c", balance_text, "")
                self.tree.insert('', tk.END, values=i)

        self.tree.insert('', tk.END, values=("", "Total", "",
                                             util.format_currency(total_expenditure,
                                                                  self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                                  self.repo.meta_data_dict['CURRENCY'])),
                         tags=('total',))

        # Bottom line
        self.tree.insert('', tk.END, values=("", "Surplus/(Deficit) [A - B]", "",
                                             util.format_currency(total_revenue - total_expenditure,
                                                                  self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                                  self.repo.meta_data_dict['CURRENCY'])),
                         tags=('title',))

    def rectify_error(self, modal, widget):
        widget.focus()
        modal.destroy()
