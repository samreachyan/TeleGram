#!/bin/env python3
import asyncio
from logging import logProcesses
from time import perf_counter
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import datetime
import configparser
import pandas as pd
import dataframe_image as dfi
import mysql.connector


try:
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
except KeyError:
    print("[!] run python3 setup.py first !!\n")


def getTargetGroup():
    '''get index of target group or channel'''
    # client = config()
    with TelegramClient(phone, api_id, api_hash) as client:
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


async def Task(target_group, delay):
    while True:
        start = perf_counter()
        print("Called processWorker", target_group.title)

        # fake object data list
        data = []
        for i in range(0, 10):
            data.append({"id": i, "name": "name" + str(i), "age": i})

        # create dataframe
        df = pd.DataFrame(data, columns=["id", "name", "age"])
        df_styled = df.style.background_gradient()

        # rename fileName by DateTime
        now = datetime.datetime.now()
        fileName = now.strftime("%b-%d-%Y") + ".png"

        # export to png
        dfi.export(df_styled, fileName)

        # get messgge from date time
        msg = "Reported at " + now.strftime("%d/%m/%Y %H:%M:%S") + \
            "\nThis is Telegram API"

        # TODO: Problem send message
        # send message to group or channel
        async with TelegramClient(phone, api_id, api_hash) as client:
            try:
                await client.connect()
                await client.send_file(target_group, fileName, caption=msg)
                await client.disconnect()
                print("Done! Sent to ", target_group.title,
                      now.strftime("%d/%m/%Y %H:%M:%S"))
            except:
                print("[!] Error send message to group or channel")

        end = perf_counter() - start
        # print("Processed in {} seconds".format(end))
        await asyncio.sleep(delay - end)


if __name__ == "__main__":
    # connection telegram get target group or channel
    target_group = getTargetGroup()

    # start tasking
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(Task(target_group, 30))  # delay 5 minutes
    try:
        loop.run_forever()
        # loop.run_until_complete(asyncio.sleep(5))
    except:
        print('[!] Force to stop task')
        # check and cancel task is running
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.close()

    print("[+] Done")
