import psutil
import datetime
import smtplib
import os

# Getting the disk usage in percentage
disk = psutil.disk_usage('/').percent
threshold = 8

# open the logging file
f = open("disk-monitoring.log", "a")

# Check disk usage
if disk > threshold:
    print(f"Warning!, disk usage has reached {disk}%")
    f.write(f"{datetime.datetime.now()}     usage: {disk}%\n")

    # extracting ip address of the machine
    current_interface = ""

    for i in psutil.net_if_stats():
        if "up" in psutil.net_if_stats()[i].flags and i != "lo":
            current_interface = i
            break

    ip_address = psutil.net_if_addrs()[current_interface][0].address

    # send email
    mail = smtplib.SMTP("smtp.gmail.com", 587)
    mail.starttls()
    sender_email = "akashsheoranwwe@gmail.com"
    sender_password = os.environ['EMAIL_PASSWORD']
    mail.login(sender_email, sender_password)
    subject = "Warning! disk usage"
    body = f"Disk usage has reached - {disk}% \n IP Address of the server is - {ip_address}"
    message = "Subject:{}\n\n{}".format(subject, body)
    listOfAddrs = ["akashsheoranwwe@gmail.com"]
    mail.sendmail(sender_email, listOfAddrs, message)
    mail.quit()

else:
    print(f"Disk usage is normal - {disk}%")
    f.write(f"{datetime.datetime.now()}     usage: {disk}%\n")

f.close()