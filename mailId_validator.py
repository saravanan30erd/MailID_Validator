import time
import re
import dns.resolver
import smtplib
from sys import argv as ARG

def basic_check(mail_id):
    if re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', mail_id):
        return True
    else:
        append_invalid_file(mail_id)
        return False
    
def append_invalid_file(mail_id):
    with open('invalid_mail_ids.txt', 'a') as text_file:
        text_file.writelines(mail_id + '\n')

def append_valid_file(mail_id):
    with open('valid_mail_ids.txt', 'a') as text_file:
        text_file.writelines(mail_id + '\n')

def append_main_file(mail_id):
    with open('blocked_mail_ids.txt', 'a') as text_file:
        text_file.writelines(mail_id + '\n')

def smtp_check(records, mail_id):
    mxrecord = str(records[0].exchange)
    server = smtplib.SMTP()
    server.set_debuglevel(0)
    try:
        server.connect(mxrecord)
        server.helo(server.local_hostname)
        from_address = ''.join(['test', '@', server.local_hostname])
        con_code, con_err = server.mail(from_address)
        code, message = server.rcpt(mail_id)
        server.quit()
        if code == 250:
            append_valid_file(mail_id)
        else:
            append_invalid_file(mail_id)
    except Exception as e:
        print str(e)
        print con_err
        if 'troubleshooting.aspx#errors' in str(con_err):
            append_main_file(mail_id)

def mx_check(mail_id):
    domain = str(mail_id.split('@')[1])
    try:
        records = dns.resolver.query(domain, 'MX')
        if records.expiration:
            smtp_check(records, mail_id)
        else:
            append_invalid_file(mail_id)
    except:
        append_invalid_file(mail_id)


def main(num_mail_ids, interval):
    with open('mail_ids.txt') as mail_ids:
        count = 0
        for mail_id in mail_ids:
            mail_id = str(mail_id.rstrip())
            if count >= num_mail_ids:
                if basic_check(mail_id):
                    mx_check(mail_id)
                time.sleep(interval)
                count = 0
            else:
                if basic_check(mail_id):
                    mx_check(mail_id)
                count += 1

if __name__=='__main__':
    try:
        num_mail_ids = int(ARG[1])-1
        interval = int(ARG[2])
    except:
        num_mail_ids = 1
        interval = 600
    finally:
        main(num_mail_ids, interval) 
