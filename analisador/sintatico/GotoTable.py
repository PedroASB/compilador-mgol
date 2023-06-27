import csv

class GotoTable:
    # transition: tupla[estado, não terminal, novo estado]
    def __init__(self, csv_goto_file):
        csvfile = csv.reader(open(csv_goto_file, 'r', encoding='utf-8'))
        header = next(csvfile)
        self.transitions = []
        for row in csvfile:
            row_state = row[0]
            for i, value in enumerate(row[1:]):
                if value != '':
                    self.transitions.append((int(row_state), header[i+1], int(value)))
    
    def get_goto(self, state: int, non_terminal: str) -> int | None:
        try:
            return next((transition[2] for transition in self.transitions if transition[0] == state and transition[1] == non_terminal))
        except StopIteration:
            return None