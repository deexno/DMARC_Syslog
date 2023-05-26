# DMARC Syslog
Python script to read DMARC reports from a mailbox, parse them, format them as syslog messages, and send them to syslog server. 

Useful to send DMARC report to SIEM to build use cases.

-------------------------------------------------------------------------------------------------------------------------------------------------
Supported mailbox access:
  1. EWS (Exchange Web Service)

-------------------------------------------------------------------------------------------------------------------------------------------------
Supported Report Formats:
  1. \*.zip
  2. \*.gz

-------------------------------------------------------------------------------------------------------------------------------------------------
Requirements:
  1. Python 3.10
  2. exchangelib 4.6.2 : installation command -> pip install exchangelib 


-------------------------------------------------------------------------------------------------------------------------------------------------
How to use it:
  1. Provide the required configuration in the configuration file "config.ini" 
  2. create a task scheduler or cron job to run the script file "start.py", as an example each 10 minutes.
  3. The script manages the last time it checked for reports and it starts from last time check.

-------------------------------------------------------------------------------------------------------------------------------------------------
Configuration File:
Section | Config Tag | Value | Description
---| --- | --- | ---
CONFIG | start_datetime | YYYY-MM-DD-HH:MM | date/time to process the emails starting from it.
CONFIG | srv_max_worker | Number | number of threads to process the reports
CONFIG | mailbox_type | [ews] | connection type to mailbox 
CONFIG | error_log_enable | [True,False] | log errors to the log file .\log\error.log
CONFIG | debug_log_enable | [True,False] | log debug to the log file .\log\error.log
SYSLOG | syslog_server | IP | syslog server IP
SYSLOG | syslog_port | Port Number | Syslog server port number
EWS | ews_username | domain\userName | username to connect to mailbox through EWS
EWS | ews_password | userPass | password to connect to mailbox through EWS
EWS | ews_email | email@domain.com | mailbox email
EWS | ews_service_endpoint | https://mail.domian.com/ews/exchange.asmx | ews service endpoint URL
EWS | ews_disable_https_cert_verify | [True,False] | disable certification verification
