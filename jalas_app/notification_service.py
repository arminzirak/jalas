from django.core.mail import EmailMessage


def notify_Poll_owner(user_email):
    email = EmailMessage('Poll Is Hold',
                         "Hi User!\n A Poll is arranged. Check your profile for further information. Bye!", to=[user_email])
    return email.send()
