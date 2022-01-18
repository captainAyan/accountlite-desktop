
class Ledger:

    REVENUE = 0
    EXPENDITURE = 1
    ASSET = 2
    LIABILITY = 3
    EQUITY = 4

    def __init__(self, _id, _type, name):
        self.id = _id
        self.type = _type
        self.name = name

    def stringify(self):
        return "L" + str(self.id) + "," + str(self.type) + "," + self.name
