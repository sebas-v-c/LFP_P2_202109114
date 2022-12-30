from tkinter import *
from tkinter import ttk

import Gramatics

from graphviz import Graph

FILE_NAME = "Res/out_tree"


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None
        parent.title("Árbol de Derivación")

        # -----------------------------------Information-------------------------------#
        title_label = ttk.Label(
            self, text="Árbol De Derivación", font=("Arial Bold", 20)
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

        # -----------------------------------Image-------------------------------#

        self.canvas = Canvas(
            self,
            width=500,
            height=900,
        )
        self.canvas.grid(row=3, column=0, columnspan=2, sticky="WE")
        # imgobj = PhotoImage(file="./Res/afd_help.png")
        # self.imgObj = imgobj
        # canvas.create_image(20, 20, anchor="nw", image=imgobj)

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

    def set_image(self, imgObj):
        self.imgObj = imgObj
        self.canvas.create_image(20, 20, anchor="nw", image=self.imgObj)

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

        # Generacion de grafica
        dot = Graph(
            name="GramaticaLC", encoding="utf-8", format="png", filename="GramaticasLC"
        )
        dot.attr(rankdir="TB", layout="dot", shape="none")

        numero = -1
        listaP = []
        indice = 0
        lista_Nodos = []
        for production in gramatic.productions:
            aux = 0
            if lista_Nodos[:] != []:
                for x in lista_Nodos:
                    if production.origin == x:
                        indice = aux
                    aux += 1
            else:
                numero += 1
                dot.node(
                    name="node" + str(numero), label=production.origin, shape="none"
                )
                lista_Nodos.append(production.origin)

            for destination in production.destinations:
                numero += 1
                dot.node(name="node" + str(numero), label=destination, shape="none")
                listaP.append(numero)
                lista_Nodos.append(destination)
            for z in listaP:
                dot.edge("node" + str(indice), "node" + str(z))
            listaP = []
            aux = 0
        dot.render(FILE_NAME, format="png")

        self._view.set_image(PhotoImage(file=FILE_NAME + ".png"))
