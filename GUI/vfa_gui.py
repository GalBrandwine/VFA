import csv
from tkinter import *
from tkinter import filedialog


class VFA_gui:
    """Simple gui for operating on VFA. """

    def __init__(self, master):
        self.master = master
        master.title("Automaton generation & verification tool")

        # Menu
        self.create_menu(master)

        # Buttons
        self.run_button = None
        self.close_button = None
        self.greet_button = None

        self.create_buttons(master)

        # Labels
        self.label = None
        self.create_labels(master)

    # Gui buttonts should activate inner class instance functions!
    def donothing(self):
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def greet(self):
        print("Greetings!")

    def run(self):
        print("Executing a Run of initiated Automaton on a given word")

    def open_vfa(self):
        """function for Getting csv path. """
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        # Sanity check
        with open('{}'.format(root.filename), 'r') as csvfile:
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
        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack(side=LEFT)

        self.run_button = Button(master, text="Run", command=self.run)
        self.run_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def create_labels(self, master):
        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()


if __name__ == "__main__":
    root = Tk()
    root.geometry("1200x600")
    my_gui = VFA_gui(root)
    root.mainloop()
