#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
from threading import Thread
import configparser
import os
import sys
import time
import datetime


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


def send_sms(client, target_group):
    '''Sending sms to group or channel'''
    # Read message from text file
    fileAttach = sys.argv[1]
    with open(fileAttach, 'r') as f:
        message = f.read()

    try:
        client.send_message(
            target_group, message)
        print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)
    except PeerFloodError:
        print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")

        sys.exit()
    except Exception as e:
        print(re+"[!] Error:", e)
        print(re+"[!] Trying to continue...")

    print("Message sent to: " + target_group.title)


def tasking():
    print("Thread started running")


# get target group
target_group = list()


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
client.start()

# get id group or channel
chats = []
last_date = None
chunk_size = 100
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if True:
            groups.append(chat)
    except:
        continue

# print group or channels
i = 0
for g in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - ' + g.title)
    i += 1

print('')
g_index = input(gr+"[+] Enter a Number : "+re)
target_group = groups[int(g_index)]
# finishing getting id target_group

message = "text.txt"
with open(message, 'r', encoding="utf8") as f:
    msg = f.read()

fileImage = "mytable.png"

# print(target_group)

t1 = Thread(target=tasking)
t1.start()

while True:
    try:
        now = datetime.datetime.now()
        print("Current date and time : ")
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        client.send_message(
            target_group, msg, file=fileImage)
        time.sleep(60 * 2)
    except KeyboardInterrupt:
        print("stopping")
        break

t1.join()
client.disconnect()
print("done")
