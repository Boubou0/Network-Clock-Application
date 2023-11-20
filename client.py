#!/usr/bin/env python
# !/
import socket
import os
import pyprctl

for cap in set(pyprctl.Cap):
    pyprctl.cap_effective.drop(cap)
    pyprctl.cap_permitted.drop(cap)

os.system('cls||clear')
# Note that the server may listen on a specific address or any address
# (signified by the empty string), but the client must specify an address to
# connect to. Here, we're connecting to the server on the same machine
# (127.0.0.1 is the "loopback" address).
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8888

os.system('cls||clear')
# Create the socket
c = socket.socket()

# Connect to the server. A port for the client is automatically allocated
# and bound by the operating system
c.connect((SERVER_ADDRESS, SERVER_PORT))

try:
    input = raw_input
except NameError:
    pass
print("Connected to " + str((SERVER_ADDRESS, SERVER_PORT)))
while True:
    try:
        data = input("Enter a Command(enter -help for help): ")
    except EOFError:
        print("\nOkay. Leaving. Bye")
        break

    if not data:
        print("Can't send empty string!")
        print("Ctrl-D [or Ctrl-Z on Windows] or enter command 'exit' to exit")
        continue

    # Convert string to bytes.
    data = data.encode()

    # Send data to server
    c.send(data)

    # Receive response from server
    data = c.recv(2048)
    if not data:
        print("Server abended. Exiting")
        break

    # Convert back to string for python3
    data = data.decode()

    print("Got this string from server:")
    print(data + '\n')

c.close()
