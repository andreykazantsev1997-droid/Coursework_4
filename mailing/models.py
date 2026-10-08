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

    STATUS_CHOICES = [
        ('created', 'создана'),
        ('sent', 'отправлена'),
        ('completed', 'завершена'),
        ('canceled', 'отменена')
    ]

    SENDING = [
        ('once a day', 'раз в день'),
        ('once a week', 'раз в неделю'),
        ('once a month', 'раз в месяц'),
    ]

    sending_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата отправки")
    status = models.CharField(max_length=50, default='created', choices=STATUS_CHOICES, verbose_name="Состояние рассылки")
    periodicity = models.CharField(max_length=20, default='once a day', choices=SENDING, verbose_name="Периодичность")
    client = models.ManyToManyField(Client, verbose_name="Получатель")
    message = models.ForeignKey(Message, on_delete=models.PROTECT, verbose_name="Сообщение")

class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    date = models.DateTimeField(blank=True, null=True, verbose_name="Дата последней попытки")
    status = models.BooleanField(default=False)
    answer = models.TextField(blank=True, null=True, verbose_name="Ответ почтового сервера")
