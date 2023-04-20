from abc import ABC, abstractmethod


class AccessPolicy(ABC):
    '''
    Abstract class for access policies for reusability.
    DUAPolicy inherits this class.
    '''
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
