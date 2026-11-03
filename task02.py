# 2.1: Because TelegramNotifier misspelled send() as sned(), calling notify() inherited and executed the parent Notifier.send() method, which silently does nothing (pass).
# 2.3: send() is an abstract method because each delivery channel must implement its own transport logic, whereas notify() is a concrete method (Template Method pattern) because truncation and dispatch are shared by all subclasses.

from abc import ABC, abstractmethod
import pytest


class Notifier(ABC):
    max_length = 1000

    @abstractmethod
    def send(self, recipient: str, text: str) -> None:
        pass

    def notify(self, recipient: str, text: str) -> None:
        self.send(recipient, text[: self.max_length])


class TelegramNotifier(Notifier):
    max_length = 4096

    def send(self, recipient: str, text: str) -> None:
        self.last_sent = (recipient, text)
        print(f"telegram -> {recipient}: {text}")


class SmsNotifier(Notifier):
    max_length = 160

    def send(self, recipient: str, text: str) -> None:
        self.last_sent = (recipient, text)
        print(f"sms -> {recipient}: {text}")


# --- Tests ---
def test_cannot_instantiate_base_or_typo_subclass():
    with pytest.raises(TypeError):
        Notifier()

    class BrokenTelegramNotifier(Notifier):
        def sned(self, recipient, text):
            pass

    with pytest.raises(TypeError):
        BrokenTelegramNotifier()


def test_notify_truncates_to_channel_max_length():
    sms = SmsNotifier()
    tg = TelegramNotifier()
    long_text = "x" * 5000

    sms.notify("+998901234567", long_text)
    assert len(sms.last_sent[1]) == 160

    tg.notify("@ali", long_text)
    assert len(tg.last_sent[1]) == 4096

