import json
import os
from sys import exit
from threading import Thread
import time

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

address = 'N3FDuSqd4FHZ6DSZtXJgNGr3Tyq4ni8CFL'

def check(add):
    initial = True  
    while 1:
        if not initial and add != prox.name_history(name)[-1]['address']:
            exit()

        print 'valid at %s' % time.asctime()

        initial = False
        time.sleep(600)

if __name__ == '__main__':
    try:
        file = open('keys.txt', 'rb')
        keys = json.load(file)
        name = keys['name']
        file.close()
    except:
        name = raw_input('Enter name\n')
        file = open('keys.txt', 'wb')
        json.dump(dict(name=name), file)
        file.close()

    try:
        prox = AuthServiceProxy('http://user:password@127.0.0.1:8336')

        valid = False
        for add in prox.name_history(name):
            if add['address'] == address:
                valid = True
        if not valid:
            print 'Invalid address.'
            os.remove('keys.txt')
            exit()

        add = prox.getnewaddress()
        prox.name_update(name, '', add)
    except JSONRPCException, exc: 
        if exc.error['message'] == 'there are pending operations on that name':
            print 'Program is or was recently running. You need wait for this copy to work.'
        else:                                                     
            print 'Invalid name.'
            os.remove('keys.txt')
        exit()

    thr = Thread(target=check, args=[add])
    thr.daemon = True
    thr.start()    

    while 1:
        print raw_input('input> ')
