import secrets
from abc import ABC, abstractmethod


class AbstractTokenHelper(ABC):
    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        pass

    @abstractmethod
    def add_token(
        self,
        token: str,
    ) -> None:
        pass

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(16)

    def generate_and_save_token(
        self,
        token: str,
    ) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token
