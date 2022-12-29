from tkinter import *
from tkinter import ttk

import threading
import os
import Automaton
import Automaton.Graphviz as Graphviz
from Automaton.stack_automaton import StackAutomaton

DOT_FILE_NAME = ".input.out"
PDF_FILE_NAME = "output.pdf"


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None

        parent.title("Crear Reporte")

        # -----------------------------------Title-------------------------------#
        title_label = ttk.Label(
            self, text="Información Del Autómata", font=("Arial Bold", 15)
        )
        title_label.grid(row=1, column=2)

        # -----------------------------------StackAutomaton Combobox-------------------------------#
        self.stack_automaton_combobox = StringVar()
        self._stack_automaton_combobox = ttk.Combobox(
            self, textvariable=self.stack_automaton_combobox
        )
        self._stack_automaton_combobox.state(["readonly"])
        self._stack_automaton_combobox.grid(row=2, column=2, sticky="WE")
        self._stack_automaton_combobox.bind(
            "<<ComboboxSelected>>", self.combobox_selected
        )

        # -----------------------------------create report button-------------------------------#
        self.create_button = ttk.Button(
            self, text="Generar Reporte", command=self.generate_report_button_pressed
        )
        self.create_button.state(["disabled"])
        self.create_button.grid(row=3, column=2, sticky="WE")

        # -----------------------------------validate label-------------------------------#
        self.generate_report = StringVar()
        self.generate_report.trace_add("write", self.on_write_changed)
        self.generate_report_label = ttk.Label(
            self,
            text="",
            foreground="red",
            font=("Arial Bold", 10),
            textvariable=self.generate_report,
        )
        self.generate_report_label.grid(row=7, column=2)

        # -----------------------------------return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=2, row=5)

        self.add_padding()

    def generate_report_button_pressed(self):
        if self.controller:
            self.controller.generate_report()

    def combobox_selected(self, *args):
        self._stack_automaton_combobox.selection_clear()
        if self.controller:
            self.controller.combobox_selected()

    def on_write_changed(self, *args):
        if self.controller:
            self.controller.on_entry_changed()

    def define_combobox_values(self, values: list):
        self._stack_automaton_combobox["values"] = values

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
        self._app = app
        self._view = View(app)
        app.switch_frame(self._view)

        self._view.set_controller(self)

        # get a list of names
        self._view.define_combobox_values(
            list(
                map(
                    lambda stack_automaton: stack_automaton.name,
                    app.automaton_objects,
                )
            )
        )

    def generate_report(self):
        stack_automaton_name = self._view.stack_automaton_combobox.get()
        stack_automaton_object: StackAutomaton
        for stack_automaton in self._app.automaton_objects:
            if stack_automaton.name == stack_automaton_name:
                stack_automaton_object = stack_automaton
                break

        if not stack_automaton_object:
            return

        # generate diagraph and description
        try:
            diagraph: str = "digraph G {\n" + Graphviz.create_diagraph(
                stack_automaton_object
            )
            description: str = (
                "\n" + Graphviz.create_description(stack_automaton_object) + "\n}"
            )
        except:
            self._view.generate_report.set(
                "Ha ocurrido un error al generar el archivo .dot"
            )
            return

        cwd = os.getcwd()

        try:
            os.remove(cwd + "/" + DOT_FILE_NAME)
        except:
            pass

        with open(DOT_FILE_NAME, mode="w") as f:
            f.write(diagraph + description)

        try:
            os.system("dot -Tpdf " + DOT_FILE_NAME + " > " + PDF_FILE_NAME)
        except:
            self._view.generate_report.set(
                "Ha ocurrido un error al generar el archivo pdf"
            )

        try:
            thread = threading.Thread(target=self.open_document, args=[cwd])
            thread.start()
        except:
            self._view.generate_report.set(
                "Ha ocurrido un error al abrir el archivo pdf"
            )

    def open_document(self, cwd):
        os.system("zathura " + cwd + "/" + PDF_FILE_NAME)

    def combobox_selected(self):
        self._view.create_button.state(["!disabled"])

    def on_entry_changed(self):
        self._view.generate_report.set("")

    def return_button(self):
        controller = Automaton.AutomatonController(self._app)
