class FixedFloat:
    def __init__(self, amount):
        self.amount = amount


    def __repr__(self):
        return f'<Fixed Float {self.amount:.2f}>'


    @classmethod
    def from_sum(cls, value1, value2):
        return cls(value1 + value2)


new_number = FixedFloat.from_sum(19.574, 0.756)
print(new_number)


class Dollar(FixedFloat):
    def __init__(self, amount):
        super().__init__(amount)
        self.symbol = '$'


    def __repr__(self):
        return f'<Dollar {self.symbol}{self.amount:.2f}>'


money = Dollar.from_sum(16.578, 9.253)
print(money)
