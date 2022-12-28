from tkinter import *
from tkinter import ttk

import Gramatics


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None
        parent.title("Información General")

        # -----------------------------------Information-------------------------------#
        title_label = ttk.Label(
            self, text="Información General", font=("Arial Bold", 20)
        )
        title_label.grid(row=1, column=0, columnspan=2)

        # -----------------------------------Gramatic Combobox-------------------------------#
        self.gramatic_combobox = StringVar()
        self._gramatic_combobox = ttk.Combobox(
            self, textvariable=self.gramatic_combobox
        )
        self._gramatic_combobox.state(["readonly"])
        self._gramatic_combobox.grid(row=2, column=0, columnspan=2, sticky="WE")
        self._gramatic_combobox.bind("<<ComboboxSelected>>", self.combobox_selected)

        # -----------------------------------Name-------------------------------#
        gramatic_name_label = ttk.Label(self, text="Nombre: ")
        gramatic_name_label.grid(row=3, column=0, sticky="e")

        self.gramatic_name = StringVar()
        gramatic_name_entry = ttk.Entry(self, textvariable=self.gramatic_name, width=20)
        gramatic_name_entry.grid(row=3, column=1)
        gramatic_name_entry.state(["disabled"])

        # -----------------------------------No terminals-------------------------------#
        no_terminals_label = ttk.Label(self, text="No Terminales: ")
        no_terminals_label.grid(row=4, column=0, sticky="e")

        self.no_terminals = StringVar()
        no_terminals_entry = ttk.Entry(self, textvariable=self.no_terminals, width=20)
        no_terminals_entry.grid(row=4, column=1)
        no_terminals_entry.state(["disabled"])

        # -----------------------------------Terminals-------------------------------#
        terminals_label = ttk.Label(self, text="Terminales: ")
        terminals_label.grid(row=5, column=0, sticky="e")

        self.terminals = StringVar()
        terminals_entry = ttk.Entry(self, textvariable=self.terminals, width=20)
        terminals_entry.grid(row=5, column=1)
        terminals_entry.state(["disabled"])

        # -----------------------------------Initial No terminals-------------------------------#
        initial_no_terminals_label = ttk.Label(self, text="No Terminales Inicial: ")
        initial_no_terminals_label.grid(row=6, column=0, sticky="e")

        self.initial_no_terminals = StringVar()
        initial_no_terminals_entry = ttk.Entry(
            self, textvariable=self.initial_no_terminals, width=20
        )
        initial_no_terminals_entry.grid(row=6, column=1)
        initial_no_terminals_entry.state(["disabled"])

        # -----------------------------------Productions-------------------------------#
        productions_label = ttk.Label(self, text="Productions: ")
        productions_label.grid(row=7, column=0, sticky="e")

        self.productions_textarea = Text(self, width=20, height=10)
        # self.productions_textarea.insert("1.0", "Ejemplo:\n\nA,1;B\nA,2;B\nB,1;C\n...")
        self.productions_textarea.grid(row=8, column=0, columnspan=2)
        self.productions_textarea.config(state=DISABLED)

        # -----------------------------------Return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=0, row=9, columnspan=2)

        self.add_padding()

    def combobox_selected(self, *args):
        self._gramatic_combobox.selection_clear()
        if self.controller:
            self.controller.combobox_selected()

    def define_combobox_values(self, values: list):
        self._gramatic_combobox["values"] = values

    def return_button_pressed(self):
        if self.controller:
            self.controller.return_button()

    def set_controller(self, controller):
        self.controller = controller

    def add_padding(self, x_size=7, y_size=7):
        for child in self.winfo_children():
            child.grid_configure(padx=x_size, pady=y_size)


class Controller:
    def __init__(self, app) -> None:
        # boiler plate code
        self._app = app
        self._view = View(app)
        app.switch_frame(self._view)

        self._view.set_controller(self)

        # get a list of names
        self._view.define_combobox_values(
            list(map(lambda gramatic: gramatic.name, app.gramatics_objects))
        )

    def return_button(self):
        controller = Gramatics.GramaticsController(self._app)

    def combobox_selected(self):
        # get gramatic by name
        name = self._view.gramatic_combobox.get()
        gramatic: Gramatics.Gramatic = list(
            filter(lambda item: item.name == name, self._app.gramatics_objects)
        )[0]

        # change name entry
        self._view.gramatic_name.set(gramatic.name)
        # change no terminals entry
        self._view.no_terminals.set(", ".join(gramatic.no_terminals))
        # change terminals entry
        self._view.terminals.set(", ".join(gramatic.terminals))
        # change initial no terminal
        self._view.initial_no_terminals.set(gramatic.initial_no_terminal)

        # change productions value
        # First convert productions into a dictionary {index: value}
        productions_dict: dict = {
            index: item for item, index in enumerate(gramatic.productions)
        }

        string = []
        for production, index in productions_dict.items():

            pass
