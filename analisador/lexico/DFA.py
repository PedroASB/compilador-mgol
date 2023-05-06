from collections.abc import Callable
from typing import Any

from .noop import noop
from .DFAState import DFAState

class DFA:
    
    def __init__(self,
                 alphabet: list[str],
                 states: list[DFAState],
                 initial_state: DFAState,
                 accept_states: list[DFAState],
                 # TODO: Change "Callable[[Any, DFAState, str, DFAState]" to "Callable[[DFA, DFAState, str, DFAState]"
                 transitions: list[tuple[DFAState, str | set[str], DFAState, Callable[[Any, DFAState, str, DFAState], Any]]]
                ):
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.transitions = DFA.process_transitions(transitions)
        self.current_state = initial_state

    def go_to_next_state(self, symbol: str):
        assert symbol in self.alphabet, f"O caractere \"{symbol}\" não é parte do alfabeto" # TODO: Improve: detect missing transitions at __init__ time
        
        next_state: DFAState = DFAState("invalid")
        transition_action: Callable[[DFA, DFAState, str, DFAState], Any] = noop
        
        for transition in self.transitions:
            if transition[0] == self.current_state and transition[1] == symbol:
                next_state = transition[2]
                transition_action = transition[3]
        print(self.current_state.name, symbol, next_state.name)

        assert next_state.name != 'invalid', f"Transição inválida: {self.current_state.name} : {symbol}" # TODO: Improve: detect missing transitions at __init__ time
        
        transition_action(self, self.current_state, symbol, next_state)
        self.current_state = next_state

    def reinit(self):
        self.current_state = self.initial_state

    def consume_string(self, string: str):
        for symbol in list(string):
            self.go_to_next_state(symbol)

    def accepts(self, string: str) -> bool:
        self.consume_string(string)
        return self.current_state in self.accept_states
    
    @staticmethod
    def process_transitions(transitions):
        # Expands transitions on 'set of symbols'
        processed_transitions = []
        for transition in transitions:
            transition_symbol_or_symbols = transition[1]
            if isinstance(transition_symbol_or_symbols, set):
                transition_expansion = []
                for c in transition_symbol_or_symbols:
                    transition_expansion.append((transition[0], c, transition[2], transition[3]))
                processed_transitions.extend(transition_expansion)
            else:
                processed_transitions.append(transition)
        return processed_transitions





