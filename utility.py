import tkinter as tk

color_yellow = "#FFFFD9"
color_light_green = "#D6F6D6"
color_dark_green = "#008080"
color_orange = "#FFDDCC"
color_grey = "#D0D0D0"
color_white = "#FFFFFF"
color_black = "#000000"

color_success = "#32ff7e"
color_danger = "#ff4d4d"
color_red = "#ff4d4d"
color_warning = "#ffaf40"
color_info = "#18dcff"


def string_to_int(val):
    try:
        return int(val)
    except ValueError:
        return 0


def format_currency(amount, _type, currency):
    if _type == "int":
        return currency + ("{:,}".format(amount))

    elif _type == "ind":
        s, *d = str(amount).partition(".")
        r = ",".join([s[x - 2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return currency + ("".join([r] + d))

    else:
        return ""


class Modal:
    TYPE_ALERT = 1
    TYPE_QUESTION = 2

    def __init__(self, parent, message, modal_type):

        self.type = modal_type

        self.positive_method = None
        self.negative_method = None
        # modal
        self.modal = tk.Frame(parent, bg=color_orange, height=200, width=200)
        self.modal.place(x=0, rely=1, anchor='sw')
        tk.Label(self.modal, text=message, bg=self.modal["background"],
                 font="arial 12 normal", wraplength=200).place(relx=0.5, rely=0.3, anchor='center')

        self.modal.focus()
        self.modal.bind("<Return>", lambda event: self.positive_method())
        self.modal.bind("<Escape>", lambda event: self.cancel_modal())
        self.modal.bind("<Tab>", lambda event: 'break')

        if self.type == Modal.TYPE_ALERT:
            tk.Button(self.modal, text="Okay", background=self.modal["background"], border=0, font="arial 12 bold",
                      command=lambda: self.positive_method()).place(relx=0.5, rely=0.9, anchor='center')
        elif self.type == Modal.TYPE_QUESTION:
            tk.Button(self.modal, text="Yes", background=self.modal["background"], border=0, font="arial 12 bold",
                      command=lambda: self.positive_method()).place(relx=0.1, rely=0.9, anchor='sw')
            tk.Button(self.modal, text="No", background=self.modal["background"], border=0, font="arial 12 bold",
                      command=lambda: self.negative_method()).place(relx=0.9, rely=0.9, anchor='se')

    def destroy(self):
        for widget in self.modal.winfo_children():
            widget.destroy()
        self.modal.destroy()

    def cancel_modal(self):
        if self.type == Modal.TYPE_QUESTION:
            self.negative_method()
        else:
            self.positive_method()

    def set_positive(self, method):
        self.positive_method = method

    def set_negative(self, method):
        self.negative_method = method
