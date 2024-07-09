import os
import datetime


def log_response(response):
    with open(os.path.join(os.getcwd(), "log.txt"), 'a') as file:
        file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        file.write("\n")
        file.write(str(response))
        file.write("\n")
