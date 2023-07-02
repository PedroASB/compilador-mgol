class Production:
    def __init__(self, left: str, right: list[str]):
        self.left = left
        self.right = right
        self.cardinality = len(right)
    
    def __str__(self) -> str:
        return ' '*(40-len(self.left)) + self.left + ' -> ' + ' '.join(self.right)