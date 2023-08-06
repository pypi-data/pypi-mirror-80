
__author__ = 'Nicholas C. Pandolfi'
#__all__ = ['app', 'HighlightView', 'TextFromLink', 'ScrollTree']


# Standard imports
import re, os, time, string, copy, functools

# TK imports
import tkinter as tk
from tkinter import ttk
from tkinter import N, S, E, W
from tkinter import messagebox, font, filedialog, scrolledtext, simpledialog

# Specialized imports
from .pathway import get_dir, get_name, path
from .simple_request import download
from .data import REGEX_TEMPLATES_LAYOUT, REGEX_TEMPLATES, FLAGS_DOCS, SYNTAX_DOCS, HELP_STRUCTURE, HELP_ABOUT, FONT_STYLES
from .util import process_docs, new_font, invert_hex, format_index, process_pattern, font_data, find_matches
from .widgets import ScrolledText, PromptedEntry, ScrolledTree


# TODO : Reorder all of these constants to be grouped correctly. Maybe different module ?
# TK Constants
START, END = '1.0', tk.END
ENABLED, DISABLED = ['!disabled'], ['disabled']

# String templates
INDEX_TEMPLATE = '1.0+{}c'
TIME_DISPLAY = 'Time: {} ms'
MATCHES_DISPLAY = '{} Matches'
STEPS_DISPLAY = 'Steps: {}'

# Color definitions for highlighting
SINGLE_COLOR = '#FFCE5C'
PASTEL_QUEUE = ('#A8E6CE', '#DCEDC2', '#FFD3B5', '#FFAAA6', '#FF8C94')
#GYCMBR_QUEUE = ('#ffff80', '#80ff80', '#80ffff', '#ff80ff', '#8080ff', '#ff8080')
GYCMBR_QUEUE = ('#FFFF80', '#80FF80', '#FF80FF', '#80FFFF', '#FF8080', '#8080FF')
COLOR_QUEUE = GYCMBR_QUEUE # !!! SELECT THE ACTIVE COLOR QUEUE HERE !!!

# Container lapping functions
GET_COLOR = lambda n: COLOR_QUEUE[n % len(COLOR_QUEUE)]
#CHAR2INT = lambda c: _LOWERCASE.index(n % len(_LOWERCASE))
INT2CHAR = lambda n: string.ascii_lowercase[n % len(string.ascii_lowercase)] # TODO only wraps around

# Misc. constants
MIN_RIGHT_PANE_SIZE = 250  #  pixels
STD_TITLE = 'Multi-Document RegEx IDE'
MINILOOP_PERIOD = 25 # ms
REALTIME_DELAY = 1250 # ms
FLAGS = ('IGNORECASE', 'DOTALL', 'MULTILINE', 'VERBOSE', 'ASCII')
FONT_SIZES = tuple(str(i) for i in (1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28))

CYCLES_PER_UPDATE = 10 # Amount of processing loop cycles between gui update events
PROGRESS_STEPS = 350

# Limit definitions
FATAL_OVERLOAD = 99999  #  Reasonable to assume that 100,000 matches is a mistake...
TREE_OVERLOAD = 100
HIGHLIGHT_OVERLOAD = 1000
REALTIME_OVERLOAD = 50000  #  Turns off the realtime flag if matches exceed this
DATA_OVERLOAD = (1024 ** 2) / 10   #   greater than 100 kb of chars will slow down the program significantly
LINK_PAGE_NAME_LEN = 30   #   How many characters to limit the page name from a retrieved link
AUTO_DISABLE_REALTIME = False

# Warning / Display constants
WARNING_SIZE = (1024 ** 2) * 10   #   10 Megabytes
LARGE_WARNING_STRING = '!!! WARNING !!!\nExcessively large files may be slow to search through\n\t'
FAILED_FILE_READ = 'Cannot read file <{}>\nUnknown encoding'
REGEX_PROMPT = '>>> REGEX ENTRY <<<'
LOCATION = 'Row {},  Column {}'


class Popup(tk.Toplevel):
    def __init__(self, master, *args, transient=True, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.blocking = transient

        if transient:
            self.resizable(False, False)
            self.transient(master)
            self.grab_set()
    def root_size(self):
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        return width, height, self.master.winfo_rootx(), self.master.winfo_rooty()
    def finalize(self):
        width, height, x_pos, y_pos = self.root_size()
        self.update()
        x_pos += int(width / 2 - self.winfo_width() / 2)
        y_pos += int(height / 2 - self.winfo_height() / 2)
        self.geometry(f'+{x_pos}+{y_pos}')
    def destroy(self):
        self.grab_release()
        tk.Toplevel.destroy(self)

class RegExTemplates(Popup):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title('Insert RegEx from Template')
    def build(self):
        self.item_frame = tk.Frame(self)
        self.item_frame.grid(row=0, column=0, sticky=N+S+E+W, padx=8, pady=8)

        populated_items = []
        for row, row_list in enumerate(REGEX_TEMPLATES_LAYOUT):
            for col, category_name in enumerate(row_list):
                try:
                    category_template = REGEX_TEMPLATES[category_name]
                except KeyError:
                    print(f'Warning: RegEx template <{category_name}> is undefined')
                    continue
                category_frame = tk.LabelFrame(self.item_frame, text=category_name, padx=16, pady=16)
                category_frame.grid(row=row, column=col, sticky=E+W, padx=16, pady=8)
                category_frame.columnconfigure(1, weight=1)
                for line_number, (title, regex) in enumerate(category_template.items()):
                    self.build_line_item(category_frame, line_number, title + ': ', regex)

                populated_items.append(category_name)

        for category_name in REGEX_TEMPLATES:
            if category_name not in populated_items:
                print(f'Warning: RegEx template <{category_name}> never placed')

        self.finalize()
    def build_line_item(self, master, row, title, regex):
        title_label = tk.Label(master, text=title, anchor=tk.E)
        title_label.grid(row=row, column=0, sticky=E+W)
        
        display = ttk.Entry(master)
        display.grid(row=row, column=1, sticky=E+W)

        display.insert('0', regex)
        display.state(DISABLED)

        insert_func = functools.partial(self.insert_regex, regex)
        insert = ttk.Button(master, text='Insert', command=insert_func, width=8)
        insert.grid(row=row, column=2, padx=4)
    def insert_regex(self, regex):
        # Calls the parent (expecting a insert_regex func) and adds the regex to the entry
        self.master.insert_regex(regex, update_gui=True)
        self.destroy()

class RegExDocs(Popup):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.geometry('800x800')
        self.title('RegEx guide (for Python 3 usage)')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
    def build(self):
        '''
        if pre_made:
            content = tk.Label(self, image=self.guide)
            content.pack(expand=True, fill=tk.BOTH)
            return
        '''
        bold_font = font.Font(font='TkFixedFont')
        bold_font.config(weight='bold')

        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0, sticky=N+S+E+W)

        syntax = ScrolledText(notebook)
        syntax.pack(fill=tk.BOTH, expand=True)
        notebook.add(syntax, text='Syntax')
        syntax.tag_config('heading', background='#DDDDDD', font=bold_font)
        syntax.tag_config('body', background='#EEEEEE')
        process_docs(syntax, SYNTAX_DOCS)
        
        flags = ScrolledText(notebook)
        flags.pack(fill=tk.BOTH, expand=True)
        notebook.add(flags, text='Flags')
        flags.tag_config('heading', background='#DDDDDD', font=bold_font)
        flags.tag_config('body', background='#EEEEEE')
        process_docs(flags, FLAGS_DOCS)

        source_string = 'Python 3 Docs: <https://docs.python.org/3/library/re.html>'
        taken_from = tk.Label(self, text=f'Adapted from {source_string}', anchor=tk.E)
        taken_from.grid(row=1, column=0, sticky=E+W)

        self.finalize()

