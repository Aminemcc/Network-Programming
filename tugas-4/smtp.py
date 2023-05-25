import smtplib
from email.message import EmailMessage
import logging
import getpass
import sys

class SMTP:
    def __init__(self):
        self.email = ""
        self.password = ""
        self.smtpsrv = "smtp.office365.com"
        self.port = 587
        self.smtpserver = smtplib.SMTP(self.smtpsrv,self.port)
        self.logfile = open("./smtp_debug.log", "w")
        self.original_std = (sys.stdout, sys.stderr)
        self.switch_sys() #print to logfile

    def switch_sys(self):
        if sys.stdout == self.logfile:
            sys.stdout, sys.stderr = self.original_std
        else:
            sys.stdout = sys.stderr = self.logfile

    def login(self):
        self.switch_sys()
        self.email = input("Email    : ")
        self.password = getpass.getpass("Password : ")
        print("Logging in")
        self.switch_sys()
        try:
            status = self.smtpserver.login(self.email, self.password)
        except smtplib.SMTPAuthenticationError as e:
            self.switch_sys()
            print("Caught Error : SMTP Authentication Error")
            exit(1)
        print(status)

    def close(self):
        status = self.smtpserver.close()
        return status
    
    def writeMessage(self, subject, content, dst):
        """
        Subject : The subject of the email
        src : the sender email
        dst : the receiver email
        """
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["to"] = dst
        msg.set_content(content)
        return msg

    def sendMessage(self):
        self.switch_sys()
        subject = input("Subject  : ")
        content = input("Content  : ")
        destination = input("TO       : ")
        self.switch_sys()

        msg = self.writeMessage(subject, content, destination)
        try:
            status = self.smtpserver.send_message(msg)
            print("Message sent successfully!")
        except smtplib.SMTPException as e:
            self.switch_sys()
            print("Caught Error : SMTP Exception, An error occurred while sending the message:", str(e))
            exit(1)
        return status
    
    def ehlo(self):
        status = self.smtpserver.ehlo()
        return status
    
    def starttls(self):
        status = self.smtpserver.starttls()
        return status
    
    def set_debuglevel(self, level):
        self.smtpserver.set_debuglevel(level)
        if level > 0:
            self.smtpserver.debugging = True
        else:
            self.smtpserver.debugging = False

def main():
    smtp = SMTP()
    smtp.smtpserver.set_debuglevel(1)

    smtp.ehlo()
    smtp.starttls()
    smtp.login()
    smtp.sendMessage()
    smtp.close()


if __name__ == "__main__":
    main()