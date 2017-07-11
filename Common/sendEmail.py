# coding=UTF-8
# __author__ = 'zhengandy'

import time
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from Config import config
import chardet


def send_email(file_to_send=None, text=None, mail_to=None, mail_cc=None):
    """
    This function takes in recipient and will send the email to that email address with an attachment.
    :param file_to_send: the file will be send to mail_to.
    :param mail_to: the email of the person to get the text file attachment.
    :param text in the file text will be seen in email content.
    """

    time_str = time.strftime("%Y-%m-%d %X", time.localtime())
    # Set the server and the message details
    send_from = '%s' % config.email_sender
    subject = "TestReport FOR Automation %s." % time_str
    # Create the multi-part
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = ",".join(mail_to)  # recipient
    msg['Cc'] = ",".join(mail_cc)

    # msg preamble for those that do not have a email reader
    msg.preamble = 'MultiPart message.\n'

    # Text part of the message
    fd = open(text, 'r')
    values = ""
    value = fd.readlines()
    for each in value:
        values += each
    # print values
    ch = chardet.detect(values)["encoding"]
    values = values.decode(ch).encode("utf-8")
    fd.close()
    part = MIMEText("Dear ALL, "
                    "\n\nThis is the latest test result of automation:\n{0}"
                    "\n\n\nIt is an automated sent email. "
                    "\nNo need to reply... it won't be answered anyway."
                    "\nAny issue please contact with the sender"
                    "\n\nThanks!"
                    "\n\nWarning Notice: If You see the Mess code, Please set the mailbox as encoding as UTF-8.".format(values))
    msg.attach(part)

    # The attachment part of the message
    fp = open("%s" % file_to_send, "rb")
    part = MIMEApplication(fp.read())
    fp.close()
    part.add_header('Content-Disposition', 'attachment', filename="%s" % file_to_send)
    msg.attach(part)

    # Create an instance of a SMTP server
    sp = SMTP()
    sp.connect('%s' % config.smtp_sever)
    # Start the server
    sp.set_debuglevel(0)
    # sp.ehlo()
    sp.starttls()
    sp.login('%s' % config.email_sender, '%s' % config.email_sender_password)

    # Send the email
    sp.sendmail(msg['From'], mail_to, msg.as_string())
    sp.quit()
#
# if __name__ == "__main__":
#     send_email("log.txt", "log.txt", ["andy.zheng@gaopeng.com"])
