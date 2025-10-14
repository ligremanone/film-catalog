class FilmError(Exception):
    """
    Base exception class for film related errors
    """


class FilmAlreadyExistsError(FilmError):
    """
    Raised when a film with the same slug already exists
    """
