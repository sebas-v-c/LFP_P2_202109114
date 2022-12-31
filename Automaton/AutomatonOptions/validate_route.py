from tkinter import *
from tkinter import ttk


import Automaton

DOT_FILE_NAME = ".input_route.out"
PDF_FILE_NAME = "output_route.pdf"


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None

        parent.title("Ruta De Validación")

        # -----------------------------------Title-------------------------------#
        title_label = ttk.Label(
            self, text="Ruta De Validación", font=("Arial Bold", 15)
        )
        title_label.grid(row=1, column=2)

        # -----------------------------------STACK_AUTOMATON Label-------------------------------#
        stack_automaton_label = ttk.Label(self, text="Autómata De Pila: ")
        stack_automaton_label.grid(row=2, column=1, sticky="E")

        # -----------------------------------STACK_AUTOMATON Combobox-------------------------------#
        self.stack_automaton_combobox = StringVar()
        self._stack_automaton_combobox = ttk.Combobox(
            self, textvariable=self.stack_automaton_combobox
        )
        self._stack_automaton_combobox.state(["readonly"])
        self._stack_automaton_combobox.grid(row=2, column=2, sticky="WE")
        self._stack_automaton_combobox.bind(
            "<<ComboboxSelected>>", self.combobox_selected
        )

        # -----------------------------------String-------------------------------#
        self.stack_automaton_string = StringVar()
        self.stack_automaton_string_entry = ttk.Entry(
            self, textvariable=self.stack_automaton_string, width=30
        )
        self.stack_automaton_string_entry.grid(row=3, column=2)
        self.stack_automaton_string_entry.state(["disabled"])

        # -----------------------------------validate button-------------------------------#
        self.validation_route_button = ttk.Button(
            self, text="Solo Validar", command=self.validation_route_button_pressed
        )
        self.validation_route_button.grid(row=3, column=3)
        self.validation_route_button.state(["disabled"])

        # -----------------------------------Validations route-------------------------------#
        validation_route_label = ttk.Label(self, text="Ruta: ")
        validation_route_label.grid(row=4, column=0, sticky="e")

        self.validation_route_textarea = Text(self, width=30, height=12)
        self.validation_route_textarea.grid(row=5, column=0, columnspan=3, sticky="we")
        # self.productions_textarea.config(state=DISABLED)

        # -----------------------------------validate label-------------------------------#
        self.validate_stack_automaton = StringVar()
        self.validate_stack_automaton.trace_add("write", self.on_write_changed)
        self.validate_stack_automaton_label = ttk.Label(
            self,
            text="",
            foreground="red",
            font=("Arial Bold", 15),
            textvariable=self.validate_stack_automaton,
        )
        self.validate_stack_automaton_label.grid(row=8, column=1, columnspan=3)

        # -----------------------------------return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=3, row=7)

        self.add_padding()

    def define_combobox_values(self, values: list):
        self._stack_automaton_combobox["values"] = values

    def on_write_changed(self, *args):
        if self.controller:
            self.controller.on_entry_changed()

    def combobox_selected(self, *args):
        self._stack_automaton_combobox.selection_clear()
        if self.controller:
            self.controller.combobox_selected()

    def validation_route_button_pressed(self):
        if self.controller:
            self.controller.validation_route()

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

    def validation_route(self):
        stack_automaton_name = self._view.stack_automaton_combobox.get()
        automaton_object: Automaton.StackAutomaton
        for stack_automaton in self._app.automaton_objects:
            if stack_automaton.name == stack_automaton_name:
                automaton_object = stack_automaton
                break

        if not automaton_object:
            return

        string = self._view.stack_automaton_string.get()
        self._view.validation_route_textarea.delete("1.0", END)

        try:
            steps: list[Automaton.Transition] = automaton_object.evaluate_string(string)
        except:
            self._view.validation_route_textarea.insert("1.0", "")
            self._view.validate_stack_automaton_label.config(foreground="red")
            self._view.validate_stack_automaton.set(
                "La Cadena Introducida No Es Válida"
            )
        else:
            formated_lines = []
            for step in steps:
                formated_lines.append(str(step))
            self._view.validation_route_textarea.delete("1.0", END)
            self._view.validation_route_textarea.update()
            self._view.validation_route_textarea.insert(
                "1.0", "\n".join(formated_lines)
            )
            self._view.validate_stack_automaton_label.config(foreground="green")
            self._view.validate_stack_automaton.set(
                "La Cadena Introducida Sí Es Válida"
            )

    def combobox_selected(self):
        self._view.validate_stack_automaton.set("")
        self._view.stack_automaton_string_entry.state(["!disabled"])
        self._view.validation_route_button.state(["!disabled"])

    def on_entry_changed(self):
        self._view.validate_stack_automaton.set("")

    def return_button(self):
        controller = Automaton.AutomatonController(self._app)
