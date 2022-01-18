
class Entry:
    def __init__(self, _id, amount, time, debit_id, credit_id, narration):
        self.id = _id
        self.amount = amount
        self.time = time
        self.debit_id = debit_id
        self.credit_id = credit_id
        self.narration = narration

    def stringify(self):
        return "E" + str(self.id) + "," + str(self.amount) + "," + str(self.time) + "," + str(self.debit_id) + "," \
               + str(self.credit_id) + "," + self.narration
