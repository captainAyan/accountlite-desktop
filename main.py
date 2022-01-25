
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont

import utility as util
from repository import Repository
from screen.createJournalEntryScreen import CreateJournalEntryScreen
from screen.viewDayBookScreen import ViewDayBookScreen
from screen.viewJournalList import ViewJournalList
from screen.createLedgerScreen import CreateLedgerScreen

FILE_NAME = 'book.bk'


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.repo = Repository(FILE_NAME)

        self.parent = parent
        self.current_window_title = StringVar()

        custom_font = tkFont.Font(size=10, weight="bold", family="Arial")
        btn_style = {'borderwidth': "0", 'font': custom_font, 'bd': '2', 'bg': util.color_dark_green,
                     'fg': util.color_white, 'anchor': "w", 'padx': 4}
        btn_size = {'height': 40, 'width': 180}

        sidebar = tk.Frame(self.parent, bg=util.color_grey, width=180)
        sidebar.pack(expand=False, fill='y', side='right', anchor='nw')

        header = tk.Frame(self.parent, bg=util.color_light_green, height=120)
        header.pack(expand=False, fill='both', side='top', anchor='n')

        # Header labels
        Label(header, text="Business Name", bg=header["background"], font='arial 12 bold').place(x=0, y=0)
        Label(header, text="User Name", bg=header["background"], font='arial 12 normal').place(x=0, y=24)
        Label(header, text="Jan 11, 2022", bg=header["background"], font='arial 10 italic').place(x=0, y=56)

        current_win_title_frame = tk.Frame(header, bg=util.color_dark_green)
        current_win_title_frame.place(height=32, relwidth=1.0, x=0, y=88)
        Label(current_win_title_frame, textvariable=self.current_window_title, font='arial 12 bold', padx=8,
              fg=util.color_white, bg=util.color_dark_green).place(x=0, y=4)
        self.current_window_title.set("Welcome Screen")

        tk.Button(current_win_title_frame, text="✕", borderwidth=0, font="size=24",
                  command=lambda:self.change_tab(-1)).place(width=32, height=32, relx=1, rely=0, anchor="ne")

        tk.Button(sidebar, text="[Q] Journal Voucher", **btn_style, command=lambda:self.change_tab(0)).place(**btn_size, x=0, y=0)
        tk.Button(sidebar, text="[W] Day Book", **btn_style, command=lambda:self.change_tab(1)).place(**btn_size, x=0, y=40)
        tk.Button(sidebar, text="[E] Journal List", **btn_style, command=lambda:self.change_tab(2)).place(**btn_size, x=0, y=80)
        tk.Button(sidebar, text="[R] Create Ledger", **btn_style, command=lambda:self.change_tab(3)).place(**btn_size, x=0, y=120)
        tk.Button(sidebar, text="[T] Ledger List", **btn_style, command=lambda:self.change_tab(4)).place(**btn_size, x=0, y=160)
        tk.Button(sidebar, text="[Y] Ledger View", **btn_style, command=lambda:self.change_tab(5)).place(**btn_size, x=0, y=200)
        tk.Button(sidebar, text="[U] Trial Balance", **btn_style, command=lambda:self.change_tab(6)).place(**btn_size, x=0, y=240)
        tk.Button(sidebar, text="[I] Income Statement", **btn_style, command=lambda:self.change_tab(7)).place(**btn_size, x=0, y=280)
        tk.Button(sidebar, text="[O] Balance Sheet", **btn_style, command=lambda:self.change_tab(8)).place(**btn_size, x=0, y=320)

        self.mainarea = tk.Frame(self.parent, bg=util.color_yellow, width=500, height=500)
        self.mainarea.pack(expand=True, fill='both', side='right')

        self.parent.bind('<Control-q>', lambda event: self.change_tab(0))
        self.parent.bind('<Control-w>', lambda event: self.change_tab(1))
        self.parent.bind('<Control-e>', lambda event: self.change_tab(2))
        self.parent.bind('<Control-r>', lambda event: self.change_tab(3))
        self.parent.bind('<Control-t>', lambda event: self.change_tab(4))
        self.parent.bind('<Control-y>', lambda event: self.change_tab(5))
        self.parent.bind('<Control-u>', lambda event: self.change_tab(6))
        self.parent.bind('<Control-i>', lambda event: self.change_tab(7))
        self.parent.bind('<Control-o>', lambda event: self.change_tab(8))

    def change_tab(self, n):
        for widget in self.mainarea.winfo_children():
            widget.destroy()

        if n == 0:
            self.current_window_title.set("Create Journal Voucher")
            CreateJournalEntryScreen(self.mainarea, self.repo)
            pass
        elif n == 1:
            self.current_window_title.set("Day Book")
            ViewDayBookScreen(self.mainarea, self.repo)
            pass
        elif n == 2:
            self.current_window_title.set("Journal List")
            ViewJournalList(self.mainarea, self.repo)
            pass
        elif n == 3:
            self.current_window_title.set("Create Ledger")
            CreateLedgerScreen(self.mainarea, self.repo)
            pass
        elif n == 4:
            self.current_window_title.set("Ledger List")
            pass
        elif n == 5:
            self.current_window_title.set("Ledger View")
            pass
        elif n == 6:
            self.current_window_title.set("Trial Balance")
            pass
        elif n == 7:
            self.current_window_title.set("Income & Expenditure Statement")
            pass
        elif n == 8:
            self.current_window_title.set("Balance Sheet Statement")
            pass
        else:
            self.current_window_title.set("Welcome Screen")
            pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("AccountLite")
    root.minsize("1200", "720")
    # root.resizable(0, 0)
    root.geometry("1200x720")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
