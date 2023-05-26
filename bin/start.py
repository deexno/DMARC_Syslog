import concurrent.futures
import sys

from dmarc import DMARCExtractor
from ews import ExchangeWebSrv
from logger import ExceptlogClient, SyslogClient
from srvconfig import DMARCSC
from utility import Utility


def main():
    init_main()

    if DMARCSC.mailbox_type == DMARCSC._mailbox_type_ews:
        attachments_gz = init_ews()

    if attachments_gz is not None:
        init_thread(DMARCSC.srv_max_worker, attachments_gz)

    DMARCSC.update_config_start_datetime()


def init_main():
    # Initialize DMARCSC configuration
    DMARCSC.init_config()

    # Initialize ExceptlogClient for error and debug logging
    ExceptlogClient.initiate(
        DMARCSC.error_log_path,
        DMARCSC.error_log_enable,
        DMARCSC.debug_log_enable,
    )

    try:
        # Initialize SyslogClient for logging to syslog server
        SyslogClient.initiate(DMARCSC.syslog_server, DMARCSC.syslog_port)
    except Exception as exception:
        ExceptlogClient.log_except(exception)


def init_ews():
    try:
        # Create an instance of ExchangeWebSrv using the provided configuration
        exchangeWebSrv = ExchangeWebSrv(
            DMARCSC.ews_username,
            DMARCSC.ews_password,
            DMARCSC.ews_email,
            DMARCSC.ews_service_endpoint,
        )

        if DMARCSC.ews_disable_https_cert_verify:
            exchangeWebSrv.disable_https_cert_verify()

        # Connect to the Exchange Web Service
        exchangeWebSrv.connect()

        # Retrieve DMARC report attachments (compressed gzip files) from the
        # Exchange server
        attachments_gz = exchangeWebSrv.get_dmarc_report_gz(
            DMARCSC.start_datetime
        )
        return attachments_gz
    except Exception as exception:
        ExceptlogClient.log_except(exception)
        input()


def init_thread(srv_max_worker, attachments_gz):
    try:
        # Initialize a ThreadPoolExecutor with the specified maximum number of
        # workers
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=srv_max_worker
        ) as executor:
            for attachment_gz in attachments_gz:
                # Submit each attachment to the executor for processing in a
                # separate thread
                executor.submit(exec_thread, attachment_gz)
    except Exception as exception:
        ExceptlogClient.log_except(exception)


def exec_thread(attachment_gz):
    try:
        # Try to decompress the archives
        if "gzip" in attachment_gz.content_type:
            result = Utility.decompress_gz_to_byte(attachment_gz.content)
        else:
            result = Utility.decompress_zip_to_byte(attachment_gz.content)

        if result is None:
            sys.exit()

        # Convert the decompressed byte content to XML
        result = Utility.byte_to_xml(result)

        dmar_extractor = DMARCExtractor()

        # Send the collected Data to the Syslog Server
        SyslogClient.log_info_msg(dmar_extractor.extract_variables(result))
    except Exception as exception:
        ExceptlogClient.log_except(exception)


if __name__ == "__main__":
    main()
