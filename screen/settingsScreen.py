import tkinter as tk
from tkinter import *

import utility as util


class SettingsScreen(tk.Frame):
    def __init__(self, parent, repo, business, name, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.repo = repo
        self.parent = parent

        label_font = "arial 12 normal"

        # business name
        self.business = business
        tk.Label(self.parent, text="Business Name", bg=self.parent["background"], font=label_font).place(x=20, y=30)
        self.business_entry = tk.Entry(self.parent, borderwidth=0, bg=util.color_black, fg=util.color_white,
                                   font=label_font, insertbackground=util.color_white, textvariable=self.business)
        self.business_entry.place(x=148, y=30, width=200, height=24)
        self.business_entry.focus()
        self.business_entry.bind('<Return>', lambda event: self.name_entry.focus())

        # user name
        self.name = name
        tk.Label(self.parent, text="User Name", bg=self.parent["background"], font=label_font).place(x=20, y=60)
        self.name_entry = tk.Entry(self.parent, borderwidth=0, bg=util.color_black, fg=util.color_white,
                                   font=label_font, insertbackground=util.color_white, textvariable=self.name)
        self.name_entry.place(x=148, y=60, width=200, height=24)
        self.name_entry.focus()
        self.name_entry.bind('<Return>', lambda event: self.currency_entry.focus())
        self.name_entry.bind('<Escape>', lambda event: self.business_entry.focus())

        # currency
        self.currency = StringVar(value=self.repo.meta_data_dict['CURRENCY'])
        tk.Label(self.parent, text="Currency", bg=self.parent["background"], font=label_font).place(x=20, y=90)
        self.currency_entry = tk.Entry(self.parent, borderwidth=0, bg=util.color_black, fg=util.color_white,
                                       font=label_font, insertbackground=util.color_white, textvariable=self.currency)
        self.currency_entry.place(x=148, y=90, width=200, height=24)
        self.currency_entry.focus()
        self.currency_entry.bind('<Return>', lambda event: self.currency_format_entry.focus())
        self.currency_entry.bind('<Escape>', lambda event: self.name_entry.focus())

        # currency format
        self.currency_format = StringVar(value=self.repo.meta_data_dict['CURRENCY_FORMAT'])
        tk.Label(self.parent, text="Currency Format", bg=self.parent["background"], font=label_font).place(x=20, y=120)
        self.currency_format_entry = tk.Entry(self.parent, borderwidth=0, bg=util.color_black, fg=util.color_white,
                                              font=label_font, insertbackground=util.color_white,
                                              textvariable=self.currency_format)
        self.currency_format_entry.place(x=148, y=120, width=200, height=24)
        self.currency_format_entry.focus()
        self.currency_format_entry.bind('<Return>', lambda event: self.submit())
        self.currency_format_entry.bind('<Escape>', lambda event: self.currency_entry.focus())
        tk.Label(self.parent, text="Write 'ind' for Indian format and 'int' for international", font=label_font,
                 bg=self.parent["background"]).place(x=360, y=120)

    def submit(self):
        modal = util.Modal(self.parent, "Save settings ?", util.Modal.TYPE_QUESTION)
        modal.set_positive(lambda: self.save_settings(modal))
        modal.set_negative(lambda: modal.destroy())

    def save_settings(self, modal):
        self.repo.save_settings(self.business.get(), self.name.get(), self.currency.get(), self.currency_format.get())
        modal.destroy()
