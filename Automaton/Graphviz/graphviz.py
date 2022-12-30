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


def create_mini_table_diagraph(stack, entry) -> str:
    lines = []
    lines.append("node [shape=record];")
    lines.append('"node" [')
    lines.append('label =<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">')

    lines.append("<tr>")
    lines.append("<td><B>Pila</B></td>")
    lines.append("<td><B>Entrada</B></td>")
    lines.append("</tr>")

    lines.append("<tr>")
    lines.append(f"<td>{stack}</td>")
    lines.append(f"<td>{entry}</td>")
    lines.append("</tr>")

    lines.append("</TABLE>>")
    lines.append('shape="none"')
    lines.append("];")
    return "\n".join(lines)


def create_colored_diagraph(
    stack_automaton: StackAutomaton, current_tranistion: Transition, last_item=False
) -> str:
    lines: list[str] = []

    lines.append("rankdir=LR;")

    lines.append(";".join(stack_automaton.states) + ";")

    # add acceptance state
    for state in stack_automaton.acceptance_states:
        lines.append(state + " [peripheries=2];")

    if not last_item:
        lines.append(current_tranistion.origin + ' [style=filled fillcolor="#96CDFB"];')
    else:
        lines.append(
            current_tranistion.destination + ' [style=filled fillcolor="#96CDFB"];'
        )

    # add transitions
    for transition in stack_automaton.transitions:
        temp_str = (
            " -> ".join([transition.origin, transition.destination])
            + ' [label="'
            + ",".join([transition.entry, transition.pop_stack])
            + ";"
            + transition.push_stack
        )
        if transition != current_tranistion or last_item:
            temp_str = temp_str + '"];'
        else:
            temp_str = temp_str + '" fontcolor="red"];'

        lines.append(temp_str)

    return "\n".join(lines)
