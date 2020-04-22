#   Heights sockets Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017


import socket
import os

IP = '127.0.0.1'
PORT = 8421


def valid_request(request):
    """Check if the request is valid (is included in the available commands)

    Return:
        True if valid, False if not
    """
    if 'EXIT' == request.upper():
        return True
    # Checks if the input line is just EXIT
    else:
        #Checks if there is a valid command and if so, the number of variables is correct
        list1 = request.split(" ")
        if 'SEND_FILE' == list1[0] and len(list1) == 2:
            return True
        elif 'TAKE_SCREENSHOT' == list1[0] and len(list1) == 2 and os.path.exists(list1[1]):
            return True
        elif 'DIR' == list1[0] and len(list1) == 2:
            return True
        elif 'DELETE' == list1[0] and len(list1) == 2:
            return True
        elif 'EXECUTE' == list1[0] and len(list1) == 2:
            return True
        elif 'COPY' == list1[0] and len(list1) == 3:
            return True
        else:
            return False


def send_request_to_server(my_socket, request):
    """Send the request to the server. First the length of the request (2 digits), then the request itself

    Example: '04EXIT'
    Example: '12DIR c:\cyber'
    """
    #Returns three digits before the recorded input line
    length = len(request)
    if length < 10:
        send = '00' + str(length) + request
    elif length < 100:
        send = '0' + str(length) + request
    else:
        send = str(length) + request
    my_socket.send(send)


def handle_server_response(my_socket, request):
    """Receive the response from the server and handle it, according to the request

    For example, DIR should result in printing the contents to the screen,
    while SEND_FILE should result in saving the received file and notifying the user
    """
    if not "EXIT" in request:
        data = my_socket.recv(1024)
        while '//end//' not in data:
            data = data + my_socket.recv(1024)
        data = data.replace('//end//', '')
        #Get the data
        if 'SEND_FILE' in request:
            params = "".join(request.split()[1:])
            type_of_file = "." + str(params.split(".")[len(params.split("."))-1])
            #Get the type of the file (like - .txt , .java , .py) 
            i = 1
            while (os.path.exists('new_file' + str(i) + type_of_file)):
                i += 1
            with open('new_file' + str(i) + type_of_file, 'wb') as input_file:
                input_file.write(data)
            #Checks if there is a file with the name new_file1 and so on and then creates the following file
        elif 'DIR' in request:
            print data
            #Prints the server's response line
        elif 'DELETE' in request:
            print data
            #Prints the server's response line
        elif 'COPY' in request:
            print data
            #Prints the server's response line
        elif 'EXECUTE' in request:
            print data
            #Prints the server's response line
        elif 'TAKE_SCREENSHOT' in request:
            list_path = request.split()
            path = str(list_path[1])
            i = 1
            while (os.path.exists(path + '/screenshot_file' + str(i) + '.png')):
                i += 1
            with open(path + '/screenshot_file' + str(i) + '.png', 'wb') as input_file:
                input_file.write(data)
            #Checks if there is a file with the name screenshot_file1 and so on and then creates the following file



def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_FILE\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    done = False
    # loop until user requested to exit
    while not done:
        request = raw_input("Please enter command:\n")
        if valid_request(request):
            send_request_to_server(my_socket, request)
            handle_server_response(my_socket, request)
            if request == 'EXIT':
                done = True
    my_socket.close()


if __name__ == '__main__':
    main()
