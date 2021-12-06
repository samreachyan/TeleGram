#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl import functions
from telethon.tl.types import InputPhoneContact
import configparser

try:
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
except KeyError:
    print("[!] run python3 setup.py first !!\n")

result = {}


def get_info(phone_number):
    try:
        contact = InputPhoneContact(
            client_id=0, phone=phone_number, first_name="", last_name="")
        contacts = client(functions.contacts.ImportContactsRequest([contact]))
        username = contacts.to_dict()['users'][0]['username']
        user_id = contacts.to_dict()['users'][0]['id']
        access_hash = contacts.to_dict()['users'][0]['access_hash']
        msg = 'Ok'

        functions.contacts.DeleteContactsRequest(
            id=[username])  # Delete the contact

    except IndexError as e:
        msg = f'ERROR: there was no response for the phone number: {phone_number}'
    except TypeError as e:
        msg = f"TypeError: {e}. --> The error might have occured due to the inability to delete the {phone_number} from the contact list."
    except:
        raise

    return {username, user_id, access_hash, msg}


def user_validate():
    '''
    Function to validate the user avaiable on Telegram or not
    '''
    input_phones = input("Enter the phone number: ")
    phones = input_phones.split()

    try:
        for phone in phones:
            api_res = get_info(phone)
            result[phone] = api_res
    except:
        raise Exception("[!] Connection Error")


if __name__ == "__main__":
    client = TelegramClient(phone, api_id, api_hash)
    with client:
        client.connect()
        user_validate()

        # display all dict
        # for key, value in result.items():
        #     print(f"{key} : {value}")

        print(result)
