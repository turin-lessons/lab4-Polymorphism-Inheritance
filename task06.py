# 6.1: export_report only needs target to have a write(data: bytes) method that accepts bytes; it does not need target to inherit from io.IOBase.
# 6.4: At runtime, passing an object without write() raises an AttributeError when target.write(...) is first called. Running mypy catches this error statically before the program ever runs because the object does not satisfy the Writable Protocol.

import io
from typing import Iterable, Protocol, Any


class Writable(Protocol):
    def write(self, data: bytes) -> int:
        ...


def export_report(rows: Iterable[Iterable[Any]], target: Writable) -> None:
    for r in rows:
        target.write((",".join(map(str, r)) + "\n").encode())


class S3Upload:
    def __init__(self, bucket: str, key: str):
        self.bucket, self.key = bucket, key
        self.parts: list[bytes] = []

    def write(self, data: bytes) -> int:
        self.parts.append(data)
        return len(data)


class FakeTarget:
    def __init__(self):
        self.buffer = b""

    def write(self, data: bytes) -> int:
        self.buffer += data
        return len(data)


# --- Tests ---
def test_export_report_with_three_unrelated_targets():
    rows = [["id", "amount"], [1, 5000]]
    expected = b"id,amount\n1,5000\n"

    bio = io.BytesIO()
    export_report(rows, bio)
    assert bio.getvalue() == expected

    s3 = S3Upload("reports", "march.csv")
    export_report(rows, s3)
    assert b"".join(s3.parts) == expected

    fake = FakeTarget()
    export_report(rows, fake)
    assert fake.buffer == expected

