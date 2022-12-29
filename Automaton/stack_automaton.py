separator = ";"


class Transition:
    def __init__(self, origin, entry, pop_stack, destination, push_stack) -> None:
        self.origin = origin
        self.entry = entry
        self.pop_stack = pop_stack
        self.destination = destination
        self.push_stack = push_stack

    def __str__(self) -> str:
        return f"{self.origin}, {self.entry}; {self.destination}"


class StackAutomaton:
    def __init__(self, name: str) -> None:
        self.name = name
        self._states: list[str] = []
        self._alfabet: list[str] = []
        self._stack_alfabet: list[str] = []
        self._initial_state: str = ""
        self._acceptance_states: list[str] = []
        self._transitions: list[Transition]
        if name == "":
            raise NameException("Name is empty")

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, value: str):
        new_states: list[str] = value.split(separator)
        if len(new_states) == 0 or value == "":
            raise StatesException("The states property is Empty")

        # there are duplicates
        if not len(new_states) == len(set(new_states)):
            raise StatesException("There is duplicates")

        self._states: list[str] = new_states

    @property
    def alfabet(self):
        return self._alfabet

    @alfabet.setter
    def alfabet(self, value: str):
        if len(self._states) == 0:
            raise AlfabetException("states property is empty")

        new_alfabet = value.split(separator)
        # if there are duplicate items in the alfabet we raise an error
        if len(new_alfabet) != len(set(new_alfabet)):
            raise AlfabetException("Duplicate items in alfabet list")

        for item in new_alfabet:
            if item in self._states:
                raise AlfabetException("Item of alfabet is in states list property")

        self._alfabet = new_alfabet

    @property
    def stack_alfabet(self):
        return self._stack_alfabet

    @stack_alfabet.setter
    def stack_alfabet(self, value: str):
        if len(self._states) == 0:
            raise StackAlfabetException("states property is empty")

        new_stack_alfabet = value.split(separator)
        # if there are duplicate items in the alfabet we raise an error
        if len(new_stack_alfabet) != len(set(new_stack_alfabet)):
            raise StackAlfabetException("Duplicate items in stack alfabet list")

        for item in new_stack_alfabet:
            if item in self._states:
                raise StackAlfabetException(
                    "Item of stack alfabet is in states list property"
                )

        self._stack_alfabet = new_stack_alfabet

    @property
    def initial_state(self):
        return self._initial_state

    @initial_state.setter
    def initial_state(self, value: str):
        new_initial_state = value
        if new_initial_state not in self._states:
            raise InitialStateException(
                "Initial state item is not declared in states property"
            )
        self._initial_state = new_initial_state

    @property
    def acceptance_states(self):
        return self._acceptance_states

    @acceptance_states.setter
    def acceptance_states(self, value: str):
        new_acceptance_states = value.split(separator)
        for item in new_acceptance_states:
            if item not in self._states:
                raise AcceptanceStatesException(
                    "Acceptance state item is not declared in states property"
                )
        self._acceptance_states = new_acceptance_states

    @property
    def transitions(self):
        return self._transitions

    @transitions.setter
    def transitions(self, value: str):
        """The transition must have the format A,a,$;B,a separated by a \n character"""
        new_transitions = value.split("\n")
        new_transitions = filter(lambda x: not x == "", new_transitions)
        new_transitions_list = []
        try:
            for transition in new_transitions:
                # split transition
                splited_transition = transition.split(",")
                last_item = splited_transition.pop(-1)
                destination = splited_transition.pop(-1)
                destination = destination.split(";")
                splited_transition = splited_transition + destination + [last_item]

                new_transitions_list.append(
                    Transition(
                        origin=splited_transition[0],
                        entry=splited_transition[1],
                        pop_stack=splited_transition[2],
                        destination=splited_transition[3],
                        push_stack=splited_transition[4],
                    )
                )
        except:
            raise TransitionsSyntaxException(
                "Transition syntax is not formatted correctly"
            )

        self._transitions = new_transitions_list

    def evaluate_string(self, string: str) -> list[Transition]:
        # TODO change this code validate with lambda and a stack
        transitions: list[Transition] = []
        state = self.initial_state
        # current_state = self.initial_state
        string_list = list(string)
        in_acceptance_state = False

        for char in string_list:
            # if character is not in alfabet
            if char not in self.alfabet:
                raise InvalidStringException(
                    "The character doesn't belong to the alfabet"
                )
            # given the current state get available transitions
            available_transitions: list[Transition] = list(
                filter(lambda transition: transition.origin == state, self.transitions)
            )

            # given the available transitions, get the correct one
            correct_transition: list[Transition] = list(
                filter(
                    lambda transition: transition.entry == char,
                    available_transitions,
                )
            )

            if len(correct_transition) == 0:
                raise InvalidStringException("There is no transition with this letter")

            state = correct_transition[0].destination
            transitions.append(correct_transition[0])

            if state in self._acceptance_states:
                in_acceptance_state = True
            else:
                in_acceptance_state = False

        if not in_acceptance_state:
            raise InvalidStringException("The string ended in no acceptance state")

        return transitions

    def __str__(self):
        return f"Name: {self.name}\nStates: {self._states}\nAlfabet: {self._alfabet}\nInitial State: {self._initial_state}\nAcceptance States: {self._acceptance_states}"


# Exception classes for error handling


class InvalidStringException(Exception):
    pass


class NameException(Exception):
    pass


class StatesException(Exception):
    pass


class AlfabetException(Exception):
    pass


class StackAlfabetException(Exception):
    pass


class InitialStateException(Exception):
    pass


class AcceptanceStatesException(Exception):
    pass


class TransitionsSyntaxException(Exception):
    pass


class TransitionException(Exception):
    pass
