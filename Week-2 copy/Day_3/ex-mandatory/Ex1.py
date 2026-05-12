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
        if isinstance(other, Currency):
            if self.currency == other.currency:
                return Currency(self.currency, self.amount + other.amount)
            else:
                raise TypeError(f"Cannot add between currencies type {self.currency} and {other.currency}")
        elif isinstance(other, (int, float)):
            return Currency(self.currency, self.amount + other)
        else:
            raise TypeError("Addition with unsupported type")

    def __iadd__(self, other):
        if isinstance(other, Currency):
            if self.currency == other.currency:
                self.amount += other.amount
            else:
                raise TypeError(f"Cannot add between currencies type {self.currency} and {other.currency}")
        elif isinstance(other, (int, float)):
            self.amount += other
        else:
            raise TypeError("Addition with unsupported type")

        return self
        
c1 = Currency('dollar', 5)
c2 = Currency('dollar', 10)
c3 = Currency('shekel', 1)
c4 = Currency('shekel', 10)

print(c1)
print(int(c1))
print(repr(c1))
print(c1 + 5)
print(c1 + c2)
print(c1) 
c1 += 5
print(c1)
c1 += c2
print(c1)

