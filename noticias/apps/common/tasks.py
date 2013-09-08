from celery.task import task
from django.core.mail import send_mail

@task
def celery_send_email(subject, content, from_email, to_email):
    send_mail(subject,content,from_email, to_email, auth_user="naoresponda@clickpb.com.br",auth_password="s0d4!SODA@")
    return True

