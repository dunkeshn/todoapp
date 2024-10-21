from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from django.db import models


class Tasks(models.Model):
    title = models.CharField(max_length=150,
                             verbose_name='Название')
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    priority = models.CharField(max_length=50,
                                choices=[('COMMON', 'Обычный'), ('LOW', 'Низкий'), ('MEDIUM', 'Средний'),
                                         ('HIGH', 'Высокий')],
                                verbose_name='Приоритет',
                                default='COMMON')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    completed = models.BooleanField(default=False,
                                    verbose_name='Выполнено')
    owners = models.ManyToManyField('Users',
                                    related_name='tasks',
                                    verbose_name='Пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['created_at']


class Users(AbstractUser):
    first_name = models.CharField(max_length=100,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=100,
                                 blank=True,
                                 verbose_name='Фамилия')
    username = models.CharField(max_length=100,
                                unique=True,
                                verbose_name='Никнейм')
    email = models.CharField(max_length=100,
                             unique=True,
                             verbose_name='Почта')
    about = models.TextField(blank=True,
                             verbose_name='О себе')
    date_of_birth = models.DateField(null=True,
                                     blank=True,
                                     verbose_name='Дата рождения')
    picture = models.ImageField(upload_to='pictures',
                                null=True,
                                blank=True,
                                default='pictures/default.jpg',
                                verbose_name='Фото')
    friends = models.ManyToManyField('self',
                                     blank=True,
                                     verbose_name='Друзья',
                                     symmetrical=False)
    password = models.CharField(max_length=100,
                                verbose_name='Пароль')

    def __str__(self):
        return f'{self.first_name} ({self.username})'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']


class FriendshipInvite(models.Model):
    sent_from = models.ForeignKey(Users, related_name='invites_sent', on_delete=models.CASCADE)
    sent_to = models.ForeignKey(Users, related_name='invites_received', on_delete=models.CASCADE)

    def __str__(self):
        return f'Приглашение в друзья от {self.sent_from} к {self.sent_to}'

    class Meta:
        verbose_name = 'Приглашение в друзья'
        verbose_name_plural = 'Приглашения в друзья'
        ordering = ['sent_from']
