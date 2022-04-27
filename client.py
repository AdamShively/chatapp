import socket
import threading
import PySimpleGUI as sg
import sys

FORMAT = 'utf-8'
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, 5050)
chat_name = None
recieved = []

def try_connecting(client):
    while True:
        try:
            client.connect(ADDR)
            chat_name = sg.popup_get_text('Screen name', 'Please input screen name')
            client.send(chat_name.encode(FORMAT))
            break
        except:
            error_window()
            
def error_window():
    layout = [[sg.Text('No connection could be made at this time.')],
            [sg.Button('Try Again?'), sg.Button('Exit')]]

    window = sg.Window('ERROR!', layout)
    event, _ = window.read()
    if event == ('Try Again?'):
        window.close()
        
    elif event in (sg.WIN_CLOSED, 'Exit'):
        window.close()
        sys.exit() 

def client_receive(window, client):
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            recieved.append(message)
            window['-RECIEVED-'].update(recieved)
        except:
            client.close()
            break

def client_send(client, msg):
    client.send(msg.encode(FORMAT))

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try_connecting(client)
    sg.theme('DarkBlue')

    layout = [
                [sg.Listbox(('',),size=(80, 5), key='-RECIEVED-')],
                [sg.Text('Send a message'), sg.Multiline(key='-SENDING-')],
                [sg.Button('Send'), sg.Button('Exit')],
                ]

    window = sg.Window('Client', layout,  keep_on_top=True, finalize=True)

    receive_thread = threading.Thread(target=client_receive, args=(window, client))
    receive_thread.start()

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            client_send(client, "_QUIT_")
            break

        if event in ('Send',):
                client_send(client, values['-SENDING-'])
                window['-SENDING-'].update("")

    window.close()

if __name__ == "__main__":
    main()
