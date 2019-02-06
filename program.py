import requests
import requests.exceptions
import time
import datetime
import socket
import logger
import static_references

import zip_file

url = "http://google.com"
file_name = "{}_{}.txt".format(
    socket.gethostname(), datetime.datetime.now().strftime("%y%m%d")
)


def main():
    while True:
        try:
            requests.get(url, timeout=5)
            print("Network connection established, preparing to zip files")
            logger.log_file(
                "Network connection established, preparing to zip files",
                static_references.system_log,
            )
            zip_file.zip_files()
            network_state(480)
            zip_file.zip_files()
            return False
        except IOError as e:
            wait_time = 10
            print(
                "Unable to establish network connection. Logging error and waiting {} minutes to retry...".format(
                    wait_time
                )
            )
            logger.log_file(
                "Unable to establish network connection: {}".format(e),
                static_references.error_log,
            )
            counter = wait_time * 60
            while counter > 0:
                print("Waiting {} seconds... ".format(counter))
                counter -= 30
                time.sleep(30)


def network_state(duration=1):
    count = duration * 6

    while count > 0:
        try:
            url_check = requests.get(url, timeout=5)
            url_speed = url_check.elapsed.total_seconds()
            if url_check.status_code == 200:
                message = "Attempts left = {} | Successful_ping_of | {} | {}.".format(
                    count, url, url_speed
                )
                logger.log_file(message, file_name)

        except Exception as e:
            message = "Attempts left = {} | GENERAL_EXCEPTION_of | {} | NA | {}.".format(
                count, url, e
            )
            logger.log_file(message, file_name)

        count -= 1
        print("runs left = {}".format(count))
        time.sleep(10)


if __name__ == "__main__":
    main()
