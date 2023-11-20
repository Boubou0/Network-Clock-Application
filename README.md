# Network Clock Application
This is a secure code project realized in Python during my month-long course in Prague at the Czech Technical University.

## Instruction
Develop a Network Clock (NC) application with the following characteristics:

NC is run as a standard application. It displays the current date and time to the interactive (logged-on) user; the user may specify the exact format of the displayed value by setting a format string interactively. It’s acceptable to only update the display on request.
Additionally, NC listens for communications on a TCP port number defined in a configuration file (or a registry key). A remote user can connect to this port and request the current date and time in a specified format.
The interactive user (but not a remote one) may also set the date/time.
Note that since the application is accessible from the internet, there are many potential attackers waiting to exploit any bug. For this reason, the application should be written with security in mind; particularly, it will use as low privileges as possible.
