# 9.1: Invoice.__mro__ is (Invoice, TimestampMixin, ValidateMixin, AuditMixin, Model, object). Because ValidateMixin forgot super().save(), the chain stopped at ValidateMixin and never reached AuditMixin or Model.
# 9.2: The lines appear in order: TimestampMixin -> ValidateMixin -> Model.save -> AuditMixin. "write audit entry" appears after INSERT because AuditMixin prints after its super().save() call returns, ensuring we only audit records that were actually saved.
# 9.3: ValidateMixin must raise an exception (e.g., ValueError) rather than returning silently; a silent return lets the caller believe save() succeeded and return "201 Created" even though nothing was written to the database.
# 9.4: With (TimestampMixin, AuditMixin, Model, ValidateMixin), ValidateMixin is never called because Model.save() does not call super().save(), showing that the base class (Model) must always be placed last after all mixins.

import pytest


class Model:
    def save(self):
        print("Model.save: INSERT/UPDATE")


class TimestampMixin:
    def save(self):
        print("TimestampMixin: set updated_at")
        super().save()


class ValidateMixin:
    def save(self):
        print("ValidateMixin: validate fields")
        if getattr(self, "amount", 0) <= 0:
            raise ValueError("Invoice amount must be positive")
        super().save()


class AuditMixin:
    def save(self):
        super().save()
        print("AuditMixin: write audit entry")


class Invoice(TimestampMixin, ValidateMixin, AuditMixin, Model):
    def __init__(self, amount: int = 100):
        self.amount = amount


# --- Tests ---
def test_invoice_save_mro_order(capsys):
    inv = Invoice(amount=500)
    inv.save()
    lines = capsys.readouterr().out.strip().splitlines()
    assert lines == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
        "Model.save: INSERT/UPDATE",
        "AuditMixin: write audit entry",
    ]


def test_invalid_invoice_raises_and_stops_save(capsys):
    bad_inv = Invoice(amount=-10)
    with pytest.raises(ValueError, match="positive"):
        bad_inv.save()

    output = capsys.readouterr().out
    assert "Model.save" not in output
    assert "AuditMixin" not in output

