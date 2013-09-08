from django.core.mail import send_mail
import threading
import traceback, sys

class EmailThread(threading.Thread):
    def __init__(self, subject, content, from_email, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.content = content
        self.from_email = from_email
        threading.Thread.__init__(self)

    def run (self):
        try:
            #for i in range(10):
            send_mail(self.subject,self.content,self.from_email,self.recipient_list)
        except:
            traceback.print_exc(file=sys.stdout)

