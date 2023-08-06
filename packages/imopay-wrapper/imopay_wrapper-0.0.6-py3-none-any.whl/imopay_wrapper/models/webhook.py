from dataclasses import dataclass

from .base import BaseImopayObj


@dataclass
class Webhook(BaseImopayObj):
    event: str
    url: str
    description: str
