import sys
import socket
import os
import datetime
import time
import pyprctl

for cap in set(pyprctl.Cap):
    pyprctl.cap_effective.drop(cap)
    pyprctl.cap_permitted.drop(cap)

if len(sys.argv) == 2:
    if sys.argv[1] == "--server":
        SERVER_ADDRESS = 'localhost'

        # Can change this to any port 1-65535 (on many machines, ports <= 1024 are
        # restricted to privileged users)
        SERVER_PORT = 8888

        # Create the socket
        s = socket.socket()

        # Optional: this allows the program to be immediately restarted after exit.
        # Otherwise, you may need to wait 2-4 minutes (depending on OS) to bind to the
        # listening port again.
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to the desired address(es) and port. Note the argument is a tuple: hence
        # the extra set of parentheses.
        s.bind((SERVER_ADDRESS, SERVER_PORT))

        # How many "pending connections" may be queued. Exact interpretation of this
        # value is complicated and operating system dependent. This value is usually
        # fine for an experimental server.
        s.listen(5)

        print("Listening on address %s. Kill server with Ctrl-C" %
              str((SERVER_ADDRESS, SERVER_PORT)))

        # Now we have a listening endpoint from which we can accept incoming
        # connections. This loop will accept one connection at a time, then service
        # that connection until the client disconnects. Lather, rinse, repeat.
        while True:
            c, addr = s.accept()
            print("\nConnection received from %s" % str(addr))

            while True:
                data = c.recv(2048)
                if not data:
                    print("End of file from client. Resetting")
                    break

                # Decode the received bytes into a unicode string using the default
                data = data.decode()
                print("Received '%s' from client" % data)
                if data.startswith("time"):
                    format = data.replace("time", "")
                    if len(format) <= 30:
                        res = ""
                        date = datetime.datetime.now()
                        letters = "aAwdbmByYHlpMSfjUWcxX"
                        separators = " .,/-:"
                        if format != "":
                            for char in format:
                                if char in letters:
                                    res += f"%{char}"
                                elif char in separators:
                                    res += char
                                else:
                                    data = "Bad format input"
                                    data = data.encode()
                                    c.send(data)
                                    break
                            data = datetime.datetime.strftime(date, res)
                        else:
                            data = date.strftime("%B %dth %Y %H:%M:%S")
                    else:
                        data = "format to long"
                elif data == "exit":
                    break
                elif data == "-help":
                    data = "NAME\n\ttime\nSYNOPSIS\n\ttime [+FORMAT]\nDESCRIPTION\n\tDisplay current DateTime in a certain FORMAT."
                    data += "\nFORMAT\n\ta: Abbreviated weekday name \n\t"
                    data += "A : Full weekday name \n\t"
                    data += "w: Weekday as decimal number\n\t"
                    data += "d: Day of the month as a zero-padded decimal\n\t"
                    data += "b: Abbreviated month name\n\t"
                    data += "m: Month as a zero padded decimal number\n\t"
                    data += "B: Full month name\n\t"
                    data += "y: Year without century as a zero padded decimal number\n\t"
                    data += "Y: Year with century as a decimal number \n\t"
                    data += "H: Hour(24 hour clock) as a zero padded decimal number\n\t"
                    data += "l: Hour(12 hour clock) as a zero padded decimal number\n\t"
                    data += "p: Locale’s AM or PM\n\t"
                    data += "M: Minute as a zero padded decimal number\n\t"
                    data += "S: Second as a zero padded decimal number\n\t"
                    data += "f: Microsecond as a decimal number, zero padded on the left side\n\t"
                    data += "j: Day of the year as a zero padded decimal number\n\t"
                    data += "U: Week number of the year (Sunday being the first)\n\t"
                    data += "W: Week number of the year\n\t"
                    data += "c: Locale’s appropriate date and time representation\n\t"
                    data += "x: Locale’s appropriate date representation\n\t"
                    data += "X: Locale’s appropriate time representation\n"
                    data += "SEPARATORS\n\t. ,  / - :\n"
                    data += "EXAMPLE \n\ttime d/m/Y H:M:S \n\twill return for example 12/07/2022 08:27:41\n"
                    data += "NAME\n\texit\nSYNOPSYS\n\texit\nDESCRIPTION\n\tExit"
                else:
                    data = "Command not found"
                data = data.encode()

                # Send the modified data back to the client.
                c.send(data)

            c.close()
    elif sys.argv[1] == "--local":
        command = ""
        while command != "exit":
            command = input("Waiting for your input (\"-help\" for help): ")
            while command != "exit" and command != "-help" and not command.startswith(
                    "setDate") and not command.startswith("getTime"):
                print("Command not found")
                command = input("Waiting for your input(\"-help\" for help): ")
            if command == "exit":
                os.system('cls||clear')
                print("Closing... Goodbye")
            elif command == "-help":
                helpString = "NAME\n\tgetTime\nSYNOPSIS\n\tgetTime [+FORMAT]\nDESCRIPTION\n\tDisplay current DateTime in a certain FORMAT.\nFORMAT\n\ta: Abbreviated weekday name \n\tA : Full weekday name \n\tw: Weekday as decimal number\n\td: Day of the month as a zero-padded decimal\n\tb: Abbreviated month name\n\tm: Month as a zero padded decimal number\n\tB: Full month name\n\ty: Year without century as a zero padded decimal number\n\tY: Year with century as a decimal number \n\tH: Hour(24 hour clock) as a zero padded decimal number\n\tl: Hour(12 hour clock) as a zero padded decimal number\n\tp: Locale’s AM or PM\n\tM: Minute as a zero padded decimal number\n\tS: Second as a zero padded decimal number\n\tf: Microsecond as a decimal number, zero padded on the left side\n\tj: Day of the year as a zero padded decimal number\n\tU: Week number of the year (Sunday being the first)\n\tW: Week number of the year\n\tc: Locale’s appropriate date and time representation\n\tx: Locale’s appropriate date representation\n\tX: Locale’s appropriate time representation\nSEPARATORS\n\t. ,  / - :\nEXAMPLE \n\tgetTime d/m/Y H:M:S \n\twill return for example 12/07/2022 08:27:41\nNAME\n\tsetDate\nSYNOPSYS\n\tsetDate DATE\nDESCRIPTION\n\tSet the date and time of the current system\nDATE FORMAT\n\tyyyy/mm/dd hh:mm:ss\nEXAMPLE\n\tSet date to 14/12/2022 12:30:15 will be \"setDate 2022/12/14 12:30:15\"\nNAME\n\texit\nSYNOPSYS\n\texit\nDESCRIPTION\n\tExit"
                print(helpString)
            elif command.startswith("getTime"):
                try:
                    format = command.replace("getTime ", "")
                    format = command.replace("getTime", "")
                    if len(format) <= 30:
                        res = ""
                        date = datetime.datetime.now()
                        letters = "aAwdbmByYHlpMSfjUWcxX"
                        separators = " .,/-:"
                        if format != "":
                            for char in format:
                                if char in letters:
                                    res += f"%{char}"
                                elif char in separators:
                                    res += char
                                else:
                                    raise ValueError("Bad format input")
                            print(datetime.datetime.strftime(date, res))
                        else:
                            print(date.strftime("%B %dth %Y %H:%M:%S"))
                    else:
                        raise ValueError("format to long")
                except ValueError as exp:
                    print("Error", exp)
            elif command.startswith("setDate"):
                date = command.replace("setDate ", "")
                date = command.replace("setDate", "")
                date = date.replace(" ", "", 1)
                try:
                    if date != "":
                        if " " not in date:
                            raise ValueError("bad input")
                        else:
                            testDate = date.split(" ")[0]
                            testTime = date.split(" ")[1]
                            characters = "0123456789:/ "
                            for char in date:
                                if char not in characters:
                                    raise ValueError("bad input")
                            year, month, day = testDate.split('/')
                            isValidDate = True
                            try:
                                datetime.datetime(int(year), int(month), int(day))
                            except ValueError:
                                isValidDate = False
                            if not isValidDate:
                                raise ValueError("Input date is not valid")
                            hour, minute, seconde = testTime.split(':')
                            isValidTime = True
                            try:
                                datetime.time(int(hour), int(minute), int(seconde))
                            except ValueError:
                                isValidTime = False
                            if not isValidTime:
                                raise ValueError("Input time is not valid")
                            res = testDate + " " + testTime
                            try:
                                timestamp = time.mktime(time.strptime(res, "%Y/%m/%d %H:%M:%S"))
                                os.system("sudo python /usr/bin/setDatetime.py " + str(timestamp))
                            except OverflowError:
                                print("Erreur lors de la création du timestamp")
                            except:
                                print("Something else went wrong")
                    else:
                        print("Missing arguments")
                except ValueError as exp:
                    print("Error", exp)
    else:
        print("error bad argument")
elif len(sys.argv) == 1:
    print("Missing argument, expected 1 argument got 0")
else:
    print("error too many arguments")
