from collections import defaultdict
from analisador.lexico.Token import Token

class SemanticStack:
    def __init__(self):
        self.stack: list[Token] = []
    
    def pop(self, n=1):
        for _ in range(0, n):
            self.stack.pop()
    
    def top(self) -> Token:
        return self.stack[-1]
    
    def get_named_tokens(self, token_template: list[str]) -> dict[str, Token]:
        tokens = [self.get_then_pop() for _ in token_template]
        tokens.reverse()
        
        names_counter = defaultdict(lambda: 0)
        renamed_token_template = []
        for token_name in token_template:
            renamed_token_template.append(token_name + ('_' + str(names_counter[token_name]) if names_counter[token_name] > 0 else ''))
            names_counter[token_name] += 1

        return {token_name: token for token_name, token in zip(renamed_token_template, tokens)}

    def push(self, value: Token):
        self.stack.append(value)

    def get_then_pop(self) -> Token:
        top = self.top()
        self.pop()
        return top