class TextFromLink(Popup):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title('New page from URL')

    def build(self):
        self.build_link_entry()
        self.build_name_entry()
        self.build_status_box()
        self.build_ok_cancel()

        #self.link_var.set(r'https://httpbin.org/user-agent')
        self.link_var.set(r'https://demo.borland.com/testsite/stadyn_largepagewithimages.html')
        self.update_link()

        self.finalize()
    def build_link_entry(self):
        link_frame = ttk.Frame(self)
        link_frame.grid(row=0, column=0, sticky=E+W, padx=16, pady=16)

        link_label = ttk.Label(link_frame, text='Link: ')
        link_label.pack(side=tk.LEFT)
        self.link_var = tk.StringVar(self)
        link_entry = ttk.Entry(link_frame, textvariable=self.link_var)
        link_entry.bind('<Return>', self.download)
        link_entry.bind('<KeyRelease>', self.update_link)
        link_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        start = ttk.Button(link_frame, text='Download', command=self.download)
        start.pack(side=tk.LEFT)
    def build_name_entry(self):
        name_frame = ttk.Frame(self)
        name_frame.grid(row=1, column=0, sticky=E+W, padx=16)

        name_label = ttk.Label(name_frame, text='Tab name: ')
        name_label.pack(side=tk.LEFT)

        self.tab_name = tk.StringVar(self)
        self.name_entry = ttk.Entry(name_frame, textvariable=self.tab_name, width=32, state=DISABLED)
        self.name_entry.pack(side=tk.LEFT)
        self.name_entry.bind('<Return>', self.download)

        self.manual_name = tk.IntVar(self, value=0)
        manual_name = ttk.Checkbutton(name_frame, text='Manual', variable=self.manual_name,
                                      command=self.update_name_entry_state)
        manual_name.pack(side=tk.LEFT, padx=10)
    def build_progress_bar(self):
        self.progress = ttk.Progressbar(self, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky=E+W, padx=20, pady=20)
        self.progress.grid_remove()
    def build_status_box(self):
        status_frame = ttk.LabelFrame(self, text='Download Status')
        status_frame.grid(row=2, column=0, sticky=N+S+E+W, padx=20, pady=20)

        self.status = scrolledtext.ScrolledText(status_frame, height=12, width=100)
        self.status.pack(side=tk.TOP, padx=4, pady=4)
    def build_ok_cancel(self):
        ctrl_frame = tk.Frame(self, bg='light grey')
        ctrl_frame.grid(row=3, column=0, sticky=E+W)

        self.cancel_btn = ttk.Button(ctrl_frame, text='Cancel', command=self.destroy)
        self.cancel_btn.pack(side=tk.RIGHT, padx=8, pady=6)
        self.cancel_btn.bind('<Return>', self.destroy)

        self.ok_btn = ttk.Button(ctrl_frame, text='OK', command=self.accept)
        self.ok_btn.pack(side=tk.RIGHT, padx=0, pady=6)
        self.ok_btn.bind('<Return>', self.accept)
        self.ok_btn.state(DISABLED)
    
    def update_name_entry_state(self):
        state = ENABLED if self.manual_name.get() else DISABLED
        self.name_entry.state(state)
    def update_link(self, *args):
        automatic = not self.manual_name.get()
        if automatic:
            url = self.link_var.get()

            if len(url) > LINK_PAGE_NAME_LEN:
                last_30 = url[-(LINK_PAGE_NAME_LEN - 1):]
                new_tab_name = '...' + last_30
            else:
                new_tab_name = url

            self.tab_name.set(new_tab_name)

    def download(self, *args):
        self.ok_btn.state(DISABLED)
        self.cancel_btn.state(DISABLED)
        self.update()

        self.status.delete(START, END)

        url = self.link_var.get()
        text, good = download(url)
        self.page_text = text
        self.page_title = self.tab_name.get()

        size = len(text)
        kb_size = round(size / 1024, 2)

        # Only turn on the accept (ok) button if it worked
        if good:
            self.ok_btn.state(ENABLED)
            self.status.insert(END, 'Download complete\n\n')
            if size > WARNING_SIZE:
                self.status.insert(END, LARGE_WARNING_STRING)
            self.status.insert(END, f'Text Size: {kb_size} Kb')
            self.ok_btn.focus()
        else:
            self.status.insert(END, '!!! ERROR !!!\n\n')
            self.status.insert(END, text)
            self.ok_btn.state(DISABLED)

        self.cancel_btn.state(ENABLED)
    def accept(self, *args):
        # Calls the parent (expecting a add_page func) and adds the text to a new page
        self.master.add_page(text=self.page_text, title=self.page_title)
        self.destroy()

class HelpGuide(Popup):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title('Help guide on REMESH')
    def build(self):
        self.categories = ttk.Notebook(self)
        self.categories.pack(expand=True, fill=tk.BOTH)

        self.build_categories()
        self.finalize()
    def build_categories(self):
        for title, sub_titles in HELP_STRUCTURE:
            if isinstance(sub_titles, str):
                sub_titles = (sub_titles,)

            if sub_titles:

                # Build a sub-notebook with pages as frames
                sub_category = ttk.Notebook(self.categories)
                self.categories.add(sub_category, text=title)

                for sub_title in sub_titles:

                    # Add frame to second-level notebook
                    sub_cat_frame = ttk.Frame(sub_category, width=400, height=400)
                    sub_category.add(sub_cat_frame, text=sub_title)

                    #Populate frame with title-specific content
                    self.build_sub_category(sub_cat_frame, sub_title)
            else:

                # Build a sub-page that is just a frame (ex. 'About' page)
                cat_frame = ttk.Frame(self.categories, width=400, height=400)
                self.categories.add(cat_frame, text=title)

                #Populate frame with title-specific content
                self.build_sub_category(cat_frame, title)
    def build_sub_category(self, master, title):
        if title == HELP_ABOUT:
            name = ttk.Label(master, text='Nicholas C. Pandolfi', anchor=tk.CENTER)
            name.pack(expand=True, fill=tk.BOTH)

def text_popup(event, x_size=100, y_size=24):
    win = tk.Tk()
    win.overrideredirect(1)
    win.bind_all('<Leave>', lambda _: win.destroy())  # Remove popup when pointer leaves the window
    
    x_pos = event.x_root - int(x_size / 2)
    y_pos = event.y_root - int(y_size / 2)
    win.geometry(f'{x_size}x{y_size}+{x_pos}+{y_pos}')

    label = tk.Label(win, text="Coming Soon")
    label.pack(fill=tk.BOTH)

    win.mainloop()

# IDE's methods on top are GUI-heavy methods. On the bottom are functional-heavy methods

