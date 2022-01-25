from model.Entry import Entry
from model.Journal import Journal
from model.Ledger import Ledger


class Repository:
    def __init__(self, file_name):
        self.file_name = file_name
        self.meta_data_dict = {}
        self.entries = []
        self.ledgers = []
        self.journals = []

        self.parse(open(self.file_name, 'r').read())

    def add_entry(self, amount, time, debit_name, credit_name, narration):
        debit = None
        credit = None

        for l in self.ledgers:
            if l.name == debit_name:
                debit = l
            elif l.name == credit_name:
                credit = l

            if debit is not None and credit is not None:
                break

        self.entries.append(Entry(len(self.entries) + 1, amount, time, debit.id, credit.id, narration))
        self.journals.append(Journal(len(self.journals) + 1, amount, time, debit, credit, narration))

        open(self.file_name, 'w').write(self.stringify())

    def add_ledger(self, name, _type):
        self.ledgers.append(Ledger(len(self.ledgers)+1, _type, name))
        open(self.file_name, 'w').write(self.stringify())

    def stringify(self):
        output = ""

        for x in self.meta_data_dict:
            b = "#" + x + "=" + self.meta_data_dict[x] + "\n"
            output += b

        for x in self.ledgers:
            output += x.stringify()
            output += "\n"

        for x in self.entries:
            output += x.stringify()
            output += "\n"

        return output

    def parse(self, val):
        lines = val.split("\n")

        for line in lines:
            if line == "":  # a small fix for the empty lines
                continue

            if line[0] == '#':  # meta
                x = line.split("=")
                name = x[0][1:]
                content = line[len(name) + 2:]
                self.meta_data_dict[name] = content

            elif line[0] == 'E':  # entry
                x = line.split(",")

                _id = int(x[0][1:])
                amount = int(x[1])
                time = int(x[2])
                debit_id = int(x[3])
                credit_id = int(x[4])

                l = len(x[0]) + len(x[1]) + len(x[2]) + len(x[3]) + len(x[4]) + 5
                narration = line[l:]

                self.entries.append(Entry(_id, amount, time, debit_id, credit_id, narration))
                self.journals.append(Journal(_id, amount, time, self.ledgers[debit_id - 1], self.ledgers[credit_id - 1],
                                             narration))

            elif line[0] == 'L':  # ledger
                x = line.split(",")

                _id = int(x[0][1:])
                _type = int(x[1])

                l = len(x[0]) + len(x[1]) + 2
                name = line[l:]

                self.ledgers.append(Ledger(_id, _type, name))
