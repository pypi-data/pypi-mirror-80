from .base import BaseImopayWrapper, CreateMixin, DestroyMixin
from ..models.webhook import Webhook


class WebhookWrapper(BaseImopayWrapper, CreateMixin, DestroyMixin):
    """
    Wrapper para os métodos de webhooks
    """

    @property
    def action(self):
        return "webhooks"

    @property
    def model(self):
        return Webhook
