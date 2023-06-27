class Production:
    def __init__(self, left: str, right: list[str]):
        self.left = left
        self.right = right
        self.cardinality = len(right)