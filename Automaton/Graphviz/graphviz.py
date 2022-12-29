from Automaton.stack_automaton import StackAutomaton
from Automaton.stack_automaton import Stack
from Automaton.stack_automaton import Transition


# -------------------------------------StackAutomaton-------------------------------------#
def create_diagraph(stack_automaton: StackAutomaton) -> str:
    lines: list[str] = []

    lines.append("rankdir=LR;")

    transitions = ";".join(stack_automaton.states) + ";"
    lines.append(transitions)

    # add acceptance state
    for state in stack_automaton.acceptance_states:
        lines.append(state + " [peripheries=2];")

    # lines.append('INICIO [shape="triangle"]')
    # lines.append("INICIO -> " + stack_automaton.initial_state + ";")
    # add transitions
    for transition in stack_automaton.transitions:
        lines.append(
            " -> ".join([transition.origin, transition.destination])
            + ' [label="'
            + ",".join([transition.entry, transition.pop_stack])
            + ";"
            + transition.push_stack
            + '"];'
        )

    return "\n".join(lines)


def create_description(stack_automaton: StackAutomaton) -> str:
    lines: list[str] = []

    lines.append("node [shape=circle];")
    lines.append("fontsize=40")
    lines.append('NodeLabel [shape=none fontsize=18 fontname = "monospace" label = <')
    lines.append("Nombre: " + stack_automaton.name + "<br/>")

    align_left = '<br align="left"/>'

    lines.append("Estados: " + " ".join(stack_automaton.states) + align_left)
    lines.append("Alfabeto: " + " ".join(stack_automaton.alfabet) + align_left)
    lines.append(
        "Alfabeto De Pila: " + " ".join(stack_automaton.stack_alfabet) + align_left
    )
    lines.append(
        "Estados de aceptación: "
        + " ".join(stack_automaton.acceptance_states)
        + align_left
    )
    lines.append("Estado inicial: " + stack_automaton.initial_state + align_left)
    lines.append(">];")

    return "\n".join(lines)


def create_table_diagraph(transitions: list[Transition], name: str, string: str) -> str:
    lines = []
    # table fabrication code
    lines.append(f"title [shape=none label={name} fontsize=30];")
    lines.append("node [shape=record];")
    lines.append('"node" [')
    lines.append('label =<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">')

    # converting list to a dictionary
    transitions_dict = {
        "Iteración": [num for num in range(len(transitions) + 1)],
        "Pila": [""],
        "Entrada": [string[0:i] for i in range(len(string) + 1)],
        "Transición": [str(step) for step in transitions] + [""],
    }
    # readjust entry values
    while len(transitions_dict["Entrada"]) < len(transitions_dict["Iteración"]):
        transitions_dict["Entrada"].append(string)
    # stack code
    stack_string = []
    for transition in transitions:
        if transition.pop_stack != "$":
            stack_string.pop(0)
        if transition.push_stack != "$":
            stack_string.insert(0, transition.push_stack)
        transitions_dict["Pila"].append("".join(stack_string))

    transitions_dict["Pila"].append("".join(stack_string))

    # Convert dictionary to html table
    # Table headers
    lines.append("<tr>")
    lines.append("<td><B>Iteración</B></td>")
    lines.append("<td><B>Pila</B></td>")
    lines.append("<td><B>Entrada</B></td>")
    lines.append("<td><B>Transición</B></td>")
    lines.append("</tr>")
    for i in range(len(transitions) + 1):
        lines.append("<tr>")
        lines.append(f"<td>{transitions_dict['Iteración'][i]}</td>")
        lines.append(f"<td>{transitions_dict['Pila'][i]}</td>")
        lines.append(f"<td>{transitions_dict['Entrada'][i]}</td>")
        lines.append(f"<td>{transitions_dict['Transición'][i]}</td>")
        lines.append("</tr>")

    # table fabrication code
    lines.append("</TABLE>>")
    lines.append('shape="none"')
    lines.append("];")
    lines.append('title -> "node" [color=none];')
    return "\n".join(lines)


def create_route_diagraph(stack_automaton: StackAutomaton, transitions: list) -> str:
    lines: list[str] = []

    lines.append("rankdir=LR;")
    lines.append("")

    for i in range(len(transitions)):
        lines[1] += str(i) + ";"

    lines.append(str(len(transitions)) + " [peripheries=2];")

    lines.append('INICIO [shape="triangle"]')
    lines.append("INICIO -> 0;")

    for i in range(len(transitions)):
        lines.append(
            " -> ".join([str(i), str(i + 1)])
            + ' [label="'
            + transitions[i].entry
            + '"];'
        )

    return "\n".join(lines)


def create__route_description(
    stack_automaton: StackAutomaton, transitions: list, string: str
) -> str:
    """Generate a description in Graphviz Syntax for the transitions that the
    StackAutomaton took"""
    lines: list[str] = []

    lines.append("node [shape=circle];")
    lines.append("fontsize=40")
    lines.append("NodeLabel [shape=none fontsize=18 label = <")
    lines.append("Nombre: " + stack_automaton.name + "<br/>")

    align_left = '<br align="left"/>'

    lines.append("Estados: " + " ".join(stack_automaton.states) + align_left)
    lines.append("Alfabeto: " + " ".join(stack_automaton.alfabet) + align_left)
    lines.append(
        "Estados de aceptación: "
        + " ".join(stack_automaton.acceptance_states)
        + align_left
    )
    lines.append("Estado inicial: " + stack_automaton.initial_state + align_left)
    lines.append("Transiciones Realizadas: " + align_left)

    num = 1
    for transition in transitions:
        lines.append(str(num) + ". " + str(transition) + align_left)
        num += 1

    lines.append(" " + align_left)
    lines.append("Cadena ingresada: " + string + align_left)
    lines.append(">];")

    return "\n".join(lines)
