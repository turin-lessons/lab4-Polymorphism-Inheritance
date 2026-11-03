# 4.1: No, an AuditLog is not a list because a list is a mutable collection, whereas an audit log is strictly append-only. Methods that break the audit rule include clear(), pop(), sort(), remove(), and reverse().
# 4.3: Use a tuple (e.g., (user, action)) or a frozen dataclass/NamedTuple because tuples are immutable and cannot be modified after creation.
# 4.4: Overriding a few methods is fragile because list has 11 public mutating/access methods (47 attributes total in dir(list), 11 public methods) such as remove(), reverse(), sort(), __setitem__, and __delitem__, and missing even one leaves a security hole.

import pytest


class AuditLog:
    def __init__(self):
        self._entries: list[tuple[str, str]] = []

    def record(self, user: str, action: str) -> None:
        self._entries.append((user, action))

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries)

    def last(self, n: int) -> list[tuple[str, str]]:
        return list(self._entries[-n:]) if n > 0 else []


# --- Tests ---
def test_audit_log_operations():
    log = AuditLog()
    log.record("admin", "approve_loan#77")
    log.record("user1", "login")
    log.record("user1", "transfer")

    assert len(log) == 3
    assert list(log) == [
        ("admin", "approve_loan#77"),
        ("user1", "login"),
        ("user1", "transfer"),
    ]
    assert log.last(2) == [("user1", "login"), ("user1", "transfer")]


def test_audit_log_cannot_be_mutated():
    log = AuditLog()
    log.record("admin", "approve_loan#77")

    with pytest.raises(AttributeError):
        log.clear()
    with pytest.raises(AttributeError):
        log.sort()
    with pytest.raises(TypeError):
        log[0] = ("hacker", "erase")

