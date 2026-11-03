# 3.1: FamilySubscription.__init__ is missing super().__init__(user, months), so self.months and self.base_monthly are never set. Python does not require attributes to be declared upfront, so the AttributeError only occurs when price() tries to read self.months.
# 3.4: Only the parent Subscription class had to be opened to change VAT_PERCENT because VAT calculation is centralized in Subscription.price().

class Subscription:
    VAT_PERCENT = 12

    def __init__(self, user: str, months: int):
        self.user = user
        self.months = months
        self.base_monthly = 50_000

    def net(self) -> int:
        return self.base_monthly * self.months

    def price(self) -> int:
        return self.net() * (100 + self.VAT_PERCENT) // 100


class StudentSubscription(Subscription):
    def net(self) -> int:
        return super().net() // 2


class FamilySubscription(Subscription):
    def __init__(self, user: str, months: int, members: list[str]):
        super().__init__(user, months)
        self.members = members

    def net(self) -> int:
        extra = 20_000 * (len(self.members) - 1) * self.months
        return super().net() + extra


# --- Tests ---
def test_subscription_prices_with_12_percent_vat():
    std = Subscription("ali", 3)
    student = StudentSubscription("vali", 3)
    family = FamilySubscription("gani", 3, ["gani", "m2", "m3", "m4"])

    assert std.price() == 168_000       # 150,000 * 1.12
    assert student.price() == 84_000    # 75,000 * 1.12
    assert family.price() == 369_600    # (150,000 + 180,000) * 1.12


def test_changing_vat_in_one_place(monkeypatch):
    monkeypatch.setattr(Subscription, "VAT_PERCENT", 15)
    assert Subscription("ali", 3).price() == 172_500
    assert StudentSubscription("vali", 3).price() == 86_250
    assert FamilySubscription("gani", 3, ["a", "b", "c", "d"]).price() == 379_500

