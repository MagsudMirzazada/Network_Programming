# SCRATCH-UP
# CREATES SECURE CONNECTION AND SENDS MAIL TO ONE OR MANY USERS VIA GMAIL

import smtplib
import ssl
import csv
import getpass

SMTP_SERVER = "smtp.gmail.com"
PORT = 587
sender_email = "magsud.16@gmail.com"
password = getpass.getpass()
receiver_email = "nonessential001@gmail.com"

messageForSingle = '''\
Subject: Hi there

This message is sent from python.'''

messageForMulti = '''\
Subject: Your Grade

Hi {name}, your grade is {grade}'''

def singlemail():
    # create secure SSL and connection
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, messageForSingle)
    except Exception as e:
        print(e)
    finally:
        server.quit()

def multimail():
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        with open("emails_ex.csv") as file:
            reader = csv.reader(file)
            next(reader) #Skip header row
            for name, email, grade in reader:
                server.sendmail(sender_email, email, messageForMulti.format(name=name, grade=grade))
    except Exception as e:
        print(e)
    finally:
        server.quit()


def main():
    #singlemail()
    multimail()

if __name__ == '__main__':
    main()