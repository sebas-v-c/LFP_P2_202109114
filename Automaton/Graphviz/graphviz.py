from Automaton.stack_automaton import StackAutomaton


def create_diagraph(obj) -> str:
    if isinstance(obj, StackAutomaton):
        return create_stack_automaton_diagraph(obj)
    return ""


def create_description(obj) -> str:
    if isinstance(obj, StackAutomaton):
        return create_stack_automaton_description(obj)
    return ""


def create_route_description(obj, transitions: list, string: str) -> str:
    if isinstance(obj, StackAutomaton):
        return create_stack_automaton_route_description(obj, transitions, string)
    return ""


def create_route_diagraph(obj, transitions: list) -> str:
    if isinstance(obj, StackAutomaton):
        return create_stack_automaton_route_diagraph(obj, transitions)
    return ""


# -------------------------------------StackAutomaton-------------------------------------#
def create_stack_automaton_diagraph(stack_automaton: StackAutomaton) -> str:
    lines: list[str] = []

    lines.append("rankdir=LR;")

    transitions = ";".join(stack_automaton.states) + ";"
    lines.append(transitions)

    # add acceptance state
    for state in stack_automaton.acceptance_states:
        lines.append(state + " [peripheries=2];")

    lines.append('INICIO [shape="triangle"]')
    lines.append("INICIO -> " + stack_automaton.initial_state + ";")
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


def create_stack_automaton_description(stack_automaton: StackAutomaton) -> str:
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


def create_stack_automaton_route_description(
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


def create_stack_automaton_route_diagraph(
    stack_automaton: StackAutomaton, transitions: list
) -> str:
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
