"""
I created this program to help validate
emails using PyDNS. 
"""
import re 
import smtplib 
import dns.resolver
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

def isValidIp(hostname):
    """ Check if the hostname is valid, and if it is get mx_record """
    mx_records = DNS.resolver.query(hostname, 'MX')
    return (True, mx_records)


#def isValidServer():
    

def main():

    email_final = ""

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
    hostname = str(split_email[1])

    mx_record = isValidIp(hostname)
    if not mx_record[0]:
        print("Invalid Hostname")
        sys.exit()
    else:
        print(mx_record[1])


    


    





















if __name__ == "__main__":
    main()