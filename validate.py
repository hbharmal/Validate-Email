"""
I created this program to help validate
emails using PyDNS. 
"""
import re 
import smtplib 
import DNS
import socket 
import sys

# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

class InvalidEmailError(Error):
    """ Raised if Email is not valid """
    pass 

class InvalidServerError(Error):
    """ Raised if Server is not valid """
    pass

text = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

def isValidEmail(email):
    if re.match(text, email):
        return True
    else:
        return False 

def isValidIp(domain_name):
    """ Check if the hostname is valid, and if it is get mx_record """
    try:
        mx_records = DNS.mxlookup(domain_name)
        return (True, mx_records)
    except InvalidServerError:
        return (False, None)


#def isValidServer():
    

def main():

    email_final = ""
    timeout = 5000

    while (True):
        try:
            email = input('Please enter an email address: ')
            if not isValidEmail(email):
                raise InvalidEmailError 
            else:
                email_final = email 
                break
        except InvalidEmailError:
            print("The email is not valid, please enter a valid email address")
            continue 
    
    split_email = email_final.split('@')
    domain_name = str(split_email[1])

    InvalidServerError = DNS.ServerError

    mx_record = isValidIp(domain_name)

    if not mx_record[0]:
        print("Invalid Hostname, please try again.")
        sys.exit()

    mx_domain = mx_record[1][0][1]
    print(mx_domain)


    hostname = socket.gethostname()

    try:

        smtp = smtplib.SMTP(timeout=timeout)
        smtp.connect(mx_domain)
        response_helo = smtp.helo(hostname)

        if (response_helo[0] != 250):
            smtp.quit()
            print("HELO failed with status code: " + response_helo[0])
            sys.exit()

        response_mail = smtp.mail('none@fakedomain.com')

        if (response_mail[0] != 250):
            smtp.quit()
            print("MAIL faile with status code: " + response_mail[0])
            sys.exit()
        smtp.quit()

        assert response_helo[0] == 250 and response_mail[0] == 250

        print("Email is valid!")
        sys.exit()

    except smtplib.SMTPServerDisconnected:
        print("SMTP Server Disconnected!")
        sys.exit()

    except smtplib.SMTPConnectError:
        print("Failed to Connect to SMTP Server!")
        sys.exit()
    
    except socket.error as e:
        print("Socket error, could not get hostname!")
        print(e)
        sys.exit()
    

if __name__ == "__main__":
    main()