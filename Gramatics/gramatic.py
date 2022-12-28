separator = ";"

MINIMUM_STRING_LENGHT = 1


class Production:
    def __init__(self, origin, destinations) -> None:
        self.origin = origin
        self.destinations = destinations

    def __str__(self) -> str:
        return f"{self.origin} &gt; {self.destinations}"


class Gramatic:
    def __init__(self, name: str) -> None:
        self.name = name
        self._no_terminals: list[str] = []
        self._terminals: list[str] = []
        self._initial_no_terminal: str = ""
        self._productions: list[Production]
        if name == "":
            raise NameException("Name is empty")

    @property
    def no_terminals(self):
        return self._no_terminals

    @no_terminals.setter
    def no_terminals(self, value: str):
        new_no_terminals: list[str] = value.split(separator)
        if len(new_no_terminals) == 0 or value == "":
            raise NoTerminalsException("The no terminals property is Empty")

        # there are duplicates
        if not len(new_no_terminals) == len(set(new_no_terminals)):
            raise NoTerminalsException("There is duplicates")

        self._no_terminals: list[str] = new_no_terminals

    @property
    def terminals(self):
        return self._terminals

    @terminals.setter
    def terminals(self, value: str):
        if len(self._no_terminals) == 0:
            raise TerminalsException("no_terminals property is empty")

        new_terminals = value.split(separator)
        # if there are duplicate items in the terminals we raise an error
        if len(new_terminals) != len(set(new_terminals)):
            raise TerminalsException("Duplicate items in terminals list")

        for item in new_terminals:
            if item in self._no_terminals:
                raise TerminalsException(
                    "Item of terminals is in no_terminals list property"
                )

        self._terminals = new_terminals

    @property
    def initial_no_terminal(self):
        return self._initial_no_terminal

    @initial_no_terminal.setter
    def initial_no_terminal(self, value: str):
        new_initial_no_terminal = value
        if new_initial_no_terminal not in self._no_terminals:
            raise InitialStateException(
                "Initial state item is not declared in no_terminals property"
            )
        self._initial_no_terminal = new_initial_no_terminal

    @property
    def productions(self):
        return self._productions

    @productions.setter
    def productions(self, value: str):
        new_productions = value.split(";")
        # remove extra empty spaces
        new_productions = list(map(lambda trans: trans.strip(), new_productions))
        # clean empty strings
        new_productions = filter(lambda x: not x == "", new_productions)
        new_productions_list = []

        def validate_destinations(string: str) -> list[str]:
            production = string.split(" ")

            no_terminal = []
            terminal = []

            is_terminal = lambda item: True if item in self._terminals else False
            is_no_terminal = lambda item: True if item in self._no_terminals else False

            for item in production:
                if is_terminal(item):
                    terminal.append(item)
                elif is_no_terminal(item):
                    no_terminal.append(item)

            if len(no_terminal) == 0 and len(terminal) == 0:
                raise Exception("The characters dont match terminal and no terminal")

            return production

        try:
            for production in new_productions:
                splited_trans = production.split(">")
                if len(splited_trans) == 1:
                    raise Exception("The syntax is not correct")

                # 'A' '0 B 0'
                if len(splited_trans) == 2:
                    pass
                else:
                    raise Exception("The syntax is not correct")

                # '0'     'B'
                destinations = validate_destinations(splited_trans[1])

                new_productions_list.append(Production(splited_trans[0], destinations))

        except:
            raise ProductionsSyntaxException(
                "Production syntax is not formatted correctly"
            )

        self._productions = new_productions_list

    def is_free_of_context(self) -> bool:
        regular_gramatic = True
        for production in self._productions:
            if len(production.destinations) > 2:
                regular_gramatic = False

        return not regular_gramatic

    def __str__(self):
        return f"Name: {self.name}\nNo_Terminals: {self._no_terminals}\nTerminals: {self._terminals}\nInitial State: {self._initial_no_terminal}"


# Exception classes for error handling


class InvalidStringException(Exception):
    pass


class NameException(Exception):
    pass


class NoTerminalsException(Exception):
    pass


class TerminalsException(Exception):
    pass


class InitialStateException(Exception):
    pass


class AcceptanceNoTerminalsException(Exception):
    pass


class ProductionsSyntaxException(Exception):
    pass


class ProductionsException(Exception):
    pass
