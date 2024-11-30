from django.db import models

class ChatMessage(models.Model):
    query = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения чата'

    def __str__(self):
        return f"Запрос {self.id}: {self.query[:50]}"
