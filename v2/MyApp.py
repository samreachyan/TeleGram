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
        status = cpass['cred']['status']

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


def readText(file):
    '''
        read text file
        return list of text
    '''
    with open(file, 'r', encoding="utf8") as f:
        msg = f.read()
    return msg


def configDB(host, user, password, database):
    mydb = mysql.connector.connect(
        host=host, user=user, password=password, database=database).cursor()

    mydb.execute(
        "SELECT name, number, created_at FROM `services` JOIN users ON users.service_id = services.id")

    result = mydb.fetchall()
    return result


def updateStatus(status):
    cpass = configparser.RawConfigParser()
    # set status = 0 not downloads
    cpass.set('cred', 'status', status)
    with open('config.data', 'wb') as configfile:
        cpass.write(configfile)


class WorkingThread(Thread):
    '''
        function working thread
    '''

    def __init__(self, target_group, status):
        Thread.__init__(self)
        self.running = True
        self.target_group = target_group
        self.status = status

    def run(self):
        if self.running and self.status:
            # Connect DB save CSV
            # Convert to PNG
            # Send sms

            # sleep 23h50mn
            print('Working...' + self.target_group.title)
            self.changeStatus(False)

            time.sleep(1)

    def stop(self):
        self.running = False

    def changeStatus(self, status):
        self.status = status  # update status to config.data

    def getStatus(self):
        return self.status


if __name__ == '__main__':
    # config.data to login Telegram API
    client = config()
    # get index of target group or channel
    target_group = getTargetGroup(client)

    print("Running...")
    status = True
    while True:
        try:
            # create a thread
            thread = WorkingThread(target_group, status)
            # start the thread
            thread.start()

            # do something else
            # time.sleep(60*60*24)
            time.sleep(30)

            # stop the thread
            thread.stop()
            thread.changeStatus(True)  # task done and update status
            status = thread.getStatus()  # get current status

        except KeyboardInterrupt:
            thread.join()  # wait thread get finished and then stop
            thread.stop()  # stop thread
            print("Stopping by key")
            break
        except:
            thread.join()
            thread.stop()
            print("Stopping by error")
            break
    client.disconnect()
    print("Stopped running")
