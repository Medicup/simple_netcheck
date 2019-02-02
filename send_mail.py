import datetime
import mimetypes
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os
import static_references
import credentials_email

body = 'Initiating email log: \n'


def send_mail():
    pass


def message_body_update(message):
    message_body = ('log entry at {}: {} \n'.format(static_references.time_stamp, message))
    body.append(message_body)


def create_error_log(message):
    log_line = "{}, {} \n".format(static_references.time_stamp, message)
    file_name = "error_log.txt"

    if os.path.isfile(file_name) is True:
        with open(file_name, "a", newline="") as log_file:
            log_file.writelines(log_line)
    else:
        try:
            open(file_name, 'w')
        except FileExistsError:
            pass  # directory already exists


def mailer(file, email=static_references.default_email):
    from_email = credentials_email.email
    from_password = credentials_email.password

    subject = "Network log files report"
    msg_body = '{} Starting to send mail. \n'.format(body)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = email

    msg.attach(MIMEText(msg_body))

    with open(file, 'r') as temp_file:
        part = MIMEApplication(
            temp_file.read()
        )
    part['Content-Disposition'] = 'attachment; filename={}'.format(file)
    msg.attach(part)
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)

    try:
        gmail.send_message(msg)
        gmail.quit()

    except smtplib.SMTPAuthenticationError:
        create_error_log('error: SMTPAuthenticationError')

    except smtplib.SMTPServerDisconnected:
        create_error_log('error: The server unexpectedly disconnects.')

    except smtplib.SMTPSenderRefused:
        create_error_log('error: Semder address refused.')

    except smtplib.SMTPRecipientsRefused:
        create_error_log('error: All recipient addresses refused.')

    except smtplib.SMTPDataError:
        create_error_log('error: The SMTP server refused to accept the message data.')

    except smtplib.SMTPConnectError:
        create_error_log('error: Error occurred during establishment of a connection with the server.')

    except smtplib.SMTPHeloError:
        create_error_log('error: The server refused our "HELO" message.')

    except smtplib.SMTPException as e:
        create_error_log('{}'.format(e))

    except Exception as e:
        create_error_log('{}'.format(e))

        pass




