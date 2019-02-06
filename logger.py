import os.path
import datetime


def create_log_file(file):
    # Creates log files when called by log_file
    try:
        open(file, "w")
    except Exception as e:
        log_file(
            "{} | failed to create file. Please contact administrator and advise the following error description: {}.".format(
                datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S"), e
            )
        )
        return


def log_file(message, file):
    """
    Sends message to log files.
    :param message: Text message to log
    :param file: log file defined by type of log (error, syslog, etc)
    :return: log line appended to appropriate log file
    """

    time_stamp = datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")
    if os.path.isfile(file):
        with open(file, "a", newline="") as line:
            line.writelines("{} | {} \n".format(time_stamp, message))
    else:
        create_log_file(file)
        with open(file, "a", newline="") as line:
            line.writelines(
                "{} | {} created \n".format(time_stamp, file)
            )
