from io import TextIOWrapper
from analisador.lexico.types import TransitionsList
from . import consts
from .DFAState import DFAState
from .DFA import DFA

class DFAReader:
    def __init__(self, file_: TextIOWrapper):
        self.states: list[DFAState] = []
        self.alphabet: list[str] = []
        self.initial_state: DFAState = DFAState('None')
        self.accept_states: list[DFAState] = []
        self.transitions: TransitionsList = []
        self.file = file_

    def __del__(self):
        if self.file:
            self.file.close()

    def read_states(self):
        while (line := self.file.readline().strip()) != "":
            self.states.append(DFAState(line))

    def read_alphabet(self):
        while (line := self.file.readline().strip()) != "":
            try:
                self.alphabet.extend(consts.alphabet_dictionary[line])
            except KeyError as e:
                raise ('Esse conjunto não existe: ' + line) from e

    def read_initial_state(self):
        while (line := self.file.readline().strip()) != "":
            self.initial_state = DFAState(line)

    def read_accept_states(self):
        while (line := self.file.readline().strip()) != "":
            self.accept_states.append(DFAState(line))

    def read_transitions(self):
        while (line := self.file.readline().strip()) != "":
            state_from, symbol_set, state_to = line.split(',')
            try:
                processed_symbols = consts.alphabet_dictionary[symbol_set]
            except KeyError as e:
                raise ('Esse conjunto não existe: ' + symbol_set) from e
            
            self.transitions.append((DFAState(state_from), processed_symbols, DFAState(state_to)))

    def read(self) -> DFA:
        while (line := self.file.readline().strip()) != "":
            match line:
                case '#states':
                    self.read_states()
                case '#alphabet':
                    self.read_alphabet()
                case '#initial':
                    self.read_initial_state()
                case '#accepting':
                    self.read_accept_states()
                case '#transitions':
                    self.read_transitions()
                case _:
                    print("Arquivo descritor do autômato com formato incorreto")
                    break

        return DFA(self.alphabet, self.states, self.initial_state, 
                   self.accept_states, self.transitions)

