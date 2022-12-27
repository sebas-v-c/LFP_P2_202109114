from tkinter import *
from tkinter import ttk

import time
import threading

import InitialWindow


TIMER_LENGTH = 5


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None
        parent.title("Pantalla Principal")

        # -----------------------------------Information-------------------------------#
        course_label = ttk.Label(self, text="Lenguajes Formales\ny de Programación")
        course_label.grid(row=1, column=1, sticky="W")

        course_section_label = ttk.Label(self, text="Sección: N")
        course_section_label.grid(row=2, column=1, sticky="W")

        student_name_label = ttk.Label(
            self, text="Sebastian Alejandro\nVásquez Cartagena"
        )
        student_name_label.grid(row=1, column=3, sticky="E")

        student_id_label = ttk.Label(self, text="202109114")
        student_id_label.grid(row=2, column=3, sticky="E")

        title_label = ttk.Label(self, text="SPARK STACK", font=("Arial Bold", 30))
        title_label.grid(row=4, column=2)

        # -----------------------------------Good bye label-------------------------------#
        self.goodbye = StringVar()
        goodbye_label = ttk.Label(
            self, text="", font=("Arial Bold", 15), textvariable=self.goodbye
        )
        goodbye_label.grid(row=6, column=2)

        # -----------------------------------Count Down Label-------------------------------#
        self.countdown = StringVar()
        self.countdown.set("5 s")
        countdown_label = ttk.Label(
            self, text="5 s", font=("Arial Bold", 13), textvariable=self.countdown
        )
        countdown_label.grid(row=7, column=2)

        self.add_padding()

    def create_afd_button_pressed(self):
        if self.controller:
            self.controller.create_afd_button()

    def set_controller(self, controller):
        self.controller = controller

    def add_padding(self, x_size=7, y_size=7):
        for child in self.winfo_children():
            child.grid_configure(padx=x_size, pady=y_size)


class Controller:
    def __init__(self, app, exit=False) -> None:
        # boiler plate code
        self._app = app
        self._view = View(app)
        app.switch_frame(self._view)

        self._view.set_controller(self)

        try:
            thread = threading.Thread(target=self.update_count_down, args=[exit])
            thread.start()
        except:
            pass

        if exit:
            self._view.goodbye.set("¡Hasta La Próxima!")

    def update_count_down(self, exit):
        start_time = time.time()
        interval = 1
        for i in range(1, int(TIMER_LENGTH) + 1):
            time.sleep(start_time + i * interval - time.time())
            self._view.countdown.set(str(TIMER_LENGTH - i) + " s")

        if exit:
            self._app.destroy()
            raise Exception
        else:
            controller = InitialWindow.MenuController(self._app)
