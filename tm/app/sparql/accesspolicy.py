from abc import ABC, abstractmethod


class AccessPolicy(ABC):
    @abstractmethod
    def __init__(self):
        self.count = None
        self.policies = None

    @property
    @abstractmethod
    def count(self) -> int:
        pass

    @property
    @abstractmethod
    def policies(self) -> list[str]:
        pass
