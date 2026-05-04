class BankAccount:
    def __init__(self, balance):
        # private variable
        self._balance = balance

    @property
    def balance(self):
        # Getter
        return self._balance

    @balance.setter
    def balance(self, value):
        # Setter
        if not isinstance(value, (int, float)):
            return NotImplemented
        if value < 0:
            raise ValueError("Balance cannot be negative.")
        self._balance = value

    def __repr__(self):
        return f"BankAccount(balance={self.balance!r})"


account_163 = BankAccount(540394)
account_163.balance = 63567
print(f"Balance: {account_163.balance}")
