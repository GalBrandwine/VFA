import csv
import logging
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from run import Run


class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


class VFA_gui:
    """ Simple gui for operating on VFA. """

    def __init__(self, title, win_width, win_height):
        self.master = None
        self.init(title, win_width, win_height)

        # Menu
        self.create_menu(self.master)

        # Buttons
        self.create_buttons(self.master)

        # VFA1
        self.vfa = None
        # VFA2
        self.secondary_vfa = None
        
        # Word
        self.word = None

    # Gui button's should activate inner class instance functions!
    def raise_expection(self, exception):
        """ Raise exception in a separate gui. """
        messagebox.showerror('Exception', exception)

    def message_window(self, message):
        """ Simple window message. """
        filewin = Toplevel(self.master)
        filewin.geometry("350x50")
        label = Label(filewin, text=message)
        label.pack()
        button = Button(filewin, text="Ok", command=filewin.destroy)
        button.pack()

    def new_vfa_window(self):
        """ Window for generate random VFA. """
        filewin = Toplevel(self.master)
        filewin.title("VFA generator.")
        filewin.geometry("450x270")

        label = Label(filewin, text="Num of const: ")
        label.grid(row=1, column=1, pady=5, padx=5)
        num_of_const = Entry(filewin, bd=5)
        num_of_const.grid(row=1, column=2, pady=5, padx=5)

        label = Label(filewin, text="Num of states: ")
        label.grid(row=2, column=1, pady=5, padx=5)
        num_of_states = Entry(filewin, bd=5)
        num_of_states.grid(row=2, column=2, pady=5, padx=5)

        label = Label(filewin, text="Width: ")
        label.grid(row=3, column=1, pady=5, padx=5)
        width = Entry(filewin, bd=5)
        width.grid(row=3, column=2, pady=5, padx=5)

        check_var1 = BooleanVar()
        check_var2 = BooleanVar()
        C1 = Checkbutton(filewin, text="Unreachable states", variable=check_var1, onvalue=1, offvalue=0, height=5,
                         width=20)
        C2 = Checkbutton(filewin, text="Unwinded", variable=check_var2, onvalue=1, offvalue=0, height=5, width=20)
        C1.grid(row=4, column=1, pady=5, padx=5)
        C2.grid(row=4, column=2, pady=5, padx=5)

        button = Button(filewin, text="Ok",
                        command=lambda: self.generate_automata(filewin, num_of_const.get(), num_of_states.get(),
                                                               width.get(), check_var1.get(), check_var2.get()))
        button.grid(row=5, column=2, columnspan=3, pady=5, padx=5, sticky="ew")

    def generate_automata(self, filewin, num_of_const, num_of_states, width, unreachable_states, unwinded):
        """Function for generating VFA. """
        filewin.destroy()

        print("VFA generated with the folowing parameters:\n"
              "num_of_const: \t\t{}\n"
              "num_of_states: \t\t{}\n"
              "width: \t\t\t\t{}\n"
              "unreachable_states: {}\n"
              "unwinded: \t\t\t{}\n".format(num_of_const, num_of_states, width, unreachable_states, unwinded))

    def run(self):
        """
        Function for calling RUN's run operation
        todo: implement Run module and its methods.
        :return:
        """
        filewin = Toplevel(self.master)
        filewin.title("Run on Word")
        filewin.geometry("665x450")

        # Add text widget to display logging info
        st = ScrolledText(filewin, state='disabled')
        st.configure(font='TkFixedFont')
        st.grid(column=0, row=1, sticky='w', columnspan=4)

        # Create textLogger
        text_handler = TextHandler(st)

        # Logging configuration
        # Add the handler to logger
        logger = logging.getLogger('Run')
        logger.setLevel(logging.INFO)
        # Create file handler which logs even debug messages
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        text_handler.setFormatter(formatter)

        # Add the handler to logger
        logger.addHandler(text_handler)
        run = Run(logger, self.vfa, self.word)
        logger.info("Executing a Run of initiated automata on a given word")
        print("Executing a Run of initiated automata on a given word")

    def emptiness(self):
        """
        Function for calling VFA's unwind operation
        todo: call self.VFA.unwind. add the returned VFA into the VFA container.
        :return: unwinded new VFA
        """
        print("emptiness have been performed")

    def union(self):
        """
        Function for calling VFA's union operation
        todo: call self.VFA.union.
        :return:
        """
        self.master.filename = filedialog.askopenfilename(initialdir="/", title="Select VFA to union with.",
                                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

        # Sanity check
        try:
            with open('{}'.format(self.master.filename), 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for i, row in enumerate(spamreader):
                    if i == 0:
                        """column names. """
                        pass
                    else:
                        print(', '.join(row))
            print("VFA loaded: \n")
        except FileNotFoundError as err:
            pass
        except Exception as err:
            self.raise_expection(err)

    def complete(self):
        """
        Function for calling VFA's complete operation
        todo: call self.VFA.complete.
        :return:
        """
        print("complete have been performed")

    def intersect(self):
        """
        Function for activating VFA's intersect operation
        todo: call VFA.generate(root.filename), add the result into a second VFA containar
        :return:
        """
        self.master.filename = filedialog.askopenfilename(initialdir="/", title="Select VFA to intersect with.",
                                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

        # Sanity check
        try:
            with open('{}'.format(self.master.filename), 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for i, row in enumerate(spamreader):
                    if i == 0:
                        """column names. """
                        pass
                    else:
                        print(', '.join(row))
            print("VFA loaded: \n")
        except FileNotFoundError as err:
            pass
        except Exception as err:
            self.raise_expection(err)

    def get_inserted_word(self, word):
        """
        Function for creating a Word instance from given word.
        :return:
        """
        print(word)
        # todo: get inserted word, initiate a  Word instance and add it to the RUN instance, than RUN!

    def open_vfa(self):
        """Function for getting csv path. """
        self.master.filename = filedialog.askopenfilename(initialdir="/", title="Select VFA",
                                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        # Sanity check
        try:
            with open('{}'.format(self.master.filename), 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for i, row in enumerate(spamreader):
                    if i == 0:
                        """column names. """
                        pass
                    else:
                        print(', '.join(row))
                    # todo: call VFA.generate(root.filename)
            print("VFA loaded: \n")
        except FileNotFoundError as err:
            pass
        except Exception as err:
            self.raise_expection(err)

    def load_word(self):
        """Function for getting word_file path. """
        self.master.filename = filedialog.askopenfilename(initialdir="/", title="Select file for word reading",
                                                          filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        # Sanity check
        try:
            with open('{}'.format(self.master.filename), 'r') as txtfile:
                print('{} '.format(txtfile.read()))
                # todo: call Word(txtfile.read())
            print("Word loaded! \n")

        except FileNotFoundError as err:
            pass
        except Exception as err:
            self.raise_expection(err)

    def create_menu(self, master):
        """Menu for ur GUI.

        capabilities:
            * Load VFA from csv.
            * Save generated VFA to csv.
            * exit.

        """
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_vfa_window)
        filemenu.add_command(label="Open", command=self.open_vfa)
        filemenu.add_command(label="Save",
                             command=lambda: self.message_window("Save"))  # todo: replace with real save to csv!
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)

    def create_buttons(self, master):
        """

        :param master:
        :return:
        """
        self.create_right_buttons(master)
        self.create_center_widgets(master)

    def create_right_buttons(self, master):
        """

        :param master:
        :return:
        """

        # Create right_side elements
        right_frame = Frame(master)
        right_frame.pack(side=RIGHT)

        right = Frame(right_frame, width=300, height=100, pady=0, padx=100)
        right.grid(row=0, sticky="ew")

        run_button = Button(right, text="Run", command=self.run)
        run_button.grid(row=1, column=0, pady=5, sticky="ew")
        # Separator
        ttk.Separator(right, orient=HORIZONTAL).grid(row=2, column=0, pady=30, sticky="ew")

        button = Button(right, text="emptiness", command=self.emptiness)
        button.grid(row=3, column=0, pady=5, sticky="ew")

        button = Button(right, text="complete", command=self.complete)
        button.grid(row=4, column=0, pady=5, sticky="ew")

        button = Button(right, text="union", command=self.union)
        button.grid(row=5, column=0, pady=5, sticky="ew")

        button = Button(right, text="intersect", command=self.intersect)
        button.grid(row=6, column=0, pady=5, sticky="ew")

        close_button = Button(right, text="Close", command=master.quit)
        close_button.grid(row=7, columnspan=3)

    def create_center_widgets(self, master):
        """

        :param master:
        :return:
        """
        # Create center elements
        center_frame = Frame(master)
        center_frame.pack()

        center_grid = Frame(center_frame, width=300, height=300, pady=150, padx=50)
        center_grid.grid(row=0, sticky="ew")

        word_button = Label(center_grid, text="Enter word:")
        word_button.grid(row=1, column=0, pady=5)

        entered_word = Entry(center_grid, bd=5)
        entered_word.grid(row=1, column=2, pady=5, padx=5)

        button = Button(center_grid, text="Ok", command=lambda: self.get_inserted_word(entered_word.get()))
        button.grid(row=1, column=3, pady=5, padx=5)

        load = Button(center_grid, text="Load word from file", command=self.load_word)
        load.grid(row=2, columnspan=4, pady=10, sticky="ew")

        # Separator
        ttk.Separator(center_grid, orient=HORIZONTAL).grid(row=3, columnspan=10, pady=30, sticky="ew")

        # Table creation
        from_label = Label(center_grid, text="From")
        from_label.grid(row=4, column=0, pady=5)
        # VERT Separator
        ttk.Separator(center_grid, orient=VERTICAL).grid(row=4, column=1, rowspan=30, pady=0, padx=5, sticky="ns")
        from_label = Label(center_grid, text="Condition")
        from_label.grid(row=4, column=2, pady=5)

        # VERT Separator
        ttk.Separator(center_grid, orient=VERTICAL).grid(row=4, column=3, rowspan=30, pady=0, padx=5, sticky="ns")
        from_label = Label(center_grid, text="To")
        from_label.grid(row=4, column=4, pady=5)

        starting_row = 5
        self.fill_table(center_grid, starting_row)

    def fill_table(self, center_grid, starting_row):
        """
        Simple example for filling the table
        todo: should be able to fill from loaded VFA
        :param center_grid:
        :param starting_row:
        :return:
        """
        for r in range(3):
            for c in range(0, 5, 2):
                # col 0, is FROM
                if c == 0:
                    Label(center_grid, text='q{}'.format(c),
                          borderwidth=1).grid(row=starting_row + r, column=c)
                # col 2, is CONDITION
                if c == 2:
                    Label(center_grid, text='x{}'.format(r),
                          borderwidth=1).grid(row=starting_row + r, column=c)
                # col 4, is TO
                if c == 4:
                    Label(center_grid, text='q{}'.format(c),
                          borderwidth=1).grid(row=starting_row + r, column=c)

    def init(self, title, win_width, win_height):
        root = Tk()
        root.geometry("{}x{}".format(win_width, win_height))
        self.master = root
        self.master.title(title)

    def start(self):
        self.master.mainloop()


if __name__ == "__main__":
    """ Lazy testing. """

    my_gui = VFA_gui("Automata generation & verification tool", 1000, 500)
    my_gui.start()
