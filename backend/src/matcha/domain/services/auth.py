from abc import ABC, abstractmethod


class AbstractAuthService(ABC):
    @abstractmethod
    def generate_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def generate_tokens(self, account_id: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def can_refresh_token(self, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        raise NotImplementedError
