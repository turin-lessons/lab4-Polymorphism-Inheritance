# 10.4: Having a single string-to-class registry at the HTTP boundary is acceptable because external input arrives as raw strings and must be parsed once, whereas putting if/elif inside Checkout couples core business logic to transport strings and duplicates branching across the codebase.
# 10.5: Adding BankTransfer required changing only one place: adding a single key-value entry to the PAYMENT_REGISTRY dictionary.

import pytest
from task01 import PaymentMethod, Card, Click, Payme, Cash, BankTransfer


class UnknownPaymentMethodError(ValueError):
    pass


PAYMENT_REGISTRY: dict[str, type[PaymentMethod]] = {
    "card": Card,
    "click": Click,
    "payme": Payme,
    "cash": Cash,
    "bank_transfer": BankTransfer,
}


def create_payment_method(name: str) -> PaymentMethod:
    normalized = name.strip().lower()
    cls = PAYMENT_REGISTRY.get(normalized)
    if cls is None:
        supported = ", ".join(sorted(PAYMENT_REGISTRY.keys()))
        raise UnknownPaymentMethodError(
            f"Unknown payment method '{name}'. Supported methods: {supported}"
        )
    return cls()


# --- Tests ---
def test_create_payment_method_normalizes_input():
    assert isinstance(create_payment_method("payme"), Payme)
    assert isinstance(create_payment_method("PAYME"), Payme)
    assert isinstance(create_payment_method("  Payme \n"), Payme)
    assert isinstance(create_payment_method("bank_transfer"), BankTransfer)


def test_unknown_payment_method_lists_supported_options():
    with pytest.raises(UnknownPaymentMethodError) as exc_info:
        create_payment_method("bitcoin")

    msg = str(exc_info.value)
    for supported_name in ["bank_transfer", "card", "cash", "click", "payme"]:
        assert supported_name in msg

