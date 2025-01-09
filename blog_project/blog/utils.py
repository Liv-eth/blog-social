from .models import Notification

def create_notification(recipient, sender, notification_type, post=None, comment=None):
    text = ''
    if notification_type == 'comment':
        text = f'{sender.username} commented on your post "{post.title}"'
    elif notification_type == 'post':
        text = f'{sender.username} published a new post: "{post.title}"'
    elif notification_type == 'like':
        text = f'{sender.username} liked your post "{post.title}"'

    Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        post=post,
        comment=comment,
        text=text
    )