import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta

import utility as util


class ViewLedgerScreen(tk.Frame):
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

        style = ttk.Style()

        style.theme_use("default")
        style.configure("Treeview", background=util.color_orange, foreground=util.color_black,
                        fieldbackground=util.color_orange, font=label_font, borderwidth=0, rowheight=40)
        style.map('Treeview', background=[('selected', util.color_red)])

        style.configure("Treeview.Heading", background=util.color_dark_green, foreground=util.color_white,
                        font=header_font, borderwidth=1)

        columns = ('date', 'particulars', 'id', 'debit', 'credit')
        self.tree = ttk.Treeview(self.mainarea, columns=columns, show='headings', selectmode="browse")

        self.tree.heading('date', text='Date')
        self.tree.column('date', minwidth=0, width=100, stretch=NO)

        self.tree.heading('particulars', text='Particulars')
        self.tree.column('particulars', minwidth=0, width=200)

        self.tree.heading('id', text='No.')
        self.tree.column('id', minwidth=0, width=80, stretch=NO)

        self.tree.heading('debit', text='Debit')
        self.tree.column('debit', minwidth=0, width=200, anchor="e", stretch=NO)

        self.tree.heading('credit', text='Credit')
        self.tree.column('credit', minwidth=0, width=200, anchor="e", stretch=NO)

        self.tree.pack(anchor=N, fill=BOTH, expand=True, side=BOTTOM)

        description_frame = Frame(self.mainarea, bg=util.color_yellow, height=160)
        description_frame.pack(anchor=N, fill=X, expand=False, side=TOP)

        self.ledger_name = StringVar(value="-")

        tk.Label(description_frame, text="Ledger Name ", bg=description_frame["background"], font=label_font)\
            .place(x=10, y=10)
        tk.Label(description_frame, textvariable=self.ledger_name, bg=description_frame["background"],
                 font=header_font).place(x=128, y=10)

        self.ledger_type = StringVar(value="-")

        tk.Label(description_frame, text="Ledger Type ", bg=description_frame["background"], font=label_font) \
            .place(x=10, y=34)
        tk.Label(description_frame, textvariable=self.ledger_type, bg=description_frame["background"],
                 font=header_font).place(x=128, y=34)

        self.opening_balance = StringVar(value="-")

        tk.Label(description_frame, text="Opening Bal. ", bg=description_frame["background"], font=label_font) \
            .place(x=10, y=58)
        tk.Label(description_frame, textvariable=self.opening_balance, bg=description_frame["background"],
                 font=header_font).place(x=128, y=58)

        self.closing_balance = StringVar(value="-")

        tk.Label(description_frame, text="Closing Bal. ", bg=description_frame["background"], font=label_font) \
            .place(x=10, y=82)
        tk.Label(description_frame, textvariable=self.closing_balance, bg=description_frame["background"],
                 font=header_font).place(x=128, y=82)

        self.from_date = StringVar(value=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))

        tk.Label(description_frame, text="From Date ", bg=description_frame["background"], font=label_font) \
            .place(x=10, y=106)
        self.from_date_entry = tk.Entry(description_frame, textvariable=self.from_date, bg=util.color_black,
                                        fg=util.color_white, font=header_font, insertbackground=util.color_white)
        self.from_date_entry.place(x=128, y=106)

        self.to_date = StringVar(value=(datetime.now()).strftime("%Y-%m-%d"))

        tk.Label(description_frame, text="To Date ", bg=description_frame["background"], font=label_font) \
            .place(x=10, y=130)
        self.to_date_entry = tk.Entry(description_frame, textvariable=self.to_date, bg=util.color_black,
                                      fg=util.color_white, font=header_font, insertbackground=util.color_white)
        self.to_date_entry.place(x=128, y=130)

        # Events
        self.from_date_entry.focus()
        self.from_date_entry.bind('<Return>', lambda event: self.to_date_entry.focus())

        self.to_date_entry.bind('<Escape>', lambda event: self.from_date_entry.focus())
        self.to_date_entry.bind('<Return>', lambda event: self.ledger_list_box.focus())

        self.ledger_list_box.bind('<Escape>', lambda event: self.to_date_entry.focus())
        self.ledger_list_box.bind('<Return>', lambda event: self.change_current_account())

        self.tree.bind('<Escape>', lambda event: self.ledger_list_box.focus())

    def change_current_account(self):
        try:
            self.selected_ledger_index = self.ledger_list_box.curselection()[0]

        except IndexError:
            self.selected_ledger_index = 0

        self.render_ledger()
        self.tree.focus()

    def render_ledger(self):
        self.tree.delete(*self.tree.get_children())

        # NOTE: +ve value is Debit balance and -ve value is Credit balance
        opening_balance = 0
        offset_balance = 0  # balance during the period (from_date -> to_date) Therefore, closing = opening + offset

        current_ledger = self.repo.ledgers[self.selected_ledger_index]
        ledger_types = ["Revenue Account",
                        "Expenditure Account",
                        "Asset Account",
                        "Liability Account",
                        "Equity Account"]

        self.ledger_name.set(current_ledger.name.capitalize() + " A/c")
        self.ledger_type.set(ledger_types[current_ledger.type])

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

        items = []
        for j in self.repo.journals:

            if to_date.timestamp() < j.time:
                break

            if j.time < from_date.timestamp():
                if current_ledger.id == j.debit.id:
                    opening_balance += j.amount
                elif current_ledger.id == j.credit.id:
                    opening_balance -= j.amount

            if from_date.timestamp() <= j.time < to_date.timestamp():

                if current_ledger.id == j.debit.id:
                    offset_balance += j.amount
                    items.append((datetime.fromtimestamp(j.time).strftime('%Y-%m-%d'), "To. " + j.credit.name.capitalize() +
                                  " A/c", "#" + str(j.id), util.format_currency(j.amount,
                                                                                self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                                                self.repo.meta_data_dict['CURRENCY']), ""))

                elif current_ledger.id == j.credit.id:
                    offset_balance -= j.amount
                    items.append((datetime.fromtimestamp(j.time).strftime('%Y-%m-%d'), "By. " + j.debit.name.capitalize() +
                                  " A/c", "#" + str(j.id), "", util.format_currency(j.amount,
                                                                                    self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                                                    self.repo.meta_data_dict['CURRENCY'])))

        if opening_balance > 0:
            self.opening_balance.set(util.format_currency(opening_balance,
                                                          self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                          self.repo.meta_data_dict['CURRENCY']) + " Dr.")
        elif opening_balance < 0:
            self.opening_balance.set(util.format_currency(opening_balance*-1,
                                                          self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                          self.repo.meta_data_dict['CURRENCY']) + " Cr.")
        else:
            self.opening_balance.set("-")

        if opening_balance + offset_balance > 0:
            self.closing_balance.set(util.format_currency(opening_balance + offset_balance,
                                                          self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                          self.repo.meta_data_dict['CURRENCY']) + " Dr.")
        elif opening_balance + offset_balance < 0:
            self.closing_balance.set(util.format_currency((opening_balance + offset_balance)*-1,
                                                          self.repo.meta_data_dict['CURRENCY_FORMAT'],
                                                          self.repo.meta_data_dict['CURRENCY']) + " Cr.")
        else:
            self.closing_balance.set("-")

        for i in reversed(items):
            self.tree.insert('', tk.END, values=i)

    def rectify_error(self, modal, widget):
        widget.focus()
        modal.destroy()
