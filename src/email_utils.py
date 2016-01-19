import smtplib
import random
import string


def send_recovery_email(user):
    recovery_code = "".join(random.choice(string.ascii_uppercase + string.ascii_uppercase) for _ in range(10))
    message = \
        """ From: NoReply <noreply@artizanz.com>
        To: {0} <{1}>
        MIME-Version: 1.0
        Content-Type: text/html
        Subject: Artizanz Password Recovery

        Your recovery code is {2}
        """.format(user.username, user.email, recovery_code)
    try:
        smtp_obj = smtplib.SMTP("localhost")
        smtp_obj.sendmail("noreply@artizanz.com", [user.email], message)
        return True
    except smtplib.SMTPException:
        return False

