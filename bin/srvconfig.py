import configparser
import os
import sys
from datetime import datetime

from logger import ExceptlogClient


class DMARCSC:
    # Initialize the Class variables
    config = None
    _config_file_path = os.path.join(sys.path[0], "config", "config.ini")
    start_datetime = ""
    ews_username = ""
    ews_password = ""
    ews_email = ""
    ews_service_endpoint = ""
    ews_disable_https_cert_verify = False
    syslog_server = ""
    syslog_port = ""
    syslog_application = ""
    srv_max_worker = ""
    mailbox_type = ""
    _mailbox_type_ews = "ews"
    error_log_path = os.path.join(sys.path[0], "log", "error.log")
    error_log_enable = True
    debug_log_enable = False

    @staticmethod
    def init_config():
        try:
            # Initialize the configuration parser
            DMARCSC.config = configparser.RawConfigParser()
            DMARCSC.config.read(DMARCSC._config_file_path)

            # Read configuration values from the config file
            DMARCSC.start_datetime = DMARCSC.config["CONFIG"]["start_datetime"]
            DMARCSC.srv_max_worker = int(
                DMARCSC.config["CONFIG"]["srv_max_worker"]
            )
            DMARCSC.syslog_server = DMARCSC.config["SYSLOG"]["syslog_server"]
            DMARCSC.syslog_port = int(DMARCSC.config["SYSLOG"]["syslog_port"])
            DMARCSC.mailbox_type = DMARCSC.config["CONFIG"]["mailbox_type"]

            # Check if the mailbox type is Exchange Web Service (EWS)
            if DMARCSC.mailbox_type == DMARCSC._mailbox_type_ews:
                DMARCSC.ews_username = DMARCSC.config["EWS"]["ews_username"]
                DMARCSC.ews_password = DMARCSC.config["EWS"]["ews_password"]
                DMARCSC.ews_email = DMARCSC.config["EWS"]["ews_email"]
                DMARCSC.ews_service_endpoint = DMARCSC.config["EWS"][
                    "ews_service_endpoint"
                ]

                # Check if the option to disable HTTPS certificate verification
                # is present
                if DMARCSC.config.has_option(
                    "EWS", "ews_disable_https_cert_verify"
                ):
                    DMARCSC.ews_disable_https_cert_verify = eval(
                        DMARCSC.config["EWS"]["ews_disable_https_cert_verify"]
                    )

            # Read the error log and debug log enable flags from the
            # config file
            DMARCSC.error_log_enable = eval(
                DMARCSC.config["CONFIG"]["error_log_enable"]
            )
            DMARCSC.debug_log_enable = eval(
                DMARCSC.config["CONFIG"]["debug_log_enable"]
            )

        except Exception as exception:
            # If an exception occurs, initialize the ExceptlogClient for error
            # logging and log the exception
            ExceptlogClient.initiate(
                DMARCSC.error_log_path,
                DMARCSC.error_log_enable,
                True,
            )
            ExceptlogClient.log_except(exception)

    @staticmethod
    def update_config_start_datetime():
        # Get the current datetime and format it as "%Y-%m-%d-%H:%M"
        now = datetime.now().strftime("%Y-%m-%d-%H:%M")

        # Update the start_datetime configuration value with the current
        # datetime
        DMARCSC.config.set("CONFIG", "start_datetime", now)

        # Write the updated config to the config file
        with open(DMARCSC._config_file_path, "w") as configfile:
            DMARCSC.config.write(configfile)
