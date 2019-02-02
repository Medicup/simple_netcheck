import datetime
import zipfile
import glob
import send_mail
import logger
import static_references
import os


def zip_files():
    name = "networkLogArchive_{}.zip".format(datetime.datetime.now().strftime("%y%m%d"))
    zip_list = glob.glob("*.txt")
    logger.log_file(
        "The files to zip are: {}".format(zip_list), static_references.system_log
    )
    try:
        with zipfile.ZipFile(name, "w") as zip_file:
            for afile in zip_list:
                zip_file.write(afile)
        logger.log_file(
            "Files zipped and sending to mailer", static_references.system_log
        )
        try:
            send_mail.mailer()
            purge = glob.glob("*.txt")
            for afile in purge:
                os.remove(afile)
        except Exception as e:
            logger.log_file(
                "Unable to send zipped files: {}".format(e), static_references.error_log
            )
    except zipfile.BadZipFile as e:
        logger.log_file(
            "{} | BadZipFile exception raised as {}".format(static_references, e),
            static_references.error_log,
        )
    except zipfile.LargeZipFile as e:
        logger.log_file(
            "{} | LargeZipFile exception raised as {}".format(
                static_references.error_log, e
            ),
            static_references.error_log,
        )
    except Exception as e:
        logger.log_file(
            "Unknown ZipFile error as {}".format(e), static_references.error_log
        )
