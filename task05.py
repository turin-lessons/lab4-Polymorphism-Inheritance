# 5.1: No, "a lecturer is an employee" does not hold as a permanent identity because a person stays the same employee when their job title changes. On promotion, only the employee's role and pay calculation change, not their identity.
# 5.4: Employee has a composition ("has-a" with strong ownership) relationship with its role history, as the history belongs exclusively to that Employee instance and has no independent lifecycle.

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date


class Role(ABC):
    @abstractmethod
    def monthly_pay(self) -> int:
        pass


class LecturerRole(Role):
    def __init__(self, hours: int):
        self.hours = hours

    def monthly_pay(self) -> int:
        return self.hours * 120_000


class HeadRole(Role):
    def __init__(self, salary: int):
        self.salary = salary

    def monthly_pay(self) -> int:
        return self.salary + 3_000_000


class Employee:
    def __init__(self, emp_id: int, name: str, role: Role, start_date: date = date.today()):
        self.emp_id = emp_id
        self.name = name
        self.role = role
        self.role_history: list[tuple[Role, date]] = [(role, start_date)]

    def change_role(self, new_role: Role, start_date: date = date.today()) -> None:
        self.role = new_role
        self.role_history.append((new_role, start_date))

    def monthly_pay(self, on_date: date | None = None) -> int:
        if on_date is None:
            return self.role.monthly_pay()
        active_role = self.role_history[0][0]
        for role, start in self.role_history:
            if start <= on_date:
                active_role = role
        return active_role.monthly_pay()


# --- Tests ---
def test_promotion_preserves_identity_and_history():
    emp = Employee(101, "Dilshod", LecturerRole(hours=100), start_date=date(2026, 1, 1))
    access_list = [emp]

    assert emp.monthly_pay() == 12_000_000

    emp.change_role(HeadRole(salary=14_000_000), start_date=date(2026, 3, 1))

    assert access_list[0] is emp
    assert emp.emp_id == 101
    assert emp.monthly_pay() == 17_000_000
    assert emp.monthly_pay(on_date=date(2026, 2, 15)) == 12_000_000
    assert len(emp.role_history) == 2
