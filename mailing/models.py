from django.utils import timezone
from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name="ФИО")
    email = models.EmailField(unique=True)
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return self.name

class Message(models.Model):
    topic = models.CharField(max_length=150, verbose_name="Тема сообщения")
    text = models.TextField(verbose_name="Текст сообщения")

    def __str__(self):
        return self.topic

class Mailing(models.Model):

    SENDING = [
        ('once a day', 'раз в день'),
        ('once a week', 'раз в неделю'),
        ('once a month', 'раз в месяц'),
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время начала")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания")
    periodicity = models.CharField(max_length=20, default='once a day', choices=SENDING, verbose_name="Периодичность")
    recipients  = models.ManyToManyField(Client, verbose_name="Получатель")
    message = models.ForeignKey(Message, on_delete=models.PROTECT, verbose_name="Сообщение")

    @property
    def status(self):
        now = timezone.now()
        if now < self.start_time:
            return 'Создана'
        elif self.start_time <= now <= self.end_time:
            return 'Запущена'
        else:
            return 'Завершена'

    def __str__(self):
        return f"Рассылка {self.id} ({self.status})"

class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время последней попытки")
    status = models.BooleanField(default=False)
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ почтового сервера")

