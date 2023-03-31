from tkinter import messagebox
import threading
import socket
from tkinter import *

clients = []

def connetion_init(server_ip,server_port):
    global server
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((server_ip,server_port))
    server.listen()
    print("[+] Listening for connections .....")
    messagebox.showinfo("Server Management","Server is live and ready for connections")
    auth_window.destroy()
    main()

def broadcaster(message):
    for client in clients:
        client.send(message)

def communication_handler(client):
    while True:
        try:
            message = client.recv(4096)
            clients.remove(client)
            broadcaster(message)
            clients.append(client)
        except:
            clients.remove(client)
            broadcaster(f"[-] [{client_address}] left the conversation !!".encode('ascii'))

def main():
    while True:
        global client_address
        client,client_address = server.accept()
        print(f"[+] {client} connected to the server")
        client.send("[+] Connected to server !".encode('ascii'))

        broadcaster(f"[+] [{client_address}] Joined the conversation !!".encode('ascii'))
        clients.append(client)

        thread = threading.Thread(target=communication_handler,args=(client,))
        thread.start()

auth_window = Tk()

auth_window.configure(background="teal")
auth_window.minsize(width=318,height=135)

frame = LabelFrame(auth_window,borderwidth=5,height=300,width=400,
                   background="teal")
frame.grid(padx=5,pady=5)

ip_label = Label(frame,text="Server Address",background="teal",font=("Andalus", 10, "bold"))
port_label = Label(frame,text="Server Port",background="teal",font=("Andalus", 10, "bold"))

ip_label.grid(column=0,row=2)
port_label.grid(column=0,row=3)

ip_entry = Entry(frame,justify=CENTER,width=30,font=("Andalus", 8, "bold"),relief="sunken",borderwidth=2)
port_entry = Entry(frame,justify=CENTER,width=30,font=("Andalus", 8, "bold"),relief="sunken",borderwidth=2)

ip_entry.grid(column=2,row=2,pady=10,padx=5)
port_entry.grid(column=2,row=3,pady=10,padx=5)

connect_button = Button(frame,text="Host",width=10,background="red",
                        command=lambda :connetion_init(str(ip_entry.get()),int(port_entry.get())))
connect_button.grid(column=2,row=4,pady=5)

auth_window.mainloop()
