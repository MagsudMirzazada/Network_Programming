# TAKEN

import smtplib
import ssl
import getpass

sender_email = "traptheonly@gmail.com"
password = "magicfootball7"  # getpass.getpass("Enter a password: ")


# Create a secure SSL context
context = ssl.create_default_context()
server = 0
# Try to log in to server and send email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls(context=context)  # Secure the connection
    server.login(sender_email, password)
    receiver_email = "ismail.eyyub@gmail.com"
    message = """\
        Subject: Bla-Bla

        bla-bla-bla"""
    # receiver_email = "gulustankarimova@gmail.com"
    # message = """\
    # Subject: Meu Sol

    # I loooveee youuu moooreeee thannn infiniteeelyy myyy eveeerythiinnggg"""
    server.sendmail(sender_email, receiver_email, message)
except Exception as e:
    print(e)
finally:
    server.quit()
