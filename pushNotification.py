#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerUser
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
        print(
            re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")

        sys.exit()
    except Exception as e:
        print(re+"[!] Error:", e)
        print(re+"[!] Trying to continue...")

    print("Done. Message sent to group: +" + target_group.title)
    sys.exit()


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
