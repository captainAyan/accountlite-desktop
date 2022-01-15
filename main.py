import tkinter
import os

from screens import *
import utility as util


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

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
        Label(header, text="Business Name", bg=util.color_light_green, font='arial 12 bold').place(x=0, y=0)
        Label(header, text="User Name", bg=util.color_light_green, font='arial 12 normal').place(x=0, y=24)
        Label(header, text="Jan 11, 2022", bg=util.color_light_green, font='arial 10 italic').place(x=0, y=56)
        # Label(header, text="Account Lite", relx=1.0, x=0, y=0, anchor="se")

        current_win_title_frame = tk.Frame(header, bg=util.color_dark_green)
        current_win_title_frame.place(height=32, relwidth=1.0, x=0, y=88)
        Label(current_win_title_frame, textvariable=self.current_window_title, font='arial 12 bold', padx=8,
              fg=util.color_white, bg=util.color_dark_green).place(x=0, y=4)
        self.current_window_title.set("Welcome Screen")

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
            CreateJournalEntryScreen(self.mainarea)
            self.current_window_title.set("Create Journal Voucher")
            pass
        elif n == 1:
            # ViewJournalEntriesScreen(self.mainarea)
            self.current_window_title.set("Day Book")
            pass
        elif n == 2:
            # ViewJournalEntriesScreen(self.mainarea)
            self.current_window_title.set("Journal List")
            pass
        elif n == 3:
            # ViewJournalEntriesScreen(self.mainarea)
            self.current_window_title.set("Create Ledger")
            pass
        elif n == 4:
            # ViewJournalEntriesScreen(self.mainarea)
            self.current_window_title.set("Ledger List")
            pass
        elif n == 5:
            # ViewJournalEntriesScreen(self.mainarea)
            self.current_window_title.set("Ledger View")
            pass
        elif n == 6:
            # ViewJournalEntriesScreen(self.mainarea)
            self.current_window_title.set("Trial Balance")
            pass
        elif n == 7:
            # ViewJournalEntriesScreen(self.mainarea)
            self.current_window_title.set("Income & Expenditure Statement")
            pass
        elif n == 8:
            # ViewJournalEntriesScreen(self.mainarea)
            self.current_window_title.set("Balance Sheet Statement")
            pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pycyptor")
    root.minsize("900", "600")
    # root.resizable(0, 0)
    root.geometry("1360x780")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
