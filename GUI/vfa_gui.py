import csv
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


class VFA_gui:
    """Simple gui for operating on VFA. """

    def __init__(self, master):
        self.master = master
        self.master.title("Automaton generation & verification tool")

        # Menu
        self.create_menu(master)

        # Buttons
        self.create_buttons(master)

    # Gui button's should activate inner class instance functions!
    def donothing(self):
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def greet(self):
        print("Greetings!")

    def run(self):
        print("Executing a Run of initiated Automaton on a given word")

    def unwind(self):
        print("Unwinded have been performed")

    def negate(self):
        print("Negate have been performed")

    def complete(self):
        print("complete have been performed")

    def intersect(self):
        self.master.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

        # Sanity check
        print("VFA loaded: \n")
        with open('{}'.format(self.master.filename), 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for i, row in enumerate(spamreader):
                if i == 0:
                    """column names. """
                    pass
                else:
                    print(', '.join(row))
        # todo: call VFA.generate(root.filename), add the result into a second VFA containar

    def get_inserted_word(self):
        print(self.entered_word.get())
        # todo: get inserted word, initiate a  Word instance and add it to the RUN instance, than RUN!

    def generate_automaton(self):
        """
        Function for calling the VFA.generate method.
        :return: add to the VFA container
        """
        # todo: implement VFA.generate in VFA.

    def open_vfa(self):
        """function for Getting csv path. """
        self.master.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        # Sanity check
        with open('{}'.format(self.master.filename), 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for i, row in enumerate(spamreader):
                if i == 0:
                    """column names. """
                    pass
                else:
                    print(', '.join(row))
        # todo: call VFA.generate(root.filename)

    def create_menu(self, master):
        """Menu for ur GUI.

        capabilities:
            * Load VFA from csv.
            * Save generated VFA to csv.
            * exit.

        """
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.open_vfa)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_command(label="Save as...", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)
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
        run_button.grid(row=1, column=0)
        # Separator
        ttk.Separator(right, orient=HORIZONTAL).grid(row=2, column=0, pady=30, sticky="ew")

        run_button = Button(right, text="Unwind", command=self.unwind)
        run_button.grid(row=3, column=0, pady=5, sticky="ew")

        run_button = Button(right, text="negate", command=self.negate)
        run_button.grid(row=4, column=0, pady=5, sticky="ew")

        run_button = Button(right, text="complete", command=self.complete)
        run_button.grid(row=5, column=0, pady=5, sticky="ew")

        run_button = Button(right, text="intersect", command=self.intersect)
        run_button.grid(row=6, column=0, pady=5, sticky="ew")

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

        greet_button = Label(center_grid, text="Enter word:")
        greet_button.grid(row=1, column=0, pady=5)

        self.entered_word = Entry(center_grid, bd=5)
        self.entered_word.grid(row=1, column=2, pady=5, padx=5)

        button = Button(center_grid, text="Ok", command=self.get_inserted_word)
        button.grid(row=1, column=3, pady=5, padx=5)

        generate_automaton = Button(center_grid, text="Generate Automaton", command=self.generate_automaton)
        generate_automaton.grid(row=2, columnspan=4, pady=10, sticky="ew")
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


if __name__ == "__main__":
    root = Tk()
    root.geometry("1200x600")
    my_gui = VFA_gui(root)
    root.mainloop()
