class InvalidScheme(Exception):
    """URL has a invalid or unknown scheme."""
    def __init__(self, message: str) -> None:
        super().__init__(message)

class InvalidContentEncoding(Exception):
    """The 'Content-Encoding' header has an invalid/unknown value."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
