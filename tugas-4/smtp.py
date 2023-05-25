import smtplib
from email.message import EmailMessage
import logging
import getpass

class SMTP:
    def __init__(self):
        self.email = ""
        self.password = ""
        self.smtpsrv = "smtp.office365.com"
        self.port = 587
        self.smtpserver = smtplib.SMTP(self.smtpsrv,self.port)

    def login(self):
        self.email = input("Email    : ")
        self.password = getpass.getpass("Password : ")
        status = self.smtpserver.login(self.email, self.password)

    def close(self):
        status = self.smtpserver.close()
        print(status)
        return status
    
    def writeMessage(self, subject, content, dst):
        """
        Subject : The subject of the email
        dst : the receiver email
        content : The content of the email
        """
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["to"] = dst
        msg.set_content(content)
        return msg

    def sendMessage(self):
        destination = input("TO : ")
        subject = input("Subject  : ")
        content = input("Content  : ")
        msg = self.writeMessage(subject, content, destination)
        try:
            status = self.smtpserver.send_message(msg)
            print("Message sent successfully!")
        except smtplib.SMTPException as e:
            print("An error occurred while sending the message:", str(e))
        return status
    
    def ehlo(self):
        status = self.smtpserver.ehlo()
        return status
    
    def starttls(self):
        status = self.smtpserver.starttls()
        return status
    
    def set_debuglevel(self, level):
        self.smtpserver.set_debuglevel(level)


def main():
    smtp = SMTP()
    
    # Configure logging
    logging.basicConfig(filename="smtp_debug.log", level=logging.DEBUG)
    logger = logging.getLogger("SMTPDebug")
    smtp.smtpserver.set_debuglevel(1)
    smtp.smtpserver._logger = logger
    smtp.smtpserver.debugging = True

    smtp.ehlo()
    smtp.starttls()
    smtp.login()
    smtp.sendMessage()
    smtp.close()


if __name__ == "__main__":
    main()