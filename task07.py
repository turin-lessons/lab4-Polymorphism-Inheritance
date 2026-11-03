# 7.1: @dataclass(order=True) compares fields as a tuple (amount, currency) without checking if currencies match, so Money(100, 'USD') > Money(1, 'UZS') returns True instead of raising CurrencyMismatchError.
# 7.2: sum() starts with integer 0 and evaluates 0 + first_item, which calls int.__add__(0, Money) and fails with TypeError unless Money.__radd__ handles 0. In production, passing start=Money(0, 'UZS') is cleaner and works even on empty lists, though supporting 0 in __radd__ makes bare sum(items) convenient.
# 7.3: __add__ and __eq__ (and __lt__) must return NotImplemented when the other operand is not Money, allowing Python to try the other object's reflected method or fall back cleanly.
# 7.4: Money * Money has no real-world meaning ("square dollars") and must not be supported; Money / Money could mean a dimensionless ratio, but unless explicitly required it is safer to omit or keep separate from scalar multiplication.

from dataclasses import dataclass
import pytest


class CurrencyMismatchError(ValueError):
    pass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(f"Cannot combine {self.currency} and {other.currency}")

    def __add__(self, other: object) -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __radd__(self, other: object) -> "Money":
        if other == 0:
            return self
        return NotImplemented

    def __mul__(self, factor: object) -> "Money":
        if not isinstance(factor, int):
            return NotImplemented
        return Money(self.amount * factor, self.currency)

    def __rmul__(self, factor: object) -> "Money":
        return self.__mul__(factor)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return self.amount < other.amount


# --- Tests ---
def test_money_operations():
    m1 = Money(500, "UZS")
    m2 = Money(300, "UZS")
    usd = Money(100, "USD")

    assert m1 + m2 == Money(800, "UZS")
    assert m1 * 3 == Money(1500, "UZS")
    assert 3 * m1 == Money(1500, "UZS")
    assert m2 < m1
    assert (m1 == 500) is False
    assert sum([m1, m2]) == Money(800, "UZS")
    assert {m1: "five hundred"}[Money(500, "UZS")] == "five hundred"

    with pytest.raises(CurrencyMismatchError):
        _ = m1 + usd

    with pytest.raises(CurrencyMismatchError):
        _ = m1 < usd

