# 1.2: Use two separate classes (Click and Payme) rather than one class with two instances.
# Although their fee formula is identical today, they are independent external providers whose fee rules or refund policies will change independently in the future.
# 1.4: Zero lines of Checkout were changed when adding BankTransfer because Checkout depends only on the abstract PaymentMethod interface (Open/Closed Principle).

from abc import ABC, abstractmethod
import pytest


class PaymentMethod(ABC):
    @property
    @abstractmethod
    def refundable(self) -> bool:
        pass

    @abstractmethod
    def fee(self, amount: int) -> int:
        pass


class Card(PaymentMethod):
    refundable = True

    def fee(self, amount: int) -> int:
        return amount * 15 // 1000


class Click(PaymentMethod):
    refundable = True

    def fee(self, amount: int) -> int:
        return amount * 10 // 1000


class Payme(PaymentMethod):
    refundable = True

    def fee(self, amount: int) -> int:
        return amount * 10 // 1000


class Cash(PaymentMethod):
    refundable = False

    def fee(self, amount: int) -> int:
        return 0


class BankTransfer(PaymentMethod):
    refundable = True

    def fee(self, amount: int) -> int:
        return 5_000


class Checkout:
    def pay(self, method: PaymentMethod, amount: int) -> dict:
        return {
            "charged": amount + method.fee(amount),
            "refundable": method.refundable,
        }


# --- Tests ---
def test_payment_methods():
    checkout = Checkout()
    assert checkout.pay(Card(), 100_000) == {"charged": 101_500, "refundable": True}
    assert checkout.pay(Click(), 100_000) == {"charged": 101_000, "refundable": True}
    assert checkout.pay(Payme(), 100_000) == {"charged": 101_000, "refundable": True}
    assert checkout.pay(Cash(), 100_000) == {"charged": 100_000, "refundable": False}
    assert checkout.pay(BankTransfer(), 100_000) == {"charged": 105_000, "refundable": True}


def test_payment_method_is_abstract():
    with pytest.raises(TypeError):
        PaymentMethod()

