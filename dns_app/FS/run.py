# FS
from flask import Flask, request, jsonify
from socket import *

app = Flask(__name__)


def fib_fun(num):
    if num <= 1:
        return 0
    elif num == 2:
        return 1
    else:
        return fib_fun(num-1) + fib_fun(num-2)


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/register', methods=['GET', 'PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')
    if not(hostname) or not(ip) or not(as_ip) or not(as_port):
        return jsonify("Parameters missing."), 400
    else:
        client_socket = socket(AF_INET, SOCK_DGRAM)
        message = "TYPE={}\nNAME={}\nVALUE={}\nTTL={}\n".format(
            'A', hostname, ip, 10)
        client_socket.sendto(message.encode(), (as_ip, int(as_port)))
        temp_message, server = client_socket.recvfrom(2048)
        client_socket.close()
        if temp_message.decode() == 'Success':
            return jsonify('Success'), 201
        else:
            return jsonify('Failed'), 500


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    num = request.args.get('number')
    if not num.isnumeric():
        return jsonify("Parameter invalid."), 400
    return jsonify(fib_fun(int(num))), 200


app.run(host='0.0.0.0',
        port=9090,
        debug=True)
