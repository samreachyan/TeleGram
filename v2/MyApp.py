#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from threading import Thread
from datetime import date
import configparser
import os
import sys
import time
import datetime
import csv
import pandas as pd
import dataframe_image as dfi
import mysql.connector


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
        print("[!] run python3 setup.py first !!\n")
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
        print('['+str(i)+']'+' - ' + g.title)
        i += 1

    print('')
    g_index = input("[+] Enter a Number : ")
    return groups[int(g_index)]


def processWorker(client, target_group):
    print("Calling processWorker", target_group.title)

    # fake object data list
    data = []
    for i in range(0, 10):
        data.append({"id": i, "name": "name" + str(i), "age": i})

    # create dataframe
    df = pd.DataFrame(data, columns=["id", "name", "age"])
    df_styled = df.style.background_gradient()

    fileName = date.today().strftime("%b-%d-%Y") + ".png"

    # export to png
    dfi.export(df_styled, fileName)

    # get messgge from date time
    now = datetime.datetime.now()
    msg = "Reported at " + now.strftime("%d/%m/%Y %H:%M:%S") + \
        "\nThis is Telegram API"

    # // TODO : Error cannot send message
    # send message to group or channel
    # client.send_message(target_group, msg, file=fileName)

    print("Sent ", now.strftime("%d/%m/%Y %H:%M:%S"))


class WorkingThread(Thread):
    '''
        function working thread
    '''

    def __init__(self):
        Thread.__init__(self)
        self.client = config()
        self.target_group = getTargetGroup(self.client)

    def run(self):
        # infinite loop run forever
        while True:
            try:
                # calling process function
                self.love()  # call in class
                # should call method in class
                processWorker(self.client, self.target_group)

                # sleep 23h50mn
                time.sleep(60 * 5)  # Thread sleep 5 minute
            except KeyboardInterrupt:
                print("\n[!] Exiting..")
                sys.exit(1)
            except:
                print("Thread processing is error")
                sys.exit(1)

    def love(self):
        return print("I love you", self.target_group.title)


if __name__ == '__main__':
    print("Main running")
    try:
        # create a thread
        thread = WorkingThread()
        # start the thread
        thread.start()

    except:
        print("Error to start thread")
