from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post, Comment
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Comment)
def notify_post_author(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        subject = f'New comment on your post "{post.title}"'
        message = f'{instance.author.username} commented: "{instance.content}"'
        if settings.DEBUG:
            print(f"Notification: {subject}\n{message}")
    
         # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [post.author.email])