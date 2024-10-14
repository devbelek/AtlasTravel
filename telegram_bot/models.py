from django.db import models


class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat ID: {self.chat_id} (Admin: {self.is_admin})"

    class Meta:
        verbose_name = 'Telegram User'
        verbose_name_plural = 'Telegram Users'
