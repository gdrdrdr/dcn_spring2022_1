# AS
from socket import *

port_num = 53533
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', port_num))
persistent = {}

# Listen for request
while True:
    message, client_address = server_socket.recvfrom(2048)
    message = message.decode()
    print("Message is:", message)
    print(message)
    # Registration
    if 'VALUE' in message:
        print("Registration")
        temp_str = message.split('\n')
        name = temp_str[1].split('=')[1]
        value = temp_str[2].split('=')[1]
        persistent[name] = value
        print("NAME = {}\nVALUE = {}".format(name, value))
        response = 'Success'
        server_socket.sendto(response.encode(), client_address)
    # DNS Query
    else:
        print("DNS Query")
        temp_str = message.split('\n')
        name = temp_str[1].split('=')[1]
        print("NAME = {}".format(name))
        if name in persistent:
            response = "TYPE={}\nNAME={}\nVALUE={}\nTTL={}\n".format(
                'A', name, persistent[name], 10)
            server_socket.sendto(response.encode(), client_address)
        else:
            print("Invalid")
