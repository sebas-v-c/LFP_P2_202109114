from tkinter import *
from tkinter import ttk

import InitialWindow


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None
        parent.title("Módulo Gramáticas")

        # -----------------------------------Information-------------------------------#
        title_label = ttk.Label(self, text="Módulo Gramáticas", font=("Arial Bold", 30))
        title_label.grid(row=1, column=2)

        # -----------------------------------Load file-------------------------------#
        load_file_button = ttk.Button(
            self,
            text="Cargar Archivo",
            command=self.load_file_button_pressed,
        ).grid(column=2, row=2, sticky="WE")

        # -----------------------------------General Information-------------------------------#
        general_info_button = ttk.Button(
            self,
            text="Información General",
            command=self.general_info_button_pressed,
        ).grid(column=2, row=3, sticky="WE")

        # -----------------------------------Tree of derivation-------------------------------#
        derivation_tree_button = ttk.Button(
            self,
            text="Árbol De Derivación",
            command=self.derivation_tree_button_pressed,
        ).grid(column=2, row=4, sticky="WE")

        # -----------------------------------Return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=2, row=4, sticky="WE")

        self.add_padding()

    def return_button_pressed(self):
        if self.controller:
            self.controller.return_button()

    def load_file_button_pressed(self):
        if self.controller:
            self.controller.load_file_button()

    def general_info_button_pressed(self):
        if self.controller:
            self.controller.general_info_button()

    def derivation_tree_button_pressed(self):
        if self.controller:
            self.controller.derivation_tree_button()

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

    def return_button(self):
        controller = InitialWindow.MenuController(self._app)

    def load_file_button(self):
        pass

    def general_info_button(self):
        pass

    def derivation_tree_button(self):
        pass
