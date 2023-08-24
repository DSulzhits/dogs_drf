from celery import shared_task
import datetime
from dogs.models import Dog


@shared_task
def send_message_about_like(chat_id):
    print(f"Сообщение в телеграмм отправлено в чат {chat_id}")


def send_birthday_mail():
    dog_list = Dog.objects.filter(date_born=datetime.date.today())
    for dog in dog_list:
        print(f"Send mail to {dog.owner.username}")
