from django.db import models

from apps.accounts import models as account_models


class Message(models.Model):
    """
    Message sent by users
    """

    sender = models.ForeignKey(account_models.User, on_delete=models.CASCADE, related_name='sender')
    content = models.CharField(max_length=1000)
    receiver = models.ForeignKey(account_models.User, on_delete=models.CASCADE, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
