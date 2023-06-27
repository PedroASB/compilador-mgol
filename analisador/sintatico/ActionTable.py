import csv

class ActionTable:
    # action: tupla[estado, terminal, tupla[ação, produção]]
    def __init__(self, csv_actions_file):
        csvfile = csv.reader(open(csv_actions_file, 'r', encoding='utf-8'))
        header = next(csvfile)
        self.actions = []
        for row in csvfile:
            row_state = row[0]
            for i, value in enumerate(row[1:]):
                if value != '':
                    self.actions.append((int(row_state), header[i+1], (value[0], int(value[1:]) if value[1:] != '' else -1)))

    def get_action(self, state: int, terminal: str) -> tuple[str, int] | None:
        try:
            return next((action[2] for action in self.actions if action[0] == state and action[1] == terminal))
        except StopIteration:
            return None

    def get_actions_for_state(self, state: int):
        return list(([action[1], action[2]] for action in self.actions if action[0] == state))