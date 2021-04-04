import smtplib
from email.message import EmailMessage


class Text():
    def __init__(self):
        self.msg = EmailMessage()

    def send_msg(self,  to, body):
        self.msg.set_content(body)
        self.msg['subject'] = "AN IMPORTANT MESSAGE"
        self.msg['to'] = to
        self.msg['from'] = "DCSolutions"

        user = 'dmobley1898@gmail.com'
        password = 'bdbmoqdgdfzntenf'

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=120)
        server.starttls()
        server.login(user, password)
        server.send_message(self.msg)
        server.quit()
