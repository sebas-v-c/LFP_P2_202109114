from tkinter import *
from tkinter import ttk

import InitialWindow
import LoadFiles.load_files

from Automaton.AutomatonOptions import InfoController
from Automaton.AutomatonOptions import ValidateController
from Automaton.AutomatonOptions import RouteController
from Automaton.AutomatonOptions import PassController


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None
        parent.title("Módulo Autómatas")

        # -----------------------------------Information-------------------------------#
        title_label = ttk.Label(self, text="Módulo Autómatas", font=("Arial Bold", 30))
        title_label.grid(row=0, column=0, columnspan=3)

        # -----------------------------------Load file-------------------------------#
        load_file_button = ttk.Button(
            self,
            text="Cargar Archivo",
            command=self.load_file_button_pressed,
        ).grid(column=0, row=2, sticky="WE")

        # -----------------------------------General Information-------------------------------#
        general_info_button = ttk.Button(
            self,
            text="Información General",
            command=self.general_info_button_pressed,
        ).grid(column=0, row=3, sticky="WE")

        # -----------------------------------Validate string-------------------------------#
        validate_string_button = ttk.Button(
            self,
            text="Validar Cadena",
            command=self.validate_string_button_pressed,
        ).grid(column=0, row=4, sticky="WE")

        # -----------------------------------Validation Route-------------------------------#
        validation_route_button = ttk.Button(
            self,
            text="Ruta De validación",
            command=self.validation_route_button_pressed,
        ).grid(column=2, row=2, sticky="WE")

        # -----------------------------------Step by step-------------------------------#
        step_by_step_button = ttk.Button(
            self,
            text="Información General",
            command=self.step_by_step_button_pressed,
        ).grid(column=2, row=3, sticky="WE")

        # -----------------------------------One pass-------------------------------#
        onepass_button = ttk.Button(
            self,
            text="Validar A Una Pasa",
            command=self.one_pass_button_pressed,
        ).grid(column=2, row=4, sticky="WE")

        # -----------------------------------Return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=1, row=5, sticky="WE")

        self.add_padding()

    def load_file_button_pressed(self):
        if self.controller:
            self.controller.load_file_button()

    def general_info_button_pressed(self):
        if self.controller:
            self.controller.general_info_button()

    def validate_string_button_pressed(self):
        if self.controller:
            self.controller.validate_string_button()

    def validation_route_button_pressed(self):
        if self.controller:
            self.controller.validation_route_button()

    def step_by_step_button_pressed(self):
        if self.controller:
            self.controller.step_by_step_button()

    def one_pass_button_pressed(self):
        if self.controller:
            self.controller.one_pass_button()

    def set_controller(self, controller):
        self.controller = controller

    def return_button_pressed(self):
        if self.controller:
            self.controller.return_button()

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
        controller = LoadFiles.load_files.Controller(self._app, automaton=True)

    def general_info_button(self):
        controller = InfoController(self._app)

    def validate_string_button(self):
        controller = ValidateController(self._app)

    def validation_route_button(self):
        controller = RouteController(self._app)
        pass

    def step_by_step_button(self):
        pass

    def one_pass_button(self):
        controller = PassController(self._app)
