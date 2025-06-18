from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        pass

    @classmethod
    def check_password_match(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.check_password_match(db_password, password)
