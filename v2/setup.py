#!/bin/env python3
import configparser


def config_setup():
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    xid = input("[+] enter api ID : ")
    cpass.set('cred', 'id', xid)
    xhash = input("[+] enter hash ID : ")
    cpass.set('cred', 'hash', xhash)
    xphone = input("[+] enter phone number : ")
    cpass.set('cred', 'phone', xphone)
    # set status = 0 not download
    cpass.set('cred', 'status', 'True')
    setup = open('config.data', 'w')
    cpass.write(setup)
    setup.close()
    print("[+] setup complete !")


if __name__ == '__main__':
    try:
        config_setup()
    except KeyboardInterrupt:
        print("Error to setup!")
