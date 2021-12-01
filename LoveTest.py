#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from threading import Thread
import datetime
import configparser
import sys
import time
import pandas as pd
import dataframe_image as dfi
import mysql.connector

target_group = None


def config():
    '''get index of target group or channel'''
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
    # client = config()
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
        print('['+str(i)+'] - ' + g.title)
        i += 1

    print('')
    g_index = input("[+] Enter a Number : ")
    return groups[int(g_index)]


def configDB(host, user, password, database):
    mydb = mysql.connector.connect(
        host=host, user=user, password=password, database=database).cursor()

    mydb.execute(
        "SELECT name, number, created_at FROM `services` JOIN users ON users.service_id = services.id")

    result = mydb.fetchall()
    return result


async def sendSMS():
    # Now you can use all client methods listed below, like for example...
    await client.send_message('me', 'Hello to myself!')


def Task(client, target_group):

    count = 0
    while count < 5:
        count += 1
        print("Calling processWorker", count)
        # Thread worker process to send message forever

        print("Calling processWorker", target_group.title)

        # fake object data list
        data = []
        for i in range(0, 10):
            data.append({"id": i, "name": "name" + str(i), "age": i})

        # create dataframe
        df = pd.DataFrame(data, columns=["id", "name", "age"])
        df_styled = df.style.background_gradient()

        now = datetime.datetime.now()
        fileName = now.strftime("%b-%d-%Y") + ".png"

        # export to png
        dfi.export(df_styled, fileName)

        # get messgge from date time
        msg = "Reported at " + now.strftime("%d/%m/%Y %H:%M:%S") + \
            "\nThis is Telegram API"

        # // TODO: Problem send message too ???
        # send message to group or channel
        # await client.send_message('me', msg, file=fileName)
        # with client:
        #     client.loop.run_until_complete(sendSMS(client))
        # sendSMS(client)
        with client:
            client.loop.run_until_complete(sendSMS())

        print("Sent ", now.strftime("%d/%m/%Y %H:%M:%S"))
        time.sleep(60)  # Thread sleep 1 minute


if __name__ == "__main__":
    client = config()
    # if target_group is None:
    target_group = getTargetGroup(client)

    Task(client, target_group)

    # try:
    #     th = Thread(target=Task, args=(client, target_group,))
    #     th.start()
    # except:
    #     print('[!] Error starting thread')

    # while 1:
    #     pass