class IDE(tk.Frame):
    def __init__(self, *args, padx=6, pady=6, new_blank=False, auto_sash=True, title=STD_TITLE, **kwargs):
        super().__init__(*args, padx=padx, pady=pady, **kwargs)
        self.init_obj()
        self.configure()
        self.build()
        self.init_gui()
        if new_blank:
            self.add_page(text='')
        if auto_sash:
            self._auto_sash()

        # Launch the miniloop once the gui is built
        self.miniloop()
    def init_obj(self):
        ''' Initialize the 'global' variables for the gui '''
        # TODO theres a lot of junk in here. Need to go thru and delete many unused ones
        self.pages = []
        self.regex = ''
        self.prev_matches = {}
        self.prev_match_objects = []
        self.prev_group_list = []
        self.next_group_list = []
        self.last_pointer_index = None
        self.update_in_n_cycles = 0
        self.was_edited = False
        self.group_states = []
        self.hover_index = None
        self.hidden_tags = {}
        self.hover_active = False
        self.hover_previously_active = False
        self.grouping = []
        self.text_updated = True
        self.is_good = True
        self.is_executing = False
        self.leaving = False
        self.start_from_last = True
        self.realtime_tieback = None
        self.last_directory = os.getcwd()
        self.miniloop_tieback = None
        self.realtime_locked = False
        self.n_matches = 0
        self.update_font(family='Iosevka', size=16) # TODO Put this line of code somewhere else in future
    def init_gui(self):
        ''' Initialize widgets that the user interacts with -> set a default state FOR the user '''
        # Search control checkbuttons
        self.decompose_btn.state(['!alternate']) # Starts as an 'alternate' because no IntVar is assigned
        self.set_decomposed(state=False)
        self.realtime_var.set(1)

        # Search stats labels
        self.time.set(TIME_DISPLAY.format(0))
        self.matches_var.set(MATCHES_DISPLAY.format(0))
        self.steps_var.set(STEPS_DISPLAY.format(0))

        # Bottom bar
        self.wrap_text.set(1)
        self.editable_text.set(1)
        self.hover_focus_var.set(0)

        # Manual 'event' or 'callback' calls
        self.update()
        self.update_decompose()
        self.update_flags()
    def _auto_sash(self):
        '''
            A bit hack-ey, but schedule a task that will be eventually run once a Tk root has been
            created. The task will set the sash position of the window as far right as possible
            Must be called when root exists due to a strange bug I cannot figure out
        '''
        self.after(100, self._push_sash_right) # Wait 0.1s
    def miniloop(self):
        '''
            A multipurpose loop that is called 1/<MINILOOP_PERIOD> times per second
        '''
        # If the user checks the 'Hover Focus' checkbutton
        if self.hover_focus_var.get():
            self.hover_check()

        # Keep miniloop going by scheduling again
        self.miniloop_tieback = self.after(MINILOOP_PERIOD, self.miniloop)
    def stop_events(self):
        '''
            Stops all active scheduled events (realtime waiting and the miniloop tieback)
        '''
        # Cancel a realtime wait event
        if not isinstance(self.realtime_tieback, type(None)):
            self.after_cancel(self.realtime_tieback)

        # Cancel the miniloop
        if self.miniloop_tieback:
            self.after_cancel(self.miniloop_tieback)
    def periodic_update(self):
        '''
            Only force a gui update every <CYCLES_PER_UPDATE> cycles in the main searching/highlighting
            process loop. This is because <self.update()> is quite time consuming to call every cycle
        '''
        if self.update_in_n_cycles <= 0:
            self.update() # Force update of all gui changes
            self.update_in_n_cycles = CYCLES_PER_UPDATE
        else:
            self.update_in_n_cycles -= 1

    # FONT / STYLE / AESTHETICS
    def configure(self):
        # Set outtermost scaling factors
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Configure aesthetics and styles
        self.configure_font()
        self.configure_style()
    def configure_font(self):
        '''
            Configure fonts for use in the gui.
            Automatically picks from pre-approved list of monospace fonts
        '''
        self.bold_font = font.Font(font='TkFixedFont')
        self.bold_font.config(weight='bold')

        self.all_fonts = font.families()
        usable = []
        for family in self.all_fonts:
            if family in FONT_STYLES:
                usable.append(family)
        self.usable_mono_fonts = usable
    def configure_style(self):
        ''' Configure styles and themes '''
        self.style = ttk.Style()

        larger_font = new_font('TkDefaultFont', size_delta=3)
        page_ctrl_font = ('Consolas', 12, 'bold')
        smaller_font = new_font('TkDefaultFont', size_delta=-2)

        self.style.configure('bottomtab.TNotebook', tabposition='sw')
        self.style.configure('ctrl.TButton', font=page_ctrl_font)
        self.style.configure('small.TLabel', font=smaller_font)
        self.style.configure('heading.TLabel', font=larger_font)
    
    # BUILD GUI OBJECTS
    def build(self):
        self.build_toolbar()
        self.build_panes()
        self.build_tree()
        self.build_analysis()
        self.build_debug()
        self.build_bottom()
    def build_toolbar(self):
        # FRAME THAT HOLDS ALL TOP BAR CONTROLS
        self.ctrl_frame = ttk.Frame(self)
        self.ctrl_frame.grid(row=0, column=0, columnspan=3, sticky=W+E, padx=3, pady=2)
        self.ctrl_frame.columnconfigure(4, weight=1)

        self.build_toolbar_ctrl()  #  Close / left / right
        self.build_toolbar_new_page()  #  Blank page / From file / From Link Buttons
        self.build_toolbar_searcher_opts()  #  Realtime / decompose
        self.build_toolbar_groups()  #  Color palette when highlighting
        self.build_toolbar_entry()  #  RegEx entry box and associated controls
        self.build_toolbar_stats()  #  Operation time & Matches Display
        self.build_toolbar_btns()  #  Clear matches / Regex template & guide
    def build_toolbar_ctrl(self):
        page_ctrl_frame = tk.LabelFrame(self.ctrl_frame, text='Tab Control')
        page_ctrl_frame.rowconfigure(0, weight=1)
        page_ctrl_frame.grid(row=0, column=0, sticky=N+S, padx=2, pady=2)

        self.close_btn = ttk.Button(page_ctrl_frame, text='X', command=self.remove_selected,
                                    width=3, style='ctrl.TButton')
        self.close_btn.grid(row=0, column=0, sticky=N+S+E+W, pady=6, padx=2)

        ttk.Frame(page_ctrl_frame, width=8).grid(row=0, column=1)

        self.move_left_btn = ttk.Button(page_ctrl_frame, text='<', command=self.move_left,
                                        width=3, style='ctrl.TButton')
        self.move_left_btn.grid(row=0, column=2, sticky=N+S+E+W, pady=6, padx=2)

        self.move_right_btn = ttk.Button(page_ctrl_frame, text='>', command=self.move_right,
                                         width=3, style='ctrl.TButton')
        self.move_right_btn.grid(row=0, column=3, sticky=N+S+E+W, pady=6, padx=2)
    def build_toolbar_new_page(self):
        add_frame = tk.LabelFrame(self.ctrl_frame, text=' + New Page ')
        add_frame.grid(row=0, column=1)

        add_blank_btn = ttk.Button(add_frame, text='Blank\nPage', width=6, command=self._new_blank_page)
        add_blank_btn.pack(side=tk.LEFT)

        sep = tk.Label(add_frame, text='OR', width=3, anchor=tk.CENTER)
        sep.pack(side=tk.LEFT)

        from_frame = tk.LabelFrame(add_frame, text=' From ')
        from_frame.pack(side=tk.LEFT)

        add_file_btn = ttk.Button(from_frame, text='File', width=6, command=self._new_page_from_file)
        add_file_btn.pack(side=tk.LEFT, padx=1, pady=1)

        add_link_btn = ttk.Button(from_frame, text='URL', width=6, command=self._new_page_from_link)
        add_link_btn.pack(side=tk.LEFT, padx=1, pady=1)
    def build_toolbar_searcher_opts(self):
        opts_frame = tk.LabelFrame(self.ctrl_frame, text='Options')
        opts_frame.grid(row=0, column=2, padx=4, sticky=N+S)

        # DECOMPOSE MATCHES TOGGLE
        self.decompose_btn = ttk.Checkbutton(opts_frame, text='Decompose', command=self.update_decompose)
        self.decompose_btn.pack(side=tk.TOP, anchor=W)

        # REALTIME SEARCHING TOGGLE
        self.realtime_var = tk.IntVar(self)
        realtime_checkbox = ttk.Checkbutton(opts_frame, text='Realtime',
                                variable=self.realtime_var, command=self.update_realtime)
        realtime_checkbox.pack(side=tk.TOP, anchor=W)
    def build_toolbar_groups(self):
        self.group_frame = tk.LabelFrame(self.ctrl_frame, text='Group Settings', padx=4)
        self.group_frame.grid(row=0, column=3, sticky=N+S, padx=4)

        # Create color labels and grid them to the palette frame
        self.palette_widgets = []
        palette_frame = ttk.Frame(self.group_frame)
        palette_frame.grid(row=0, column=0, columnspan=2, sticky=E+W)
        for g_no, color in enumerate(COLOR_QUEUE):
            palette_frame.columnconfigure(g_no, weight=1)
            label = tk.Label(palette_frame, text=str(g_no), bg=color, width=2)
            label.grid(column=g_no, row=0, sticky=E+W)
            self.palette_widgets.append(label)

        # Create menu object
        self.group_menu = tk.Menu(self, tearoff=1, tearoffcommand=self.groups_tearoff, title='Groups')

        # Create an empty group button -> to be populated later
        self.groups_button = ttk.Menubutton(self.group_frame, menu=self.group_menu, text='Groups')
        self.groups_button.grid(row=1, column=0, sticky=E+W)

        # Color configuration launcher (choose colors)
        color_button = ttk.Button(self.group_frame, text='Colors', command=self.change_colors)
        color_button.grid(row=1, column=1, sticky=E+W)
    def build_toolbar_entry(self):
        entry_frame = tk.Frame(self.ctrl_frame, padx=4, pady=4)
        entry_frame.grid(row=0, column=4, sticky=E+W+N+S)
        entry_frame.columnconfigure(0, weight=1)
        entry_frame.rowconfigure(1, weight=1)

        self.progress_var = tk.IntVar(self, value=0)
        progress_bar = ttk.Progressbar(entry_frame, variable=self.progress_var, mode='determinate')
        progress_bar.grid(row=0, column=0, sticky=E+W, padx=1, pady=1)

        self.regex_status = tk.StringVar(self)
        inline_label = tk.Label(entry_frame, textvariable=self.regex_status, anchor=tk.W, width=12)
        inline_label.grid(row=0, column=1)

        self.flag_btns = []
        for column, flag in enumerate(FLAGS):
            state = tk.IntVar(self)
            state.set(0)
            flag_btn = tk.Checkbutton(entry_frame, text=flag, command=self.update_flags,
                                      indicatoron=False, borderwidth=1, variable=state,
                                      font=("TkDefaultFont", 7), selectcolor='light green')
            flag_btn.grid(row=0, column=column+2, padx=1, pady=1, sticky=N+S+E+W)
            flag_btn.state = state
            self.flag_btns.append(flag_btn)

        self.regex_var = tk.StringVar(self)
        self.regex_entry = PromptedEntry(entry_frame, prompt=REGEX_PROMPT, font=("Consolas", 18),
                                         textvariable=self.regex_var)
        self.regex_entry.grid(row=1, column=0, columnspan=len(FLAGS)+2, sticky=N+S+E+W, padx=1, pady=1)
        
        self.regex_entry.bind('<KeyRelease>', self.update_pattern)
        self.regex_entry.bind('<Return>', self.search)
        self.regex_entry.unbind_all("<<NextWindow>>")
        self.regex_entry.unbind_all("<<PrevWindow>>")
        self.regex_entry.bind('<Tab>', self.focus_next)
        self.regex_entry.bind('<Shift-Tab>', self.focus_prev)
        self.regex_entry.bind('<Escape>', self.clear_all)

        self.search_button = ttk.Button(entry_frame, text='Search', width=7, command=self.search)
        self.search_button.grid(row=0, rowspan=2, column=column+3, sticky=N+S)
    def build_toolbar_stats(self):
        stats_frame = tk.LabelFrame(self.ctrl_frame, text='Op. Stats')
        stats_frame.grid(row=0, column=5, padx=4, sticky=N+S)

        self.time = tk.StringVar(self)
        time_label = ttk.Label(stats_frame, width=14, textvariable=self.time, style='small.TLabel')
        time_label.pack(side=tk.TOP, anchor=W)

        self.matches_var = tk.StringVar(self)
        matches_label = ttk.Label(stats_frame, width=14, textvariable=self.matches_var, style='small.TLabel')
        matches_label.pack(side=tk.TOP, anchor=W)

        self.steps_var = tk.StringVar(self)
        steps_label = ttk.Label(stats_frame, width=14, textvariable=self.steps_var, style='small.TLabel')
        steps_label.pack(side=tk.TOP, anchor=W)
    def build_toolbar_btns(self):
        btn_frame = ttk.Frame(self.ctrl_frame)
        btn_frame.grid(row=0, column=6)
        btn_frame.rowconfigure(0, weight=1)
        btn_frame.rowconfigure(1, weight=1)

        # TEMPLATE HELPER
        template_launcher = functools.partial(self.launch_popup, RegExTemplates)
        template_btn = ttk.Button(btn_frame, text='Regex\nTemplates', command=template_launcher)
        template_btn.grid(row=0, column=0, rowspan=2, sticky=E+W+N+S)

        # CLEAR BUTTON
        clear_btn = ttk.Button(btn_frame, text='Clear\nResults', command=self.clear_all)
        clear_btn.grid(row=0, column=1, rowspan=2, sticky=E+W+N+S)

        # HELP DIALOG
        help_launcher = functools.partial(self.launch_popup, HelpGuide, transient=False)
        help_btn = ttk.Button(btn_frame, text='Help', command=help_launcher)
        help_btn.grid(row=0, column=2, sticky=E+W+N+S)

        # RegEx DOCUMENTATION DIALOG
        docs_launcher = functools.partial(self.launch_popup, RegExDocs, transient=False)
        guide_btn = ttk.Button(btn_frame, text='Regex Docs', command=docs_launcher)
        guide_btn.grid(row=1, column=2, sticky=E+W+N+S)
    def build_panes(self):
        self.main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=8)
        self.main_pane.grid(row=1, column=0, rowspan=2, columnspan=2, sticky=N+S+E+W, padx=2, pady=2)

        self.pagebook = ttk.Notebook(self.main_pane)
        self.main_pane.add(self.pagebook)
        # TODO: Put into help -> CTRL+TAB->forward  CTRL+SHFT+TAB->reverse
        self.pagebook.enable_traversal()

        tool_frame = tk.Frame(self.main_pane)
        self.main_pane.add(tool_frame)
        self.main_pane.paneconfig(tool_frame, minsize=MIN_RIGHT_PANE_SIZE)

        self.tree_status = tk.StringVar(self)
        tree_status = tk.Label(tool_frame, textvariable=self.tree_status, anchor='c')
        tree_status.pack(fill=tk.X, side=tk.TOP)

        self.toolbook = ttk.Notebook(tool_frame, style='bottomtab.TNotebook')
        self.toolbook.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)
    def build_tree(self):
        self.view = ScrolledTree(self.toolbook, xbar=False)
        self.toolbook.add(self.view, text='Matches')

        # Navigation and match selection bindings
        self.view.tree.bind("<Button-1>", self.tree_select)
        self.view.tree.bind("<Return>", self.tree_select)
        self.view.tree.bind("<Button-3>", self.show_match_info)
        self.view.tree.bind("<Escape>", self.clear_all)

        # Building the column labels for the treeview and set spacing/rules
        self.view.tree['columns'] = ('span', 'txt')
        self.view.tree.column('#0', width=60, minwidth=60, anchor='c', stretch=tk.NO)
        self.view.tree.heading('#0', text='Match #')
        self.view.tree.column('span', width=90, minwidth=90, anchor='c')
        self.view.tree.heading('span', text='Span')
        self.view.tree.column('txt', width=90, anchor=W)
        self.view.tree.heading('txt', text='Text')
    def build_debug(self):
        # Frame owned by the notebook directly
        debug_frame = ttk.Frame(self.toolbook)
        debug_frame.columnconfigure(0, weight=1)
        debug_frame.rowconfigure(0, weight=1)
        debug_frame.rowconfigure(1, weight=1)
        self.toolbook.add(debug_frame, text='Debug')

        # Labelframe dealing with the first portion of the debug string (instructions)
        code_heading = ttk.Label(debug_frame, text='Parsed Instructions', style='heading.TLabel')
        code_frame = ttk.LabelFrame(debug_frame, labelwidget=code_heading)
        code_frame.grid(row=0, column=0, sticky=N+S+E+W, padx=8, pady=8)
        self.debug_code_view = ScrolledText(code_frame, hbar=True, wrap=tk.NONE)
        self.debug_code_view.pack(expand=True, fill=tk.BOTH)

        # Labelframe dealing with the second portion of the debug string (steps)
        steps_heading = ttk.Label(debug_frame, text='Detailed Steps', style='heading.TLabel')
        steps_frame = ttk.LabelFrame(debug_frame, labelwidget=steps_heading)
        steps_frame.grid(row=1, column=0, sticky=N+S+E+W, padx=8, pady=8)
        self.debug_steps_view = ScrolledText(steps_frame, hbar=True, wrap=tk.NONE)
        self.debug_steps_view.pack(expand=True, fill=tk.BOTH)
    def build_analysis(self):
        # TODO : Flesh this tab out
        self.analysis_view = ScrolledText(self.toolbook)
        self.toolbook.add(self.analysis_view, text='Analysis')
    def build_bottom(self):
        # Container for all bottom widget sub-elements
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(row=3, column=0, columnspan=2, sticky=E+W)

        # Build sub-elements
        self.build_bottom_fonts()
        ttk.Frame(self.bottom_frame, width=16).pack(side=tk.LEFT) # Spacer frame

        self.build_bottom_opts()
        ttk.Frame(self.bottom_frame, width=24).pack(side=tk.LEFT) # Spacer frame

        self.build_bottom_status()
    def build_bottom_fonts(self):
        font_menu = tk.Menu(self, tearoff=0)
        for offset, font_type in enumerate(self.usable_mono_fonts):
            callback = functools.partial(self.update_font_family, offset)
            font_menu.add_command(label=font_type, command=callback)
        font_menu.add_separator()
        font_menu.add_cascade(label='Other Font')

        ttk.Label(self.bottom_frame, text='Font: ').pack(side=tk.LEFT)
        self.font_family = tk.StringVar(self, value=self._text_font[0])
        family_box = ttk.Menubutton(self.bottom_frame, menu=font_menu, textvariable=self.font_family)
        family_box.pack(side=tk.LEFT)

        ttk.Frame(self.bottom_frame, width=16).pack(side=tk.LEFT) # Spacer frame

        size_menu = tk.Menu(self, tearoff=0)
        for size in FONT_SIZES:
            callback = functools.partial(self.update_font_size, size)
            size_menu.add_command(label=str(size), command=callback)

        ttk.Label(self.bottom_frame, text='Size: ').pack(side=tk.LEFT)
        self.font_size = tk.IntVar(self, value=self._text_font[1])
        size_box = ttk.Menubutton(self.bottom_frame, menu=size_menu, width=2, textvariable=self.font_size)
        size_box.pack(side=tk.LEFT)
    def build_bottom_opts(self):
        self.wrap_text = tk.IntVar(self, value=0)
        text_wrap_check = ttk.Checkbutton(self.bottom_frame, text='Wrap Text', variable=self.wrap_text,
                                          command=self.update_wrap_text)
        text_wrap_check.pack(side=tk.LEFT)

        ttk.Frame(self.bottom_frame, width=16).pack(side=tk.LEFT) # Spacer frame

        self.editable_text = tk.IntVar(self, value=0)
        text_edit_check = ttk.Checkbutton(self.bottom_frame, text='Editable', variable=self.editable_text,
                                          command=self.update_editable_text)
        text_edit_check.pack(side=tk.LEFT)

        ttk.Frame(self.bottom_frame, width=16).pack(side=tk.LEFT) # Spacer frame

        self.hover_focus_var = tk.IntVar(self, value=0)
        hover_focus_check = ttk.Checkbutton(self.bottom_frame, text='Hover Focus', variable=self.hover_focus_var,
                                            command=self.update_hover_focus)
        hover_focus_check.pack(side=tk.LEFT)
    def build_bottom_status(self):
        self.cursor_var = tk.StringVar(self)
        cursor_label = tk.Label(self.bottom_frame, textvariable=self.cursor_var)
        cursor_label.pack(side=tk.LEFT)

        self.status_var = tk.StringVar(self)
        status_label = tk.Label(self.bottom_frame, textvariable=self.status_var, anchor=tk.E, width=50)
        status_label.pack(side=tk.RIGHT)
    def launch_popup(self, popup_subclass, *args, **kwargs):
        """
            Launches a class that inherits from the Popup class (defined above)
            Expects a .build method to be present, and a .grab_set method to be called ahead of time
            If there is an exception raised in the popup, we will first give control back to parent
                then re-raise the exception, so the program can be closed easily
        """
        try:
            popup = popup_subclass(self, *args, **kwargs)
            popup.build()
        except Exception:
            if popup.blocking:
                popup.grab_release()
            raise

    # PAGE CONTROL
    def add_page(self, *, text=None, file=None, title='*'):
        '''
            Add a scrollable text page to the main pane of the application
            must specify a <text> string or a filename in the <file> parameter
            Give the page a <title> too. Defaults to '*'
        '''
        if not file and not isinstance(text, str):
            raise ValueError("Must have either 'file' or 'text' parameters specified")
        elif file and isinstance(file, str) and os.path.exists(file):
            with open(file, encoding='utf-8') as handle:
                try:
                    content = handle.read()
                except UnicodeDecodeError:
                    msg = FAILED_FILE_READ.format(get_name(file))
                    notify = messagebox.showinfo('Failed file read', msg)
                    return
        elif isinstance(text, str):
            content = text
        else:
            raise ValueError("No content detected, cannot add page without content")

        wrap = tk.CHAR if self.wrap_text.get() else tk.NONE
        page = ScrolledText(self.pagebook, hbar=True, wrap=wrap)
        page.bind('<Control-MouseWheel>', self.zoom_font)
        page.bind('<ButtonRelease-1>', self.update_location)
        page.bind('<Escape>', self.clear_all)

        page.bind('<Button-1>', self.page_mouse_press)
        page.bind('<Key>', self.page_key_press)

        for arrow_key in ('Right', 'Left', 'Up', 'Down'):
            page.bind(f'<KeyRelease-{arrow_key}>', self.update_location)

        self.create_tags(page)
        self.pagebook.add(page, text=f' {title} ')
        self.pagebook.select(len(self.pages))
        page.insert(tk.END, content)
        self.pages.append(page)
        self.push_font()

        # Enable or disable editing based on 'editable' checkbutton on bottom of page
        editable = 'normal' if self.editable_text.get() else 'disabled'
        page.config(state=editable)
    def remove_selected(self):
        total_tabs = len(self.pages)
        if total_tabs == 1:
            return
        selected = self.pagebook.select()
        index = self.pagebook.index(selected)
        self.pagebook.forget(selected)
        del self.pages[index]
    def move_left(self, *args):
        total_tabs = len(self.pages)
        if total_tabs == 1:
            return
        selected = self.get_selected_page()

        index = self.pagebook.index(selected)
        if index == 0:
            return # Already as left as can go
        left_index = index - 1

        title = self.pagebook.tab(selected)['text']
        child = self.pages.pop(index)
        self.pages.insert(left_index, child)

        self.pagebook.forget(selected)
        self.pagebook.insert(left_index, child, text=title)
        self.pagebook.select(left_index)
    def move_right(self, *args):
        total_tabs = len(self.pages)
        if total_tabs == 1:
            return
        selected = self.get_selected_page()

        index = self.pagebook.index(selected)
        if index == total_tabs - 1:
            return # Already as right as can go
        right_index = index + 1

        title = self.pagebook.tab(selected)['text']
        child = self.pages.pop(index)
        self.pages.insert(right_index, child)

        self.pagebook.forget(selected)
        if right_index == total_tabs - 1:
            destination = 'end'
        else:
            destination = right_index
        self.pagebook.insert(destination, child, text=title)
        self.pagebook.select(right_index)
    def create_tags(self, page, full_compliment=False):
        # Highlighting tags
        for color in (SINGLE_COLOR,) + COLOR_QUEUE:
            fg = invert_hex(color) if full_compliment else 'black'
            sel_fg = color if full_compliment else 'white'
            bg = color
            sel_bg = invert_hex(color)

            page.tag_config(color, background=bg, foreground=fg,
                            selectforeground=sel_fg, selectbackground=sel_bg)
            page.tag_raise(color)

        # Focus / Hover tags
        page.tag_config('match')
        page.tag_bind('match', '<Leave>', self.clear_hover) # Only a bind to pointer LEAVING the match
        page.tag_bind('match', '<Button-3>', self.select_popup)
        page.tag_lower('match')
        page.tag_config('hover', font=('Iosevka', 16, 'bold')) # TODO dynamically define this pls...
        page.tag_raise('hover')
        page.tag_config('focus', foreground='#FF0000', font=self.bold_font) # TODO : Get rid of the hard define
        page.tag_raise('focus')
    def get_selected_page(self):
        selected = self.pagebook.select()
        index = self.pagebook.index(selected)
        obj = self.pages[index]
        return obj
    def select_tab(self, tab_no=1):
        # Selects the tab <tab_no> (index starting at 1, not 0)
        self.pagebook.select(self.pages[tab_no - 1])
    def get_text(self):
        page = self.get_selected_page()
        text = page.get(START, 'end-1c')
        return text
    def page_key_press(self, event):
        if event.char and not self.was_edited:
            self.was_edited = True
    def page_mouse_press(self, event):
        page = self.get_selected_page()
        position = page.index(tk.CURRENT)
        tag_range = self.determine_if_tag(page, 'match', position)
        self._remove_tag(page, 'focus')
        if tag_range:
            page.tag_add('focus', *tag_range)
    def _new_blank_page(self):
        # Add a new page with '*' title and no text
        self.add_page(text='')
    def _new_page_from_file(self):
        filetypes = (('All', '*.*'),)

        if self.start_from_last:
            start = self.last_directory
        else:
            start = os.getcwd()

        path = filedialog.askopenfilename(initialdir=start, title='Open a file', filetypes=filetypes)
        if not path:
            return None # User exit here

        self.last_directory = get_dir(path)
        self.add_page(file=path, title=get_name(path))

        #if checksize:
        #    size = os.path.getsize(path)
        #    if size > 1024**2 * 5: # File size is bigger than 5 Megabytes
        #        string_size = integrate.format_size(size, order=2, rnd=1)
        #        response = messagebox.askyesno("Warning: Large File Size",
        #            f"{path}\nIs {string_size} in size. Continue anyway?")
        #        if not response:
        #            return None # User exit here
    def _new_page_from_link(self):
        # Hand full responsibility over to a popup widget
        self.launch_popup(TextFromLink)

    # GUI STATUS CONTROL
    def setup_progress(self, total, steps=PROGRESS_STEPS):
        self.n_total = total
        self.n_steps = steps
        self.progress = 0
        self.print_at = 0
    def _reset_entry_bg(self, *args):
        # Only to be called from a scheduled TCL task
        self.regex_entry['bg'] = 'SystemWindow'
    def _remove_tag(self, page, tag):
        # Removes all occurences of <tag> in the <page>
        tag_range = page.tag_ranges(tag)
        for start, end in zip(tag_range[::2], tag_range[1::2]):
            page.tag_remove(tag, start, end)
    def _hide_tag(self, page, tag):
        # Removes all occurences of <tag> in the <page>
        self.hidden_tags[tag] = []
        tag_range = page.tag_ranges(tag)
        for start, end in zip(tag_range[::2], tag_range[1::2]):
            tag_data = (tag, start, end)
            page.tag_remove(*tag_data)
            self.hidden_tags[tag].append(tag_data)
    def _show_tag(self, page, tag):
        for tag_data in self.hidden_tags[tag]:
            page.tag_add(*tag_data)
        del self.hidden_tags[tag]
    def _push_sash_right(self):
        self.main_pane.update()
        self.main_pane.sash_place(0, 100000, 1)
    def insert_regex(self, regex, update_gui=True):
        ''' User-facing api func to insert regex into entry automatically '''

        # Put the regex into the user entry field
        self.regex_entry.insert_text(regex)

        # Update the internal objects regarding the pattern entered (if <update_gui>)
        if update_gui:
            self.update_pattern()
    def check_flag(self, flag_name):
        if flag_name not in FLAGS:
            raise ValueError(f'Flag <{flag_name}> not recognized')

        flag_no = FLAGS.index(flag_name)
        button = self.flag_btns[flag_no]
        button.invoke()

    # SELECTIVE GROUP FUNCTIONS
    def get_group_states(self):
        group_states = [(True if var.get() else False) for var in self.group_states]
        return group_states
    def toggle_groups(self, group_no=None):
        ''' Called when a group is toggled using the group-select menu in the decompose palette '''

        # When group selection is teared off and decompose is dechecked but a command is pressed
        if not self.is_decomposed():
            return

        # Run thru the group states. If all are checked, remove the 'half check' state
        for state in self.get_group_states():
            if not state:
                self.decompose_btn.state(['alternate'])
                break
        else:
            self.decompose_btn.state(['!alternate'])

        # TODO Make it an actual remarkup
        if self.realtime_var.get() and not isinstance(group_no, type(None)):
            self.remarkup_group(group_no, self.get_group_states()[group_no])
    def update_group_list(self):
        # Clear the old groups from the group-menu
        delete_index = (0, len(self.prev_group_list))
        self.group_menu.delete(*delete_index)

        # Determine groups in the new pattern
        self.next_group_list = self.pattern['group-ids']

        # Add the new groups to the group-menu
        self.group_states = []
        for group_index, next_group in enumerate(self.next_group_list):

            group_state = tk.IntVar(value=1)
            self.group_states.append(group_state)

            group_callback = functools.partial(self.toggle_groups, group_index)

            # Format the group name to differentiate between named groups and just numbers
            try:
                int(next_group)
                label = f'  Group:  #{next_group}'
            except Exception:
                label = f'  Group:  <{next_group}>'
            label = label.ljust(24)

            # Add the checkbutton widget to the menu
            self.group_menu.add_checkbutton(label=label, command=group_callback,
                                            variable=group_state)

        # Record the newest groupings to be referenced next time pattern is updated
        self.prev_group_list = self.next_group_list
    def groups_tearoff(self, parent, child):
        window_name = parent + child
        parent_window = self.nametowidget(parent)
        # TODO get the handle of the tearoff window and control size and position here
    def remarkup_group(self, group_no, active):
        page = self.get_selected_page()
        group_tag_name = GET_COLOR(group_no)

        if not active:
            self._hide_tag(page, group_tag_name)
        else:
            if not self.was_edited: # If the text was edited, force a search
                self._show_tag(page, group_tag_name)
            else:
                del self.hidden_tags[group_tag_name]
                self.search()
                self.was_edited = False

    # SPECIAL WINDOWS
    def _coming_soon(self, title):
        help_text = 'Coming soon'
        popup = messagebox.showinfo(title, help_text)
    def change_colors(self):
        self._coming_soon('Color Changer')

    # FOCUS AND TREE SELECT
    def tree_select(self, event):
        if event.char == '??':
            item = self.view.tree.identify('item', event.x, event.y)
        elif event.char == '\r':
            try:
                # Try to get the selection
                item = self.view.tree.selection()[0]
            except IndexError:
                return

        name = self.view.tree.item(item, 'text')
        if not name:
            self.clear_focus()
            return # Exit if anything other than a match listing was selected

        # Extract only the number portion of the match listing
        try:
            n = int(name)
        except ValueError:
            n = int(name[:-1])

        self.text_focus(n, tag=True)
    def show_match_info(self, event):
        item = self.view.tree.identify('item', event.x, event.y)
        name = self.view.tree.item(item, 'text')
        try:
            n = int(name)
            sub_group = False
        except ValueError:
            n = int(name[:-1])
            sub_group = name[-1]
            sub_index = string.ascii_lowercase.index(sub_group) + 1

        match_obj = self.prev_match_objects[n - 1]

        if not sub_group:
            text = match_obj.group(0)
        else:
            text = match_obj.group(sub_index)
        #start_index = INDEX_TEMPLATE.format(span[0])

        info = f'Text: "{text}"'
        messagebox.askokcancel(f'Match  #{name}  Details', info)
    def get_focus_text(self):
        page = self.get_selected_page()
        focus_ranges = page.tag_ranges('focus')

        # If no focued text, return. If error, raise
        if len(focus_ranges) < 2:
            return ''
        elif len(focus_ranges) > 2:
            raise ValueError("Error: More than one focued entry")

        # Get the 'focus' tag span and then the text from the <page.get> func
        focus_start = focus_ranges[0].string
        focus_end = focus_ranges[1].string
        focus_index = (focus_start, focus_end)
        focus_text = page.get(*focus_index)
        return focus_text
    def text_focus(self, match_no, tag=True):
        '''
            Called by tree_select function and search function to focus on specific text
            Scrolls to see text (if out of range) 
        '''
        match = self.matches['match'][match_no - 1][0]

        page = self.get_selected_page()
        span = match[1]
        start_index = INDEX_TEMPLATE.format(span[0])
        page.see(start_index)
        full_index = format_index(span)

        if tag:
            self._remove_tag(page, 'focus')
            page.tag_add('focus', *full_index)
    def focus_next(self, *args):
        '''
            Focus on next match from the one currently selected.
            If none are selected, start at first
        '''
        print('Next')
        pass
    def focus_prev(self, *args):
        '''
            Focus on previous match from the one currently selected.
            If none are selected, start at last
        '''
        print('Previous')
        pass
    def clear_focus(self):
        ''' Clear the selected item in the treeview when clicking outside of a valid entry '''
        try:
            # TODO error when right-clicking in the header columns of the treeview
            item = self.view.tree.selection()
            self.view.tree.selection_remove(item)
        except IndexError:
            # Skeleton to catch this error if deemed appropriate in the future
            raise
    def clear_hover(self, *args):
        ''' Deactivate the hover flag (mouse pointer outside of 'match' tag) '''
        if self.hover_index:
            self.get_selected_page().tag_remove('hover', *self.hover_index)
            self.hover_index = None
    def determine_if_tag(self, page, tag, position):
        '''
            Determine if the mouse is hovering over a specific <tag>
            If not, return False. If so, return the full range of the <tag> match
        '''
        # Not hovering over the particular tag
        if tag not in page.tag_names(position):
            return False # Return immediately to conserve processing power

        # Using the current <row.column> index, find the prev and next match range
        prev_range = page.tag_prevrange(tag, position)
        next_range = page.tag_nextrange(tag, position)

        # Determine which one to use as the selected tag range
        # TODO: What if one match starts where another ends and user clicks inbetween ? Defaults to...?
        if not prev_range:
            # Hovered over first char of first match
            tag_range = next_range
        elif next_range and next_range[0] == position:
            # Hovered over first char of non-first match
            tag_range = next_range
        else:
            # Hovered over middle of any match
            tag_range = prev_range

        return tag_range
    def hover_check(self):
        ''' Called every mini-loop period. If mouse is over a 'match' tag -> hover-select it '''

        # Get selected page AND the 'row.column' index of mouse pointer
        page = self.get_selected_page()
        position = page.index(tk.CURRENT)

        # If index was not changed from last cycle, skip this cycle (saves processing power)
        if self.last_pointer_index and position == self.last_pointer_index:
            return
        self.last_pointer_index = position

        # We know that we are in a 'match' tag, now to find the range of it
        tag_range = self.determine_if_tag(page, 'match', position)
        if not tag_range: # Not hovering over a match
            return

        # Still hovering over same tag, exit function, do nothing
        if self.hover_index and tag_range == self.hover_index:
            return

        # Remove previous hover tag (if there is one)
        if not isinstance(self.hover_index, type(None)):
            page.tag_remove('hover', *self.hover_index)

        # Assign and set new hover tag
        self.hover_index = tag_range
        page.tag_add('hover', *self.hover_index)
    def select_popup(self, event):
        ''' Spawn a popup when the user right-clicks on a match in the text page '''
        print(self.get_focus_text())
        text_popup(event) # TODO : Flesh this out with all the juicy data

    # < identify these >
    def check_regex(self, pattern):
        '''
            Do a throw-away compile of the regex pattern to determine if it is valid
            If it is not valid, a re.error is raised and caught.
            Returns a bool True/False for 'is_good' status
        '''
        try:
            re.compile(pattern)
        except re.error:
            is_good = False
        else:
            is_good = True
        return is_good
    def disable_realtime(self):
        #TODO currently not used. Do we still want to implement this?
        self.realtime_var.set(0)
    def is_decomposed(self):
        ''' Determine decomposed state. Return as a bool True/False '''
        state = 'selected' in self.decompose_btn.state()
        return state
    def set_decomposed(self, state):
        ''' API function to set the decompose checkbutton to a particular <state> '''
        self.decompose_btn.state(['selected' if state else '!selected'])

    # UPDATE GUI OBJECTS TODO: make this section only 'callbacks' directly from widgets
    def update_progress(self):
        self.progress += 1
        coeff = self.progress / self.n_total
        status = int(coeff * self.n_steps)
        if status > self.print_at:
            self.print_at = status
            prog = coeff * 100
            self.progress_var.set(prog)
            #str_prog = str(round(prog, 0)).zfill(8)
            #self.status_var.set(f'Progress Percentage: {str_prog}%')
    def update_decompose(self, *args):
        if self.is_decomposed():
            # Throw group palette on screen and update it
            self.group_frame.grid()
            self.toggle_groups() # Necessary to update the check button
        else:
            self.group_frame.grid_remove()
            self.decompose_btn.state(['!alternate'])

        self.search() # TODO this is already called in the toggle_group. and remember -> only remark it
    def update_realtime(self, *args):
        if self.realtime_var.get():
            self.search()
        else:
            if self.realtime_locked:
                # Realtime is off, but a task is scheduled -> cancel it
                self._cancel_realtime()
    def update_pattern(self, *args):
        if args and repr(args[0].char) == '\r':
            return # Return immediately if the entry key was released -> Delegate to 'search'

        regex = self.regex_var.get()
        if not regex or regex == REGEX_PROMPT:
            self.clear_all()

        #  < empty >    <     no change     >
        if not regex or (regex == self.regex):
            #self.regex_entry['fg'] = 'black'
            self.regex = regex
            return

        self.is_good = self.check_regex(regex)
        if self.is_good:
            self.regex_entry['fg'] = 'black'
        else:
            self.regex_entry['fg'] = 'red'
            return

        # Push new data to buffer if the new regex is error-free
        self.regex = regex
        self.pattern = process_pattern(self.regex, self.flag_obj)
        self.update_group_list()
        self.update_debug()
        self.update_steps_display()

        if self.realtime_var.get():
            self._realtime_scheduler()
    def update_debug(self):
        debug_code, debug_steps = self.pattern['debug'].split('\n\n')

        self.debug_code_view.config(state='normal')
        self.debug_code_view.delete('1.0', tk.END)
        self.debug_code_view.insert(tk.END, debug_code)
        self.debug_code_view.config(state='disabled')

        self.debug_steps_view.config(state='normal')
        self.debug_steps_view.delete('1.0', tk.END)
        self.debug_steps_view.insert(tk.END, debug_steps)
        self.debug_steps_view.config(state='disabled')
    def update_steps_display(self):
        n_steps = self.pattern['steps']
        self.steps_var.set(STEPS_DISPLAY.format(n_steps))
    def update_flags(self, *args):
        self.flags = {}
        self.flag_obj = 0 # Why is '0' the default ?
        for flag_no, flag_btn in enumerate(self.flag_btns):
            state = flag_btn.state.get()
            flag_name = FLAGS[flag_no]
            self.flags[flag_name] = state
            if state:
                if flag_name == 'IGNORECASE':
                    re_flag = re.IGNORECASE
                elif flag_name == 'MULTILINE':
                    re_flag = re.MULTILINE
                elif flag_name == 'DOTALL':
                    re_flag = re.DOTALL
                elif flag_name == 'VERBOSE':
                    re_flag = re.VERBOSE
                elif flag_name == 'ASCII':
                    re_flag = re.ASCII
                else:
                    raise ValueError(f"Flag <{flag_name}> not valid")
                self.flag_obj |= re_flag
        self.search()
    def update_match_display(self, n_matches):
        # Updates the match count in the top right 'op stats' labelframe
        self.matches_var.set(MATCHES_DISPLAY.format(n_matches))
    def update_wrap_text(self):
        wrap = tk.CHAR if self.wrap_text.get() else tk.NONE
        for page in self.pages:
            page.configure(wrap=wrap)
    def update_editable_text(self):
        state = 'normal' if self.editable_text.get() else 'disabled'
        for page in self.pages:
            page.config(state=state)
    def update_location(self, event):
        page = self.get_selected_page()
        row, column = page.index(tk.INSERT).split('.') # use tk.CURRENT to get the actual mouse cursor pos
        location = LOCATION.format(row, column)
        self.cursor_var.set(location)
    def update_hover_focus(self):
        # TODO go over all the hover code again to make sure its efficient
        self.clear_hover()

    # PAGE FONT
    def update_font(self, font_type='TkFixedFont', family=None, size=None, weight=None):
        font = font_data(font_type)
        if family:
            font[0] = family
        if size:
            font[1] = str(size)
        if weight:
            font[2] = weight

        self._text_font = font
        self.push_font()
    def push_font(self, new_font=None):
        # Push the (family, size, weight) in new_font onto the pages and tags of the gui
        if isinstance(new_font, type(None)):
            new_font = self._text_font
        elif len(new_font) != 3:
            raise IndexError('Parameter <new_font> must be in format (family, size, weight)')

        focus_font = new_font[0], new_font[1], 'bold'
        for page in self.pages:
            page.configure(font=new_font)
            page.tag_config('focus', font=focus_font)
            page.tag_config('hover', font=focus_font)
    def update_font_family(self, offset):
        # Retrieves the [3] font object and changes only the FAMILY, and pushes to screen
        new_family = self.usable_mono_fonts[offset]
        self.font_family.set(new_family)

        self._text_font = [new_family, self._text_font[1], self._text_font[2]]
        self.push_font()
    def update_font_size(self, size):
        # Retrieves the [3] font object and changes only the SIZE, and pushes to screen
        self.font_size.set(str(size))

        self._text_font = [self._text_font[0], size, self._text_font[2]]
        self.push_font()
    def zoom_font(self, event):
        prev_size = self._text_font[1]
        if (event.delta > 0) and (prev_size == FONT_SIZES[-1]):
            return # Font is already maximum -> exit
        if (event.delta < 0) and (prev_size == FONT_SIZES[0]):
            return # Font is already minimum -> exit

        font_index = FONT_SIZES.index(prev_size)
        self._text_font[1] = FONT_SIZES[font_index + (1 if event.delta > 0 else -1)]
        self.font_size.set(str(self._text_font[1]))
        self.push_font()
        #print(dir(event))

    # CLEAR GUI OBJECTS
    def clear_progress(self):
        # Clears the progressbar status by passing 0. Getting ready for another cycle
        self.progress_var.set(0)
    def clear_highlighting(self):
        # Clears highlighting on the group color tags
        page = self.get_selected_page()
        for tag in COLOR_QUEUE + (SINGLE_COLOR,):
            self._remove_tag(page, tag)

        # Clears the foreground highlighting on the treeview selection tag
        self._remove_tag(page, 'match')
        self._remove_tag(page, 'hover')
        self._remove_tag(page, 'focus')
    def clear_tree(self):
        # Clears the tree of all matches to prepare for next round
        self.view.tree.delete(*self.view.tree.get_children())
    def clear_match_display(self):
        # Sets the match display to human friendly '0'
        self.update_match_display(0)
    def clear_status(self):
        # Clears status labels
        self.tree_status.set('')
        self.regex_status.set('')
    def clear_markups(self):
        self.clear_progress()
        self.clear_highlighting()
        self.clear_tree()
    def clear_all(self, *args):
        # Clears all highlighting associated with some search event
        self.clear_highlighting()
        self.clear_tree()
        self.clear_progress()
        self.clear_match_display()
        self.clear_status()
    
    # REALTIME
    def _realtime_scheduler(self):
        # If there is no task waiting to execute, schedule one
        if not self.realtime_locked:
            self._start_realtime()
        else:
            self._reset_realtime()
    def _realtime_search(self):
        # Wrapper for the waiting task to perform a search
        pattern = self.regex_var.get()
        if pattern and pattern != REGEX_PROMPT: # Make sure pattern was not erased in wait
            self.search(self.regex, _realtime=True)
        else:
            self.clear_all()
        self.realtime_locked = False
    def _reset_realtime(self):
        # Cancels a waiting task and reschedules a new one -> essentially resetting timer
        if not self.realtime_locked:
            raise ValueError('Task does not exist, never should have happened')
        self.after_cancel(self.realtime_tieback)
        self.realtime_tieback = self.after(REALTIME_DELAY, self._realtime_search)
    def _start_realtime(self):
        # Schedule a waiting task when there are no currently active tasks
        if self.realtime_locked:
            raise ValueError('Execution already locked, never should have happened')
        self.realtime_locked = True # lock will eventually be released by the scheduled task
        self.realtime_tieback = self.after(REALTIME_DELAY, self._realtime_search)
        self.regex_status.set('Waiting...')
    def _cancel_realtime(self):
        # Cancels a waiting task
        if not self.realtime_locked:
            raise ValueError('Execution already stopped, never should have happened')
        self.after_cancel(self.realtime_tieback)
        self.realtime_locked = False

    # SEARCHING FUNCTIONS  &  REGEX PROCESSING
    def _highlight_item_add(self, match_number, match, decomposing, page):
        ''' Highlight one match on the current page '''

        # Tag the whole match with the insivible 'match' tag
        index = format_index(match[0][1])
        page.tag_add('match', *index)

        if not decomposing:
            # Not decomposing. Use single orange color
            index = format_index(match[0][1])
            page.tag_add(SINGLE_COLOR, *index)
        else:
            # we ARE decomposing, use the color groups
            for sub_match in match:
                # Find the group index of the current match
                color_group = sub_match[0]
                color_index = self.pattern['group-ids'].index(color_group)
                # Cycle-skip if this group is deselected
                if not self.get_group_states()[color_index]: # TODO : Just make a func that returns directly...
                    continue
                # Color group is None when decompose is off. Otherwise, it is an INT
                color = GET_COLOR(color_index)
                # Add the highlighting tag
                index = format_index(sub_match[1])
                page.tag_add(color, *index)
    def _tree_item_add(self, match_number, match, decomposing, page):
        ''' Build one line-item for the treeview, corresponding to one full match '''
        span = match[0][1]
        text = match[0][2]
        #n_chars += len(text)
        #if n_chars > DATA_OVERLOAD:
        #    self.tree_status.set('Data overload: Cannot exceed 100Kb')
        #    break
        line_item = (str(span), text)
        base = self.view.tree.insert('', 'end', text=str(match_number + 1), values=line_item)

        if len(match) > 1:
            for sub_row, sub_match in enumerate(match[1:]):
                identity = str(match_number + 1) + INT2CHAR(sub_row)
                
                sub_len = len(sub_match[2])
                sub_span = str(sub_len) + ' char' + ('s' if sub_len > 1 else '')
                sub_line_item = (sub_span, sub_match[2])
                self.view.tree.insert(base, 'end', text=identity, values=sub_line_item)
    def markup_matches(self, matches):
        # Return the page user is currently viewing
        page = self.get_selected_page()
        decomposing = self.is_decomposed()

        # Housekeeping
        self.clear_markups()
        self.regex_status.set('Processing')
        self.setup_progress(matches['num'])

        n_chars = 0
        for match_number, match in enumerate(matches['match']):

            session = [match_number, match, decomposing, page]

            ################  HIGHLIGHT  ################
            if match_number < HIGHLIGHT_OVERLOAD:
                self._highlight_item_add(*session)
            elif match_number == HIGHLIGHT_OVERLOAD:
                self.regex_status.set('OVERLOAD')

            ################  TREE VIEW  ################
            if match_number < TREE_OVERLOAD:
                self._tree_item_add(*session)
            elif match_number == TREE_OVERLOAD:
                self.tree_status.set('Limiting to first 99')

            self.update_progress() # Only increment progress bar
            self.periodic_update() # Only update GUI (if in proper cycle)

        # If matches were found without error, clear status to denote success
        self.regex_status.set('')

        self.update()
    def search(self, *args, _realtime=False):
        ''' Call this function to initiate a search event '''

        if self.is_executing:
            return # Already doing something
        elif not self.pages:
            return # No pages
        elif not self.regex_var.get() or self.regex_var.get() == REGEX_PROMPT:
            self.clear_highlighting()
            return # No Regex
        elif not self.is_good:
            self.regex_entry['bg'] = 'pink'
            self.after(MINILOOP_PERIOD, self._reset_entry_bg)
            return # Invalid regex

        if not _realtime and self.realtime_locked:
            self._cancel_realtime()
        
        # Lock tasks when unique entry/exit points (for function) are reduced
        self.is_executing = True

        # Main match finding algorithm
        matches = find_matches(self.regex, self.get_text(), self.flag_obj,
                                    overload=FATAL_OVERLOAD)
        self.matches = matches # Push to instance-wide matches list

        # Notify user of number of matches immediately after finding them
        self.update_match_display(matches['num'])

        # If the total # of matches exceeds the limit, indicate so and EXIT function
        if matches['num'] > FATAL_OVERLOAD:
            self.regex_status.set('OVERLOAD')
            self.tree_status.set('Fatal Overload: Aborting')
            self.is_executing = False
            return  #  Premature termination - user obviously searched in error

        # Undo the 'realtime' radiobutton if regex results overflow
        if AUTO_DISABLE_REALTIME and (self.n_matches > REALTIME_OVERLOAD):
            self.disable_realtime()

        # Main function call to markup matches in page view and tree view
        self.markup_matches(matches)

        # Zoom the selected page to the first match (if there were any)
        if matches['num']:
            self.text_focus(match_no=1, tag=False)
        else:
            self.regex_status.set('No Matches')

        self.clear_progress()

        self.is_executing = False # Release the task lock



class App(tk.Tk):
    def __init__(self, *args, geometry=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('RegEx IDE')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        if geometry:
            self.geometry(geometry)

        self.env = IDE(self, auto_sash=False) # Finalize is a hackey way to do the sashpos thing
        self.env.grid(sticky=N+S+E+W)#, padx=4, pady=4)
        self.env._push_sash_right()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def destroy(self):
        try:
            # Stop miniloop, and realtime waiting func
            self.env.stop_events()

            # If searching is still happening, wait for it to complete by recurrsively calling self
            if self.env.is_executing:
                self.after(MINILOOP_PERIOD, self.destroy)
                return
        except AttributeError:
            # During development, if there was an error while building the gui, then window
            # will be unable to be closed because the 'env' is still undefined. this catches that.
            pass

        # Call the overriden parent's destroy function
        tk.Tk.destroy(self)

