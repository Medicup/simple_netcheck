import requests
import requests.exceptions
import time
import datetime
import os
import socket

import send_mail

url = 'http://google.com'
file_name = '{}_{}.txt'.format(socket.gethostname(), datetime.datetime.now().strftime('%y%m%d'))


def main():
    time_to_check = input('How long would you like to run the network check <enter in minutes> ? ')
    try:
        int(time_to_check)
    except:
        time_to_check = 1440
    network_state(int(time_to_check))


def create_log_file(file):
    try:
        open(file, 'w')
    except Exception as e:
        print('failed to create file. Please contact administrator and advise the following error description: '
              '{}.'.format(e))
        return


def log_file(message, file):

    if os.path.isfile(file):
        with open(file, 'a', newline="") as line:
            line.writelines('{}\n'.format(message))
    else:
        create_log_file(file)


def network_state(duration=1):
    count = duration * 20

    while count > 0:
        time_stamp = datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')

        try:
            url_check = requests.get(url, timeout=5)
            url_speed = url_check.elapsed.total_seconds()
            if url_check.status_code == 200:
                message = "{} | {} | Successful_ping_of | {} | {}.".format(count, time_stamp, url, url_speed)
                log_file(message, file_name)

        except Exception as e:
            message = "{} | {} | GENERAL_EXCEPTION_of | {} | NA | {}.".format(count, time_stamp, url, e)
            log_file(message, file_name)

        count -= 1
        print('runs left = {}'.format(count))
        time.sleep(4)

    send_mail.mailer(file_name)


if __name__ == '__main__':
    main()