from typing import TypeAlias
from .DFAState import DFAState

TransitionsList: TypeAlias = list[tuple[DFAState, str | set[str], DFAState]]

class DFA:
    
    def __init__(self,
                 alphabet: list[str],
                 states: list[DFAState],
                 initial_state: DFAState,
                 accept_states: list[DFAState],
                 transitions: TransitionsList,
                ):
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.transitions = DFA.process_transitions(transitions)
        self.current_state = initial_state

        # TODO: Extract this validation to a function
        for state in self.states:
            assert state.name != 'invalid', "Um estado criado por usuário não pode ser nomeado 'invalid'"

        for transition in self.transitions:
            transition_state_from, transition_symbol, transition_state_to = transition
            assert transition_state_from in self.states and transition_state_to in self.states, "A transição contém um estado que não pertence ao conjunto de estados do DFA: " + transition_state_from.name + ' : "' + transition_symbol + '" -> ' + transition_state_to.name
    
    def go_to_next_state(self, symbol: str):
        assert symbol in self.alphabet, f"O símbolo \"{symbol}\" não pertence ao alfabeto do DFA"
        next_state: DFAState = self.get_next_state(symbol)
        assert next_state.name != 'invalid', f"Transição inválida: {self.current_state.name} : {symbol}"
        self.current_state = next_state

    def get_next_state(self, symbol: str):
        next_state: DFAState = DFAState("invalid")
        for transition in self.transitions:
            transition_state_from, transition_symbol, _ = transition 
            if (transition_state_from, transition_symbol) == (self.current_state, symbol):
                next_state = transition[2]
                break
        return next_state
    
    def reinit(self):
        self.go_to_initial_state()

    def go_to_initial_state(self):
        self.current_state = self.initial_state

    def consume_string(self, string: str):
        for symbol in list(string):
            self.go_to_next_state(symbol)

    def accepts(self, string: str) -> bool:
        self.consume_string(string)
        return self.is_in_accept_state()
    
    def is_in_accept_state(self):
        return self.current_state in self.accept_states
    
    def is_in_initial_state(self):
        return self.current_state == self.initial_state
    
    @staticmethod
    def process_transitions(transitions: TransitionsList):
        # Expands transitions on 'set of symbols'
        processed_transitions: TransitionsList = []
        for transition in transitions:
            transition_symbol_or_symbols = transition[1]
            if isinstance(transition_symbol_or_symbols, set):
                transition_expansion = []
                for c in transition_symbol_or_symbols:
                    transition_expansion.append((transition[0], c, transition[2]))
                processed_transitions.extend(transition_expansion)
            else:
                processed_transitions.append(transition)
        return processed_transitions
    
    def compile_to_zuzak_fsm_simulator(self):
        output = ""
        output += "#states\n"
        for state in self.states:
            output += f"{state.name}\n"
        output += "#initial\n"
        output += f"{self.initial_state.name}\n"
        output += "#accepting\n"
        for state in self.accept_states:
            output += f"{state.name}\n"
        output += "#alphabet\n"
        for symbol in self.alphabet:
            symbol = symbol if symbol != '\n' else '¬'
            output += f"{symbol}\n"
        output += "#transitions\n"
        for transition in self.transitions:
            symb = transition[1] if transition[1] != '\n' else '¬'
            output += f"{transition[0].name}:{symb}>{transition[2].name}\n"
        return output





