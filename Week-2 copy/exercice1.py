class Currency:
    def __init__(self, currency, amount):
        self.currency = currency
        self.amount = amount
    def __str__(self): 
        return f"{self.amount} {self.currency}s"
    def __repr__(self):
        return f"Currency('{self.currency}', {self.amount})"
    def __int__(self):
        return int(self.amount)
    def __add__(self, other):
        if isinstance(other, Currency) and self.currency == other.currency:
            return self.amount + other.amount
        else:
            raise TypeError(f"Cannot add between currencies type {self.currency} and {other.currency}")
    def __iadd__(self, other):
        if isinstance(other, Currency) and self.currency == other.currency:
            self.amount += other.amount
            return self
        else:
            raise TypeError("Cannot add different currencies or non-Currency objects")
        