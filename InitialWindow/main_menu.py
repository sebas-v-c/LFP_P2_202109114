from tkinter import *
from tkinter import ttk

import Gramatics
import Automaton

import InitialWindow


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None
        parent.title("Pantalla Principal")

        # -----------------------------------Information-------------------------------#
        title_label = ttk.Label(self, text="SPARK STACK", font=("Arial Bold", 30))
        title_label.grid(row=1, column=2)

        # -----------------------------------Free of Context gramatic module-------------------------------#
        free_context_gramatic_button = ttk.Button(
            self,
            text="Gramática Libre De Contexto",
            command=self.free_context_gramatic_button_pressed,
        ).grid(column=2, row=2, sticky="WE")

        # -----------------------------------Stack automatons module-------------------------------#
        stack_automaton_button = ttk.Button(
            self,
            text="Autómata De Pila",
            command=self.stack_automaton_button_pressed,
        ).grid(column=2, row=3, sticky="WE")

        # -----------------------------------Exit button-------------------------------#
        exit_button = ttk.Button(
            self,
            text="Salir",
            command=self.exit_button_pressed,
        ).grid(column=2, row=4, sticky="WE")

        self.add_padding()

    def exit_button_pressed(self):
        if self.controller:
            self.controller.exit_button()

    def free_context_gramatic_button_pressed(self):
        if self.controller:
            self.controller.free_context_gramatic_button()

    def stack_automaton_button_pressed(self):
        if self.controller:
            self.controller.stack_automaton_button()

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

    def exit_button(self):
        controller = InitialWindow.InitController(self._app, exit=True)

    def free_context_gramatic_button(self):
        controller = Gramatics.GramaticsController(self._app)

    def stack_automaton_button(self):
        controller = Automaton.AutomatonController(self._app)
