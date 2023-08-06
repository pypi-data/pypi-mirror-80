
__author__ = 'Nicholas C. Pandolfi'


import tkinter as tk
from tkinter import N, S, E, W
from tkinter import ttk


ENTRY_START = '0'
END = tk.END


class ScrolledText(tk.Text):
    def __init__(self, master=None, *args, vbar=True, hbar=False, **kwargs):
        self.frame = tk.Frame(master)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        super().__init__(self.frame, *args, **kwargs)
        self.grid(row=0, column=0, sticky=N+S+E+W) # Push the inherited Text to the frame

        if vbar:
            self.ybar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.yview)
            self.ybar.grid(row=0, column=1, sticky=N+S)
            self.configure(yscrollcommand=self.ybar.set)

        if hbar:
            self.xbar = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.xview)
            self.xbar.grid(row=1, column=0, sticky=E+W)
            self.configure(xscrollcommand=self.xbar.set)

        # Remaining code obtained from Python3 source code (scrolledtext.ScrolledText)
        # Its a hacky way to transfer methods from the container frame -> inherited text
        text_meths = vars(super()).keys()
        geometry_methods = (vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys())
        methods = geometry_methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        # Important for using the scrolltext as a slave
        return str(self.frame)


class ScrolledTree(ttk.Frame):
    def __init__(self, *args, xbar=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(self)
        self.tree.grid(row=0, column=0, sticky=N+S+E+W)

        self.scroll_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.scroll_y.grid(row=0, column=1, sticky=N+S)
        self.tree.configure(yscrollcommand=self.scroll_y.set)

        if xbar:
            self.scroll_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
            self.scroll_x.grid(row=1, column=0, sticky=E+W)
            self.tree.configure(xscrollcommand=self.scroll_x.set)


class PromptedEntry(tk.Entry):
    def __init__(self, *args, prompt='<required>', color='grey', **kwargs):
        super().__init__(*args, **kwargs)
        if 'textvariable' in kwargs:
            self.var = kwargs['textvariable']
        else:
            self.var = tk.StringVar(self)

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.default_color = self['fg']
        self.prompt = prompt
        self.prompt_color = color

        self.put_prompt()

    def put_prompt(self):
        self.insert(0, self.prompt)
        self['fg'] = self.prompt_color
    def insert_text(self, text):
        self.delete(ENTRY_START, END)
        self['fg'] = self.default_color
        self.var.set(text)
    def focus_in(self, event):
        if self['fg'] == self.prompt_color:
            self.delete('0', 'end')
            self['fg'] = self.default_color
    def focus_out(self, event):
        if not self.var.get():
            self.put_prompt()
