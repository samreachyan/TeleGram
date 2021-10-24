#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os
import sys
import csv
import random
import time


re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
SLEEP_TIME = 10

print(f"""
    {re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
    {re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
    {re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

                version : 3.1
            """)


def send_sms():
    # os.system('clear')
    # get messsage from argv[1]
    message = sys.argv[1]
    with open(message, 'r') as f:
        msg = f.read()

    # get Multiple file from argv[2] to argv[n]
    files = []
    for file in sys.argv[2:]:
        files.append(file)

    # function check multiple file
    def checkisfile(files):
        for file in files:
            if not os.path.isfile(file):
                return False
        return True

    if checkisfile(files) == True:
        print(gr+"[+] File exists")
    else:
        print(re+"[!] File not exists")
        sys.exit()

    # input phone number
    phoneNumber = input(f'{gr}[+] Input Phone Number : ')

    # send message to phone number
    try:
        print(gr+"[+] Sending Message ... to ", phoneNumber)
        client.send_message('me', 'Sending message to phone number via API!!')
        client.send_message(phoneNumber, msg, file=files)
        print(gr+"[+] Message was sent successfully")
    except PeerFloodError:
        print(re+"[!] Due to Flooding Error, Message was not sent")
        sys.exit()
    except Exception as error:
        print(re+"[!] Error : " + str(error))
        sys.exit()

    print(gr+"[+] Messages send done!")


# reading files config.data
try:
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
except KeyError:
    os.system('clear')
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client = TelegramClient(phone, api_id, api_hash)

with client:
    client.loop.run_until_complete(send_sms())
