from uuid import uuid4
from djongo import models

from django.core.validators import MinLengthValidator


def _generate_unique_room():
    return str(uuid4()).replace('-', '')[:16]


class Room(models.Model):
    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    uri = models.URLField(default=_generate_unique_room)
    added = models.DateTimeField(verbose_name='Дата создания комнаты', auto_now_add=True)


class Message(models.Model):
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-timestamp']

    author_id = models.PositiveIntegerField(verbose_name='ID автора сообщения', unique=True)
    room = models.ForeignKey(Room, verbose_name='Комната', related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Содержание сообщения')
    timestamp = models.DateTimeField(verbose_name='Дата отправки сообщения', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления сообщения', auto_now=True)

    def __str__(self):
        return f"ID: {self.id} - AuthorID: {self.author_id}"

    def to_json(self):
        return {'user': self.author_id, 'message': self.content}


class RoomMember(models.Model):
    room = models.ForeignKey(Room, related_name='members', on_delete=models.CASCADE)
    user_id = models.PositiveIntegerField(verbose_name='ID пользователя')
    username = models.CharField(verbose_name='Имя пользователя', validators=[MinLengthValidator(3)], max_length=25)
