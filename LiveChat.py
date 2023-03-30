#Calling of the libraries to be used in the program
from tkinter import ttk
from tkinter import *
import threading
import socket

#Start of the authentication windows *Username
#                                    *Server_ip_Address
#                                    *Server_port_Address
auth_window = Tk()
auth_window.configure(background="teal")
auth_window.minsize(width=318,height=175)
auth_window.maxsize(width=318,height=175)

frame = LabelFrame(auth_window,borderwidth=5,height=300,width=400,
                   background="teal")
frame.grid(padx=5,pady=5)

username_label = Label(frame,text="Username",background="teal",font=("Andalus", 10, "bold"))
ip_label = Label(frame,text="Server Address",background="teal",font=("Andalus", 10, "bold"))
port_label = Label(frame,text="Server Port",background="teal",font=("Andalus", 10, "bold"))

username_label.grid(column=0,row=1)
ip_label.grid(column=0,row=2)
port_label.grid(column=0,row=3)

username_entry = Entry(frame,justify=CENTER,width=30,font=("Andalus", 8, "bold"),relief="sunken",borderwidth=2)
ip_entry = Entry(frame,justify=CENTER,width=30,font=("Andalus", 8, "bold"),relief="sunken",borderwidth=2)
port_entry = Entry(frame,justify=CENTER,width=30,font=("Andalus", 8, "bold"),relief="sunken",borderwidth=2)

username_entry.grid(column=2,row=1,pady=10,padx=5)
ip_entry.grid(column=2,row=2,pady=10,padx=5)
port_entry.grid(column=2,row=3,pady=10,padx=5)

def cred_get():
    global ip_address,port_address,username
    ip_address = ip_entry.get()
    port_address = port_entry.get()
    username = username_entry.get()
    auth_window.destroy()

connect_button = Button(frame,text="Connect",width=10,background="red",command=cred_get)
connect_button.grid(column=2,row=4,pady=5)

auth_window.mainloop()

#Connection to the server using the given credentials
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((str(ip_address),int(port_address)))

#Start of the second body were we read and enter messages to send over to the rest of clients
root = Tk()
root.configure(background="teal")
theme = ttk.Style()
theme.theme_use('classic')

def send_message():
    user_message = message_entry.get()
    message_entry.delete(0,END)
    message_area.insert(END,"\n"+"You: "+user_message+"\n")
    user_message = username + " : " + user_message
    client.send(user_message.encode('ascii'))

def receive_messsage():
    while True:
        user2_message = client.recv(4096).decode('ascii')
        message_area.insert(END, "\n"+user2_message)

root.title("Secret Talkie")
root.minsize(width=520,height=555)
root.maxsize(width=520,height=555)

message_frame = LabelFrame(root,height=600,width=650,borderwidth=5,background="teal")
message_frame.grid(pady=5,padx=5)

message_area = Text(message_frame,height=30,width=70,borderwidth=2, font=("Andalus", 10, "bold"),
                    foreground="black",background="white")
message_area.grid(padx=2,pady=2)

input_frame = LabelFrame(root,height=45,width=425,borderwidth=5,background="teal")
input_frame.grid(padx=2,pady=2)

message_entry = Entry(input_frame,borderwidth=2,relief="sunken",width=58,font=("Andalus", 10, "bold"),
                      foreground="black",background="grey")
message_entry.grid(column=0,row=1,padx=2,pady=2)

submit_button = Button(input_frame,text="Send",command=send_message,
                       width=10,background="green",foreground="yellow")
submit_button.grid(column=2,row=1)

recvThread = threading.Thread(target=receive_messsage)
recvThread.daemon=True
recvThread.start()

root.mainloop()
