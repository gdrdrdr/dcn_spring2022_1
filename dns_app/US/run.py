# US
from flask import Flask, request, jsonify
from socket import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/fibonacci', methods=['GET'])
def read_request():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    num = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # 400
    if not(hostname) or not(fs_port) or not(num) or not(as_ip) or not(as_port):
        return jsonify("Parameters missing."), 400
    # 200
    else:
        client_socket = socket(AF_INET, SOCK_DGRAM)
        message = "TYPE={}\nNAME={}\n".format('A', hostname)
        client_socket.sendto(message.encode(), (as_ip, int(as_port)))
        temp_message, server = client_socket.recvfrom(2048)
        client_socket.close()
        temp_message = temp_message.decode()
        temp_str = temp_message.split('\n')
        name = temp_str[1].split('=')[1]
        value = temp_str[2].split('=')[1]
        # Create a GET Request
        url = "http://{}:{}/fibonacci?number={}".format(
            value, fs_port, num)
        return jsonify(url.json()), 200


app.run(host='0.0.0.0',
        port=8080,
        debug=True)
