from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile


import Automaton
import Gramatics


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None
        parent.title("Carga De Archivos")

        # -----------------------------------Title-------------------------------#
        title_label = ttk.Label(self, text="Carga De Archivos", font=("Arial Bold", 20))
        title_label.grid(row=1, column=2)

        # -----------------------------------Path-------------------------------#
        path_label = ttk.Label(self, text="Ruta: ")
        path_label.grid(row=2, column=1, sticky="e")

        self.path = StringVar()
        path_entry = ttk.Entry(self, textvariable=self.path)
        path_entry.grid(row=2, column=3)

        # -----------------------------------Search File-------------------------------#
        search_button = ttk.Button(
            self, text="Buscar Archivo", command=self.search_button_pressed
        ).grid(column=2, row=3, sticky="ew")

        # -----------------------------------Load File-------------------------------#
        self.load_button = ttk.Button(
            self, text="Cargar Archivo", command=self.load_button_pressed
        )
        self.load_button.grid(column=2, row=4, sticky="ew")
        self.load_button.state(["disabled"])

        # -----------------------------------label error-------------------------------#
        self.label_error = StringVar()
        label_error = ttk.Label(
            self, text="", foreground="green", textvariable=self.label_error
        )
        label_error.grid(column=2, row=6, sticky="ew")

        # -----------------------------------return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=2, row=5)

        self.add_padding()

    # Buttons listeners
    def load_button_pressed(self):
        if self.controller:
            self.controller.load_file()

    def search_button_pressed(self):
        if self.controller:
            self.controller.search_file()

    def set_controller(self, controller):
        self.controller = controller

    def return_button_pressed(self):
        if self.controller:
            self.controller.return_button()

    def add_padding(self, x_size=7, y_size=7):
        for child in self.winfo_children():
            child.grid_configure(padx=x_size, pady=y_size)


class Controller:
    def __init__(self, app, gramatics=False, automaton=False) -> None:
        self._app = app
        self._view = View(app)
        app.switch_frame(self._view)

        self.file = None
        self._view.set_controller(self)

        self.gramatics = gramatics
        self.automaton = automaton

    def load_file(self):
        if self.gramatics:
            self._load_gramatics()
        elif self.automaton:
            self._load_automaton()

    def _load_gramatics(self):
        if self.file is None:
            return

        lines: list[str] = self.file.readlines()
        # strip out the new line character
        lines = list(map(lambda x: x.strip("\n"), lines))

        new_afd_list = []
        line_num = 0
        afd_transitions: list[str] = []
        new_afd: AFD
        file_lines = len(lines)

        for line in range(len(lines)):
            if line_num == 0:
                new_afd = AFD(lines[line])

            if lines[line][0] == "%":
                line_num = 0
                new_afd.transitions = "\n".join(afd_transitions)
                new_afd_list.append(new_afd)
                afd_transitions = []
                continue

            # fill afd parameters
            if line_num == 1:
                new_afd.states = lines[line].replace(",", ";")
            elif line_num == 2:
                new_afd.alfabet = lines[line].replace(",", ";")
            elif line_num == 3:
                new_afd.initial_state = lines[line]
            elif line_num == 4:
                new_afd.acceptance_states = lines[line].replace(",", ";")
            elif line_num >= 5:
                afd_transitions.append(lines[line])

            if line == file_lines - 1:
                afd_transitions.append(lines[line])
                new_afd.transitions = "\n".join(afd_transitions)
                new_afd_list.append(new_afd)

            line_num += 1

        self._app.afd_objects = self._app.afd_objects + new_afd_list
        self._view.label_error.set("Archivo cargado con éxito")

    def _load_automaton(self):
        if self.file is None:
            return

        lines: list[str] = self.file.readlines()
        # strip out the new line character
        lines = list(map(lambda x: x.strip("\n"), lines))

        new_gr_list = []
        line_num = 0
        gr_productions: list[str] = []
        new_gr: GR
        file_lines = len(lines)

        for line in range(len(lines)):
            if line_num == 0:
                new_gr = GR(lines[line])

            if lines[line][0] == "%":
                line_num = 0
                new_gr.productions = ";".join(gr_productions)
                new_gr_list.append(new_gr)
                gr_productions = []
                continue

            # fill afd parameters
            if line_num == 1:
                new_gr.no_terminals = lines[line].replace(",", ";")
            elif line_num == 2:
                new_gr.terminals = lines[line].replace(",", ";")
            elif line_num == 3:
                new_gr.initial_no_terminal = lines[line]
            elif line_num >= 4:
                gr_productions.append(lines[line])

            if line == file_lines - 1:
                gr_productions.append(lines[line])
                new_gr.productions = ";".join(gr_productions)
                new_gr_list.append(new_gr)

            line_num += 1

        self._app.gr_objects = self._app.gr_objects + new_gr_list
        self._view.label_error.set("Archivo cargado con éxito")

    def search_file(self):
        file = None
        if self.gramatics:
            file = askopenfile(
                mode="r",
                filetypes=[("Archivos Automata de Pila", "*.ap")],
            )
        elif self.automaton:
            file = askopenfile(
                mode="r",
                filetypes=[("Archivos de Gramaticas", "*.glc")],
            )

        if file is None:
            return

        self._view.load_button.state(["!disabled"])
        self.file = file

    def return_button(self):
        if self.gramatics:
            controller = Gramatics.GramaticsController(self._app)
        elif self.automaton:
            controller = Automaton.AutomatonController(self._app)