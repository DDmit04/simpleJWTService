from dataclasses import dataclass


@dataclass
class TokenAuthData:
    access: str
    refresh: str
