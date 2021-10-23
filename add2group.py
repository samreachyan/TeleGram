#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os
import sys
import csv
import traceback
import time
import random

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"


def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

            version : 3.0
        """)


cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] run python3 setup.py -i !!\n")
    sys.exit(1)

file = sys.argv[1]


async def main():
    # Now you can use all client methods listed below, like for example...
    await client.send_message('me', 'You are adding members via API to group or channel')


SLEEP_TIME_1 = 100
SLEEP_TIME_2 = 100
with client:
    client.loop.run_until_complete(main())
client.connect()
users = []
with open(file, "r", encoding='UTF-8') as f:  # Enter your file name
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {
            'username': row[0],
            'id': int(row[1]),
            'access_hash': int(row[2]),
            'name': row[3],
        }

        users.append(user)

chats = []
last_date = None
chunk_size = 900
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
        # if chat.megagroup == True:
        if True:
            groups.append(chat)
    except:
        continue

print('Choose a group to add members: ')
for i, group in enumerate(groups):
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+group.title)
g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(
    target_group.id, target_group.access_hash)

mode = int(input("Enter 1. to add by username \nEnter 2. to add by ID: "))

n = 0

for user in users:
    n += 1
    if n % 80 == 0:
        time.sleep(60)
    try:
        print("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Waiting for 60-180 Seconds ...")
        time.sleep(random.randrange(0, 5))
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        print("Waiting {} seconds".format(SLEEP_TIME_2))
        time.sleep(SLEEP_TIME_2)
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping ...")
        print("Waiting for 5 Seconds ...")
        time.sleep(random.randrange(0, 5))
    except:
        traceback.print_exc()
        print("Unexpected Error! ")
        continue
