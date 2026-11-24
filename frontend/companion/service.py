"""Service interface for the Talking Tomatoes frontend."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class CompanionReply:
    """Response returned by a companion service."""

    text: str
    messages: list[dict]
    media_results: list[dict] = field(default_factory=list)


class CompanionError(Exception):
    """Safe, user-facing error raised by the companion service."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class CompanionService(ABC):
    """Contract that all frontend companion services must implement."""

    @abstractmethod
    def get_username(self) -> str:
        pass

    @abstractmethod
    def new_conversation(self) -> list[dict]:
        pass

    @abstractmethod
    def send_message(self, messages: list[dict]) -> CompanionReply:
        pass