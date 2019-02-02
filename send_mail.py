import mimetypes
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import static_references
import credentials_email
from email import encoders
import logger
import glob


def mailer(email=static_references.default_email):
    from_email = credentials_email.email
    from_password = credentials_email.password
    zip_list = glob.glob("*.zip")
    subject = "Network log files report"

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = email

    for attachment in zip_list:
        ctype, encoding = mimetypes.guess_type(attachment)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        try:
            with open(attachment, "rb") as f:
                part = MIMEBase(maintype, subtype)
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=os.path.basename(attachment),
                )
                msg.attach(part)
        except IOError as e:
            logger.log_file("{} | {}".format(static_references.error_log, e))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)

    try:
        gmail.send_message(msg)
        logger.log_file("Files mailed.", static_references.system_log)
        gmail.quit()

    except smtplib.SMTPAuthenticationError:
        logger.log_file("error: SMTPAuthenticationError", static_references.error_log)

    except smtplib.SMTPServerDisconnected:
        logger.log_file(
            "error: The server unexpectedly disconnects.", static_references.error_log
        )

    except smtplib.SMTPSenderRefused:
        logger.log_file("error: Semder address refused.", static_references.error_log)

    except smtplib.SMTPRecipientsRefused:
        logger.log_file(
            "error: All recipient addresses refused.", static_references.error_log
        )

    except smtplib.SMTPDataError:
        logger.log_file(
            "error: The SMTP server refused to accept the message data.",
            static_references.error_log,
        )

    except smtplib.SMTPConnectError:
        logger.log_file(
            "{} | error: Error occurred during establishment of a connection with the server.",
            static_references.error_log,
        )

    except smtplib.SMTPHeloError:
        logger.log_file(
            '{} | error: The server refused our "HELO" message.',
            static_references.error_log,
        )

    except smtplib.SMTPException as e:
        logger.log_file("{}".format(e), static_references.error_log)

    except Exception as e:
        logger.log_file("{}".format(e), static_references.error_log)
