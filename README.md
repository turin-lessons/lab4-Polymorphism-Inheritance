# Lab 4B — Inheritance, Polymorphism and Composition

**Course:** Design of Software System  
**Institution:** Turin Polytechnic University in Tashkent  

## Overview

This repository contains the solutions and unit tests for **Lab 4B**, which focuses on object-oriented design principles in Python:
- **Inheritance & Abstract Base Classes (`abc`)**
- **Polymorphism & the Open/Closed Principle**
- **Composition vs. Inheritance (`has-a` vs. `is-a`)**
- **Duck Typing & Static Protocols (`typing.Protocol`)**
- **Value Objects & Operator Overloading (`@dataclass(frozen=True)`)**
- **Method Binding & Default Argument Pitfalls**
- **Cooperative Multiple Inheritance, Mixins & MRO (`__mro__`)**
- **Factory / Registry Pattern at System Boundaries**

Each task (`task01.py` – `task10.py`) resolves a realistic production design bug, includes short architectural explanations in comments at the top of the file, and provides `pytest` unit tests in the same file.

---

## Project Structure

```text
.
├── task01.py   # Polymorphic PaymentMethod hierarchy & Checkout refactoring
├── task02.py   # Abstract Notifier base class & Template Method pattern
├── task03.py   # Subscription hierarchy with centralized VAT & super().__init__()
├── task04.py   # Append-only AuditLog using composition instead of inheriting list
├── task05.py   # Employee & Role composition with role history for promotions
├── task06.py   # Duck typing & typing.Protocol (Writable) for report exporting
├── task07.py   # Immutable Money value object with operator overloading
├── task08.py   # Single search() method avoiding Java-style overloading & mutable defaults
├── task09.py   # Cooperative mixins (Timestamp, Validate, Audit) & MRO ordering
├── task10.py   # Centralized string-to-class payment method registry
└── README.md
```

---

## Requirements & Installation

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install required packages (`pytest`, `mypy`, `pyflakes`):**
   ```bash
   pip install --upgrade pip
   pip install pytest mypy pyflakes
   ```

> **Note for Python 3.9 users:** The lab specifies Python 3.10+, which supports `X | None` union type syntax natively. For compatibility with Python 3.9, `from __future__ import annotations` is included where union type annotations are used.

---

## Running Tests & Static Analysis

### Run all unit tests
```bash
pytest task01.py task02.py task03.py task04.py task05.py task06.py task07.py task08.py task09.py task10.py
```

Or run `pytest` on an individual task:
```bash
pytest task01.py
```

### Run static type checking (Task 6)
```bash
mypy task06.py
```

### Run linter check (Task 8)
```bash
pyflakes task08.py
```

---

## Summary of Tasks

| File | Scenario / Bug | Design Pattern / Fix |
| :--- | :--- | :--- |
| `task01.py` | Adding a payment method required editing an `if/elif` chain in `Checkout`. | Extracted an abstract `PaymentMethod` class and concrete provider subclasses (`Card`, `Click`, `Payme`, `Cash`, `BankTransfer`). |
| `task02.py` | `TelegramNotifier` misspelled `send()` as `sned()` and silently did nothing. | Made `Notifier` an `ABC` with `@abstractmethod def send()`, keeping `notify()` as shared template logic. |
| `task03.py` | `StudentSubscription` missed VAT updates; `FamilySubscription` crashed with `AttributeError`. | Added `super().__init__()` in child classes and centralized VAT calculation in `Subscription.price()`, overriding only `net()`. |
| `task04.py` | `AuditLog(list)` allowed scripts to erase security logs via `.clear()` and `.pop()`. | Replaced inheritance with composition (`self._entries = []`) and exposed only `record()`, `__len__`, `__iter__`, and `last()`. |
| `task05.py` | Promoting a `Lecturer` to `HeadOfDepartment` required deleting the employee object and changing IDs. | Replaced `Employee` subclasses with a composable `Role` hierarchy (`LecturerRole`, `HeadRole`) and tracked `role_history`. |
| `task06.py` | `export_report` checked `isinstance(target, io.IOBase)`, rejecting `S3Upload`. | Removed `isinstance` check in favor of duck typing and enforced static type safety with `typing.Protocol` (`Writable`). |
| `task07.py` | Financial reports summed `USD` and `UZS` amounts together as raw integers. | Created an immutable `@dataclass(frozen=True)` `Money` value object with currency-safe `+`, `*`, `<`, `==`, and `sum()` support. |
| `task08.py` | Defining `search()` twice in `ProductSearch` overwrote the first method, causing `TypeError`. | Unified into `search(self, query, filters=None)` without mutable default arguments. |
| `task09.py` | `ValidateMixin` omitted `super().save()`, silently stopping database saves and audit logging. | Restored cooperative `super().save()` chain across mixins and raised `ValueError` when validation fails. |
| `task10.py` | Multiple modules parsed payment strings (`"Payme"`, `"payme"`) inconsistently with duplicate `if/elif` blocks. | Built a single normalized `PAYMENT_REGISTRY` factory (`create_payment_method`) at the system boundary. |
