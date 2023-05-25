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
        print(status)

    def close(self):
        status = self.smtpserver.close()
        return status
    
    def writeMessage(self, subject, dst):
        """
        Subject : The subject of the email
        src : the sender email
        dst : the receiver email
        """
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["to"] = dst
        return msg

    def sendMessage(self):
        subject = input("Subject  : ")
        destination = input("TO : ")
        msg = self.writeMessage(subject, destination)
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

    def set_debuglogger(self, logger):
        self.smtpserver.set_debuglogger(logger)

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