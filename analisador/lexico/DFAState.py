class DFAState:
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, b):
        return self.name == b.name