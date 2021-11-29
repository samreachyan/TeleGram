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


def configDB(host, user, password, database):
    mydb = mysql.connector.connect(
        host=host, user=user, password=password, database=database).cursor()

    mydb.execute(
        "SELECT name, number, created_at FROM `services` JOIN users ON users.service_id = services.id")

    result = mydb.fetchall()
    return result


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
            if now.strftime("%H:%M:%S") == "17:28:00":
                # delete file.png
                # os.remove("mytable.png")

                data = configDB(host="localhost", user="root",
                                password="", database="telegram")

                with open("mydata.csv", "w", encoding="UTF-8") as f:
                    writer = csv.writer(f, delimiter=",", lineterminator="\n")
                    writer.writerow(["Name", "N-1", "N-3",
                                    "N-7", "Total", "Date Time"])

                    for row in data:
                        writer.writerow([row[0], row[1], row[1] * 3, row[1]
                                        * 7, row[1] * 30, row[2]])

                # create Thread convert to PNG
                t1 = Thread(target=convertToPng, args=("mydata.csv",))
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
