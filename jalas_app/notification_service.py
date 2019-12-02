from django.core.mail import EmailMessage


def notify_meeting_owner(user_email):
    email = EmailMessage('Meeting Is Hold',
                         "Hi User!\n A meeting is arranged. Check your profile for further information. Bye!")
    return email.send()
