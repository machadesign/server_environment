#!/usr/bin/env python3

# from email_fruit_report -- smtp setup
# email_reports.py   -- create a pdf and send


import getpass
import email.message
import mimetypes
import os.path
import smtplib
from run_warnings import list_of_warnings
import json

config_json = "/Users/matthewchadwell/server_environment/project_files/config.json"

with open(config_json) as f:
    data = json.load(f)
    print(data)
    contact_email = data["email"]
    sender_email = data["Sender_email"]

sender = sender_email
recipient = contact_email
subject = 'Server snapshot Warnings'
body = 'The following warnings based on thresholds set and current server data.'
# attachment_path = 'pdf attachment location'


# message_content = email_generator(sender, recepient, subject, body, attachment_path)
# ?? send in send function below... email_send(message_content)
#     msg = email_generate("automation@example.com", "student-03-fc0c247f4859@example.com",
#                          "Sales summary for last month", new_summary, "/tmp/cars.pdf")
# print(email_generator(sender, recepient, subject, body, attachment_path))


# report_email.py
# create another script for generating


def send_email(sender_a, recepient_a, subject_a, body_a):
    """Creates an email with an attachement."""
  # Basic Email formatting
    message = email.message.EmailMessage()
    message["From"] = sender_a
  # for sender, recepient etc. access variables form the information above
    message["To"] = recepient_a
    message["Subject"] = subject_a
    message.set_content(body_a)

    # Process the attachment and add it to the email
    # attachment_path = "Acars.pdf"
    # attachment_filename = attachment_path

    # mime_type, _ = mimetypes.guess_type(attachment_path)
    # mime_type, mime_subtype = mime_type.split('/', 1)
    # print(mime_type, mime_subtype)
    # with open(attachment_path, 'rb') as ap:
    #     message.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, filename=os.path.basename(attachment_filename))
    #     ## message.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, filename=attachment_filename)
    # return(message)

    # return message
    # print(message)

# def send_email(message):
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
    mail_pass = 'Chink1bot,,'
    # mail_pass = getpass.getpass('Chink1bot,,')
    # print(sender)
    mail_server.login('chankleymatt@gmail.com', mail_pass)
    mail_server.send_message(message)
    mail_server.quit()


file = str(list_of_warnings)
print(file)
print(list_of_warnings)
send_email(sender,recipient, subject, body_a=file)
