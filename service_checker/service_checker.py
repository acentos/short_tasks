#!/usr/bin/env python3

import subprocess
import smtplib
import threading
import time
import logging
from email.message import EmailMessage

from settings import (
    cmd_list,
    mail_from,
    mail_to,
    logfile_name,
    logfile_path,
    period_min
)

logging.basicConfig(
    filename="{}/{}".format(logfile_path, logfile_name),
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s")


class ServiceChecker():
    """
        Check service status.

        Checking every <PERIOD> minutes service status declaring in settings.py list.
        If service not started, then script trying automaticaly restarting it
        and sending message on email.
    """

    def __init__(self):
        self.cmd_list = cmd_list
        self.mail_from = mail_from
        self.mail_to = mail_to

    def status_messager(self, output, action):
        msg = EmailMessage()
        msg.set_content(output)
        msg['Subject'] = "Service \"{}\" have problem".format(action)
        msg['From'] = self.mail_from
        msg['To'] = self.mail_to
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

    def restart_service(self, action):
        subprocess.run("sudo systemctl restart {}".format(action), shell=True)

    def cmd_check_status(self, action):
        cmd_action="systemctl status {}".format(action)
        cmd_status = subprocess.Popen(cmd_action,
                                      shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        output, error = cmd_status.communicate()
        if cmd_status.returncode != 0:
            err_cmd_status = "FAILED"
            logging.debug(
                "Service status for {}: {}".format(
                    action, err_cmd_status))
            self.status_messager(output.decode('utf-8'), action)
            self.restart_service(action)
            time.sleep(30)

    def run_status_check(self):
        for cmd in self.cmd_list:
            self.cmd_check_status(cmd)

def periodicaly_check():
    threading.Timer(60.0*int(period_min), periodicaly_check).start()
    sc=ServiceChecker()
    sc.run_status_check()

periodicaly_check()
