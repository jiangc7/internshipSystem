import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# email details
from flask import session

sender_email = 'lincolnplacementstaff@gmail.com'
sender_password = 'pnqydbmsytwdegki'

# create message object



def sentPasswordEmail(to):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    # establish connection with SMTP server
    msg['To'] = to
    msg['Subject'] = "Reset your password"
    msg.attach(MIMEText("<a href=http://localhost:5000/forgotPassword?key=%s> please click this to reset your password</a>"%(to), 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # enable encryption
        smtp.login(sender_email, sender_password)

        smtp.send_message(msg)


def sentStudentMatchingNotify(student,mentor):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = student
    msg['Subject'] = "Matching notification!"
    msg_content = "You have successfully matched with : <br>"
    for men in mentor:
        msg_content += "project: %s,from <a href=mailto:%s> %s </a>, website: <a href=%s> %s </a> <br>" % (
        men['project_title'],men['email'], men['company_name'], men['website'], men['website'])

    msg.attach(MIMEText(msg_content, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # enable encryption
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)


def sentMentorMatchingNotify(student,mentor):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = "Matching notification!"
    msg_content = "You have successfully matched with students: <br>"
    mentor = ",".join(mentor)
    msg['To'] = mentor
    msg_content += "<a href=mailto:%s> %s %s </a>, CV: <a href='http://localhost:5000/download/%s'> %s's CV  </a> <br>" % (
    student['email'], student['first_name'], student['last_name'], student['cv'],student['first_name'])

    msg.attach(MIMEText(msg_content, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # enable encryption
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

def sendEmail(subject,body,email):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    # establish connection with SMTP server
    msg['To'] = sender_email
    msg['Subject'] = subject + " from :" + email
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # enable encryption
        smtp.login(sender_email, sender_password)

        smtp.send_message(msg)

