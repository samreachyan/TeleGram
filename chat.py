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
    input_file = sys.argv[1]
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)
    print(gr+"[1] send sms by user ID\n[2] send sms by username")
    mode = int(input(gr+"Input : "+re))

    # message = input(gr+"[+] Enter Your Message : "+re)
    # get messsage from argv[2]
    message = sys.argv[2]
    with open(message, 'r') as f:
        msg = f.read()

    # fileAttach = sys.argv[3]
    # get Multiple file from argv[3] to argv[n]
    files = []
    for file in sys.argv[3:]:
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

    for user in users:
        if mode == 2:
            if user['username'] == "":
                continue
            receiver = client.get_input_entity(user['username'])
        elif mode == 1:
            receiver = InputPeerUser(user['id'], user['access_hash'])
        else:
            print(re+"[!] Invalid Mode. Exiting.")
            client.disconnect()
            sys.exit()
        try:
            print(gr+"[+] Sending Message to:", user['name'])

            # Send Text Message & Send Media Message [Video / Audio / File]
            client.send_message(
                receiver, msg.format(user['name']), file=files)

            print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
            time.sleep(SLEEP_TIME)
        except PeerFloodError:
            print(
                re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")

            sys.exit()
        except Exception as e:
            print(re+"[!] Error:", e)
            print(re+"[!] Trying to continue...")
            continue
    print("Done. Message sent to all users.")


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
