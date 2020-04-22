#   Heights sockets Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017

import socket
import os
from PIL import ImageGrab
import glob
import shutil
import subprocess

IP = '0.0.0.0'
PORT = 8421


def receive_client_request(client_socket):
    """Receives the full message sent by the client

    Works with the protocol defined in the client's "send_request_to_server" function

    Returns:
        command: such as DIR, EXIT, SCREENSHOT etc
        params: the parameters of the command

    Example: 12DIR c:\cyber as input will result in command = 'DIR', params = 'c:\cyber'
    """
    rec = client_socket.recv(1024)
    length = int(rec[0:3])
    rec = rec[3:3+length]
    arr = rec.split(" ")
    if len(arr) >= 2:
        list_command = arr[0]
        command = arr[0]
        params = " ".join(arr[1:])
        return command, params
    else:
        command = str(arr[0])
        return command, None


def check_client_request(command, params):
    """Check if the params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        error_msg: None if all is OK, otherwise some error message
    """
    vaild = True
    error = None
    if command == 'SEND_FILE' or command == 'DIR' or command == 'DELETE' or command == 'EXECUTE':
        if not os.path.exists(params):
            vaild = False
            error = "The path is not exist"
    elif command == 'COPY':
        list1 = params.split(" ")
        if (not os.path.exists(list1[0])) or (not os.path.exists(list1[1])):
            vaild = False
            error = "The path is not exist"

    return vaild, error


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory

    Returns:
        response: the requested data
    """
    if command == 'TAKE_SCREENSHOT':
        ImageGrab.grab().save("screen_capture.png", "PNG")
        with open('screen_capture.png', 'rb') as input_file:
            data = input_file.read()
            return data
    if command == 'DIR':
        files_list = glob.glob(params+"/*")
        return str(files_list)
    elif command == 'COPY':
        path_list = params.split(" ")
        shutil.copy(path_list[0], path_list[1])
        return 'The copying process was performed'
    elif command == 'SEND_FILE':
        with open(params, 'rb') as input_file:
            data = input_file.read()
            return data
    elif command == 'DELETE':
        os.remove(params)
        return "The deletion process was performed"
    elif command == 'EXECUTE':
        subprocess.call(params)
        return "The running process was performed"
    elif command == 'EXIT':
        return 'EXIT'


def send_response_to_client(response, client_socket):
    """Create a protocol which sends the response to the client

    The protocol should be able to handle short responses as well as files
    (for example when needed to send the screenshot to the client)
    """
    while len(response) >= 1024:
        client_socket.send(response[:1024])
        response = response[1024:]
    client_socket.send(response + '//end//')


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()

    # handle requests until user asks to exit
    done = False
    while not done:
        command, params = receive_client_request(client_socket)
        valid, error_msg = check_client_request(command, params)
        if valid:
            response = handle_client_request(command, params)
            send_response_to_client(response, client_socket)
        else:
            send_response_to_client(error_msg, client_socket)

        if command == 'EXIT':
            done = True

    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
