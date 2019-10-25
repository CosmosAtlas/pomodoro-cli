#!/usr/bin/env python3
# Server to keep track of a pomodoro timer

import socket
import signal
import sys
import pomodoro
from time import sleep

HOST = '127.0.0.1'
PORT = 12121


def int_handler(signal_received, frame):
    # Handle clean up here
    print('\rSIGINT or <C-c> detected, exiting gracefully!')
    sys.exit(0)


signal.signal(signal.SIGINT, int_handler)

pomo = pomodoro.Pomodoro(30, 25)


def process(data, pomo):
    if data == b'start':
        return(pomo.process_start())
    if data == b'pause':
        return(pomo.process_pause())
    if data == b'resume':
        return(pomo.process_resume())
    if data == b'stop':
        return(pomo.process_stop())
    if data == b'print':
        return(pomo.process_print())
    if data == b'exit':
        print("Exit command received")
        return(0)
    if data == b'inquiry':
        return(pomo.process_inquiry())
    else:
        return(b'unknown command')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()
s.settimeout(0.1)

while True:
    sleep(0.1)
    pomo.update()
    try:
        conn, addr = s.accept()
    except socket.timeout as e:
        err = e.args[0]
        if err == 'timed out':
            #  print('recieved time out, retry later')
            continue
        else:
            print("Error: ", e)
            s.close()
            sys.exit(1)
    except socket.error as e:
        print("Error: ", e)
        s.close()
        sys.exit(1)
    else:
        data = conn.recv(1024)
        if not data:
            continue
        proc = process(data, pomo)
        print("Server returns:", proc)
        if (proc == 0):
            conn.sendall(b"Exiting...")
            print('Exiting..')
            s.close()
            sys.exit(0)
        conn.sendall(proc.encode())
