class SemanticStack:
    def __init__(self):
        self.stack = [0]
    
    def pop(self, n=1):
        for _ in range(0, n):
            self.stack.pop()
    
    def get(self):
        return self.stack[-1]
    
    def push(self, value):
        self.stack.append(value)

    def get_then_pop(self):
        top = self.get()
        self.pop()
        return top
