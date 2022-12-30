from tkinter import *
from tkinter import ttk

import Automaton
import os
import threading
from PIL import Image, ImageTk

import Automaton.Graphviz as Graphviz

BLANK_FILE_NAME = "Res/blank"
ERROR_FILE_NAME = "Res/error"
DOT_FILE_NAME = "Res/.input.dot"
CURRENT_IMAGE_NAME = "Res/current"


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None
        parent.title("Evaluar Cadena Paso A Paso")

        # -----------------------------------Information-------------------------------#
        title_label = ttk.Label(self, text="Paso A Paso", font=("Arial Bold", 20))
        title_label.grid(row=0, column=0, columnspan=4)

        # -----------------------------------StackAutomaton label-------------------------------#
        automaton_label = ttk.Label(self, text="Autómata")
        automaton_label.grid(row=2, column=0, sticky="E")

        # -----------------------------------StackAutomaton Combobox-------------------------------#
        self.automaton_combobox = StringVar()
        self._automaton_combobox = ttk.Combobox(
            self, textvariable=self.automaton_combobox
        )
        self._automaton_combobox.state(["readonly"])
        self._automaton_combobox.grid(row=2, column=1, sticky="WE")
        self._automaton_combobox.bind("<<ComboboxSelected>>", self.combobox_selected)

        # -----------------------------------string label-------------------------------#
        automaton_label = ttk.Label(self, text="Cadena")
        automaton_label.grid(row=3, column=0, sticky="E")

        # -----------------------------------String-------------------------------#
        self.stack_automaton_string = StringVar()
        self.stack_automaton_string_entry = ttk.Entry(
            self, textvariable=self.stack_automaton_string, width=30
        )
        self.stack_automaton_string_entry.grid(row=3, column=1)
        self.stack_automaton_string_entry.state(["disabled"])

        # -----------------------------------Validate button-------------------------------#
        self.validate_button = ttk.Button(
            self, text="Validar", command=self.validate_button_pressed
        )
        self.validate_button.grid(row=2, column=3, sticky="we")
        self.validate_button.state(["disabled"])
        # -----------------------------------Next step button-------------------------------#
        self.next_step_button = ttk.Button(
            self, text="Siguiente Paso", command=self.next_steps_button_pressed
        )
        self.next_step_button.grid(row=3, column=3, sticky="we")
        self.next_step_button.state(["disabled"])

        # -----------------------------------Image-------------------------------#

        self.canvas = Canvas(
            self,
            width=800,
            height=600,
        )
        self.canvas.grid(row=4, column=0, columnspan=3, sticky="WE")
        # imgobj = PhotoImage(file="./Res/afd_help.png")
        # self.imgObj = imgobj
        # canvas.create_image(20, 20, anchor="nw", image=imgobj)

        # -----------------------------------Return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=0, row=9, columnspan=3)

        self.add_padding()

    def validate_button_pressed(self):
        if self.controller:
            self.controller.validate_button()

    def next_steps_button_pressed(self):
        if self.controller:
            self.controller.next_steps_button()

    def combobox_selected(self, *args):
        self._automaton_combobox.selection_clear()
        if self.controller:
            self.controller.combobox_selected()

    def define_combobox_values(self, values: list):
        self._automaton_combobox["values"] = values

    def set_image(self, imgObj):
        self.imgObj = imgObj
        self.canvas.create_image(5, 5, anchor=NW, image=self.imgObj)

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

        self.steps = []
        self.steps_copy = []
        self._view.set_controller(self)

        # get a list of names
        self._view.define_combobox_values(
            list(map(lambda automaton: automaton.name, app.automaton_objects))
        )

    def return_button(self):
        controller = Automaton.AutomatonController(self._app)

    def validate_button(self):
        cwd = os.getcwd()
        string = self._view.stack_automaton_string.get()

        try:
            self.steps: list[Automaton.Transition] = self.automaton.evaluate_string(
                string
            )
            # copy the array of steps
            self.steps_copy = self.steps.copy()
            # empty this stack
            self.stack = []
            # set to empty the control string
            #
            self.control_string = ""

            diagraph: str = "digraph G{\n" + Graphviz.create_colored_diagraph(
                self.automaton, self.steps_copy[0]
            )
            table: str = (
                "\n" + Graphviz.create_mini_table_diagraph(stack=" ", entry=" ") + "\n}"
            )
        except:
            self.image = Image.open(cwd + "/" + ERROR_FILE_NAME + ".png")
            self.resize_image = self.image.resize((800, 600))
            self._view.set_image(ImageTk.PhotoImage(self.resize_image))
            return

        self._view.validate_button.state(["disabled"])
        self._view.stack_automaton_string_entry.state(["disabled"])
        self._view.next_step_button.state(["!disabled"])

        try:
            os.remove(cwd + "/" + DOT_FILE_NAME)
            os.remove(cwd + "/" + CURRENT_IMAGE_NAME + ".png")
        except:
            pass

        with open(cwd + "/" + DOT_FILE_NAME, mode="w") as f:
            f.write(diagraph + table)

        try:
            os.system(
                "dot -Tpng " + DOT_FILE_NAME + " > " + CURRENT_IMAGE_NAME + ".png"
            )
        except:
            self.image = Image.open(cwd + "/" + ERROR_FILE_NAME + ".png")
            self.resize_image = self.image.resize((800, 600))
            self._view.set_image(ImageTk.PhotoImage(self.resize_image))
            return

        self.image = Image.open(cwd + "/" + CURRENT_IMAGE_NAME + ".png")
        self.resize_image = self.image.resize((800, self.image.height))
        self._view.set_image(ImageTk.PhotoImage(self.resize_image))

    def next_steps_button(self):
        cwd = os.getcwd()
        string = self._view.stack_automaton_string.get()

        last_item = False

        if len(self.steps_copy) == 1:
            # Todo add more things for make this work
            self._view.validate_button.state(["!disabled"])
            self._view.stack_automaton_string_entry.state(["!disabled"])
            self._view.next_step_button.state(["disabled"])
            last_item = True

        if not last_item:
            current_transition = self.steps_copy[1]
        else:
            current_transition = self.steps_copy[0]

        # since we block this button and len = 1 we can be sure that this
        # function cannot throw an error
        if self.steps_copy[0].pop_stack != "$":
            self.stack.pop(0)
        if self.steps_copy[0].push_stack != "$":
            self.stack.insert(0, self.steps_copy[0].push_stack)
        if self.steps_copy[0].entry != "$":
            self.control_string = self.control_string + self.steps_copy[0].entry

        try:
            diagraph: str = "digraph G{\n" + Graphviz.create_colored_diagraph(
                self.automaton, current_transition, last_item=last_item
            )
            table: str = (
                "\n"
                + Graphviz.create_mini_table_diagraph(
                    stack="".join(self.stack), entry=self.control_string
                )
                + "\n}"
            )
        except:
            self.image = Image.open(cwd + "/" + ERROR_FILE_NAME + ".png")
            self.resize_image = self.image.resize((800, 600))
            self._view.set_image(ImageTk.PhotoImage(self.resize_image))
            return

        try:
            os.remove(cwd + "/" + DOT_FILE_NAME)
            os.remove(cwd + "/" + CURRENT_IMAGE_NAME + ".png")
        except:
            pass

        with open(cwd + "/" + DOT_FILE_NAME, mode="w") as f:
            f.write(diagraph + table)

        try:
            os.system(
                "dot -Tpng " + DOT_FILE_NAME + " > " + CURRENT_IMAGE_NAME + ".png"
            )
        except:
            self.image = Image.open(cwd + "/" + ERROR_FILE_NAME + ".png")
            self.resize_image = self.image.resize((800, 600))
            self._view.set_image(ImageTk.PhotoImage(self.resize_image))
            return

        current_transition = self.steps_copy.pop(0)

        self.image = Image.open(cwd + "/" + CURRENT_IMAGE_NAME + ".png")
        self.resize_image = self.image.resize((800, self.image.height))
        self._view.set_image(ImageTk.PhotoImage(self.resize_image))

    def combobox_selected(self):
        # get automaton by name
        name = self._view.automaton_combobox.get()
        self.automaton: Automaton.StackAutomaton = list(
            filter(lambda item: item.name == name, self._app.automaton_objects)
        )[0]

        self._view.stack_automaton_string_entry.state(["!disabled"])
        self._view.validate_button.state(["!disabled"])

        cwd = os.getcwd()

        self.image = Image.open(cwd + "/" + BLANK_FILE_NAME + ".png")
        self.resize_image = self.image.resize((800, 600))
        self._view.set_image(ImageTk.PhotoImage(self.resize_image))
