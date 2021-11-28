#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from threading import Thread
import configparser
import os
import sys
import time
import datetime
import csv
import pandas as pd
import dataframe_image as dfi


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


def tasking():
    print("Thread started running")


def convertToPng(fileCSV):
    '''
        function convert file CSV to PNG
        return file_name
    '''
    users = []
    with open(fileCSV, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)

    df = pd.DataFrame(users, columns=list(
        ['username', 'id', 'access_hash', 'name']))

    # adding a gradient based on values in cell
    # df_styled = df.style.background_gradient()
    # df_styled = df.style.set_precision(2)
    df_styled = df.style.hide_index()

    dfi.export(df_styled, "mytable.png")
    return str("mytable.png")


def config(cfg="config.data"):
    '''config.data to login Telegram API'''
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
    return client


def getTargetGroup(client):
    '''get index of target group or channel'''
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
    return groups[int(g_index)]


def readText(file):
    '''
        read text file
        return list of text
    '''
    with open(file, 'r', encoding="utf8") as f:
        msg = f.read()
    return msg


if __name__ == "__main__":
    # config login Telegram API
    client = config()

    # pick group or channel
    target_group = getTargetGroup(client)

    print("Running")
    while True:
        try:
            now = datetime.datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S --"))
            time.sleep(1)

            # check time is 11:00 am
            if now.strftime("%H:%M:%S") == "11:00:00":
                # delete file.png
                os.remove("mytable.png")
                # create Thread convert to PNG
                t1 = Thread(target=convertToPng, args=("members.csv",))
                t1.start()
                t1.join()

                print("Current date and time : ")
                print(now.strftime("%Y-%m-%d %H:%M:%S"))

                # get messgge from date time
                msg = "Reported at " + \
                    now.strftime("%d/%m/%Y %H:%M:%S") + \
                    "\nThis is Telegram API"

                client.send_message(
                    target_group, msg, file="mytable.png")

                print("Sleeping for 23h and 59min!")
                time.sleep(60 * 60 * 24 - 60)

        except KeyboardInterrupt:
            print("Stopping")
            break

    # finish and disconnect Telegram API
    client.disconnect()
    print("Stopped running")
