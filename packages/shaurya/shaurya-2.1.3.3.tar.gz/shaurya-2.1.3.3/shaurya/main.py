# shaurya-1.1.2
import datetime  
import smtplib
import random

def Authenticate(variable, content):
    """
    Used to easy authenticate,
    Authenticate(variable to insert, the actual pass)
    """
    if variable == content:
        return True
    else:
        return False

def telltime():
    """
    Used to tell the current time. It returns the time
    """
    current_time = datetime.datetime.now()  
    hour = str(current_time.hour)
    minute = str(current_time.minute)
    second = str(current_time.second)
    time = [hour," : " ,minute, " : " ,second]
    str1 = ""  
    for ele in time:  
        str1 += ele     
    return str1

def send_email(sender, passw,reciev, mess):
    """ send_email(your email, your password, reciever, message) """
    email = smtplib.SMTP('smtp.gmail.com', 587)
    email.starttls()
    email.login(sender, passw)
    message = mess
    email.sendmail(sender, reciev, message)
    email.quit()

import webbrowser

def search_browser(content):
    """
    searches anything in your default browser and opens it.
    """
    search = "https://www.google.com/search?sxsrf=ALeKk03VTHs8LQWWw_7KDDAW9TKnfbz4Mg%3A1599222408960&ei=iDJSX4SQOtXSz7sPiLuiwAU&q="+content+"&gs_lcp=CgZwc3ktYWIQAxgAMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHUABYAGCkOmgAcAF4AIABAIgBAJIBAJgBAKoBB2d3cy13aXrAAQE&sclient=psy-ab"
    webbrowser.open(search)


def search_youtube(content):
    """searches the argument in youtube and opens it"""
    search = "https://www.youtube.com/results?search_query="+content
    webbrowser.open(search)

def return_url_youtube(content):
    search = "https://www.youtube.com/results?search_query="+content
    return search

def return_url_browser(content):
    search = "https://www.google.com/search?sxsrf=ALeKk03VTHs8LQWWw_7KDDAW9TKnfbz4Mg%3A1599222408960&ei=iDJSX4SQOtXSz7sPiLuiwAU&q="+content+"&gs_lcp=CgZwc3ktYWIQAxgAMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHMgQIABBHUABYAGCkOmgAcAF4AIABAIgBAJIBAJgBAKoBB2d3cy13aXrAAQE&sclient=psy-ab"
    return search

import requests

def get_status_code(site):
    s = "http://"+site
    response = requests.get(s)
    data={
        "status":response.status_code,
    }
    return data

def print_beautify(var):
    """
    returns the text in a very beautiful way
    """
    leng = len(var)
    for x in range(leng):
        print("_",end='')
    print("\n")
    var = print(var)
    for x in range(leng):
        print("_", end='')
    print("\n")  


import random
import smtplib
import webbrowser


def generate_number(digitcode):
    """
    Generates a random number | generate_number(number of digits you want)
    """
    digits = [str(num) for num in range(digitcode)]
    random.shuffle(digits)
    s = ""
    s = s.join(digits)
    return s


def send_email_otp(sender, passw, reciev, mess):
    email = smtplib.SMTP('smtp.gmail.com', 587)
    email.starttls()
    email.login(sender, passw)
    message = mess
    email.sendmail(sender, reciev, message)
    email.quit()



def OTP(sender, passw, reciever, digitcode):
    """
    Only sends the OTP through email does not authenticate it.
    """
    vandoe = generate_number(digitcode)
    send_email_otp(sender, passw, reciever, vandoe)

