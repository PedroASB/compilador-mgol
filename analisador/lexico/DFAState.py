class DFAState:
    def __init__(self, nome):
        self.name = nome
    
    def __eq__(self, b):
        return self.name == b.name