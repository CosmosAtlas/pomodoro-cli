#!/usr/bin/env python3
# Client to communicate with the server

import socket
import sys

if (len(sys.argv) != 2 or sys.argv[1] not in ['start', 'pause', 'resume', 'stop', 'exit', 'print', 'inquiry']):
    print("Require 1 command from: start, pause, resume, stop, exit, print, inquiry")
    exit(0)

COMMAND = sys.argv[1]

HOST = '127.0.0.1'
PORT = 12121

# Connect to server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        s.sendall(COMMAND.encode())
        data = s.recv(1024)
        print(data.decode())
    except Exception as e:
        print("Pomodoro server not running...")
# Parse commands and act accordingly

# Send comments
