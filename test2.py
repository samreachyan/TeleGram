#!/bin/env python3
import asyncio
from itertools import count
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from threading import Thread
import datetime
import time
import configparser
import sys
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
    try:
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
    except Exception as e:
        print(e)
        print("[!] Error")
    # finally:
        # client.disconnect()

    return groups[int(g_index)]


def configDB(host, user, password, database):
    mydb = mysql.connector.connect(
        host=host, user=user, password=password, database=database).cursor()

    mydb.execute(
        "SELECT name, number, created_at FROM `services` JOIN users ON users.service_id = services.id")

    result = mydb.fetchall()
    return result


async def Task(client, target_group, delay):
    # while True:
    print("Called processWorker", target_group.title)

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

    # // TODO: Problem send message
    # send message to group or channel
    try:
        # await client.connect()
        await client.send_file(target_group, fileName, caption=msg)
        # await client.disconnect()
    except:
        print("[!] Error send message to group or channel")

    print("Done! Sent to ", target_group.title,
          now.strftime("%d/%m/%Y %H:%M:%S"))
    await asyncio.sleep(delay)


async def hello(delay):
    # while True:
    count = 0
    while count < 10:
        print("Hello", count)
        count += 1
        await asyncio.sleep(delay)
    # print("before hello sleep")
    # await asyncio.sleep(delay)
    # print("Hello World")


async def target_group_telegram():
    try:
        cpass = configparser.RawConfigParser()
        cpass.read('config.data')
        api_id = cpass['cred']['id']
        api_hash = cpass['cred']['hash']
        phone = cpass['cred']['phone']

        client = await TelegramClient(phone, api_id, api_hash).start()

        chats = []
        last_date = None
        chunk_size = 100
        groups = []

        result = await client(GetDialogsRequest(
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
    except Exception as e:
        print(e)
        print("[!] Error")


async def process_work(target_group, delay):
    # if we config connect telegram and target group info below here
    # so we have to re-select target group id all time before tasking

    try:
        cpass = configparser.RawConfigParser()
        cpass.read('config.data')
        api_id = cpass['cred']['id']
        api_hash = cpass['cred']['hash']
        phone = cpass['cred']['phone']

        client = await TelegramClient(phone, api_id, api_hash).start()

        print("Called processWorker", target_group.title)
        # chats = []
        # last_date = None
        # chunk_size = 100
        # groups = []

        # result = await client(GetDialogsRequest(
        #     offset_date=last_date,
        #     offset_id=0,
        #     offset_peer=InputPeerEmpty(),
        #     limit=chunk_size,
        #     hash=0
        # ))
        # chats.extend(result.chats)

        # for chat in chats:
        #     try:
        #         if True:
        #             groups.append(chat)
        #     except:
        #         continue

        # # print group or channels
        # i = 0
        # for g in groups:
        #     print('['+str(i)+'] - ' + g.title)
        #     i += 1

        # print('')
        # g_index = input("[+] Enter a Number : ")
        # target_group = groups[int(g_index)]
        await client.send_message('me', "Hello World")

    except Exception as e:
        print(e)
        print("[!] Error")
    finally:
        # await hello(2)
        await client.disconnect()  # Disconnect telegram after done task

    now = datetime.datetime.now()
    print("Done! Sent ", now.strftime("%d/%m/%Y %H:%M:%S"))

    # asyncio sleep 60 seconds
    await asyncio.sleep(delay)


def go(target_group):
    print("[+] Start process worker", target_group)
    # set asyncio event loop forever
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(process_work())
    asyncio.run(process_work(target_group, 10))
    print("[+] End process worker")


if __name__ == "__main__":
    print("[+] Start")

    # if we config target group id first then error when reconnect telegram to send message

    client = config()
    target_group = getTargetGroup(client)
    print("[+] Got Target Group", target_group.title)

    try:
        th = Thread(target=go, args=(target_group,))
        th.start()
    except Exception as e:
        print(e)
        print("[!] Error")

    print("[+] Done finished thread task")
    count = 0
    while count < 5:
        print("Main work", count)
        count += 1
        time.sleep(1)
