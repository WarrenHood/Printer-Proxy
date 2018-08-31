import socket
import threading
def reply_handler(server,client):
        while True:
                try:
                        data = b""
                        leng = 4096
                        while leng == 4096:
                                dat = server.recv(4096)
                                leng = len(dat)
                                data += dat
                                print(dat.decode().strip(),end="")
                        print("")
                        client.send(data)
                except:
                        return
def print_handler(client):
        try:
                host = "192.168.122.10" 
                port = 9100
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.connect((host, port))
        except:
                print("Some error occured...")
        reply_th = threading.Thread(target=reply_handler,args=(sock,client))
        reply_th.start()
        while True:
                data = b"";
                recv_len = 1
                while recv_len:
                        dat = ""
                        dat = client.recv(1024*1024)
                        data += dat
                        recv_len = len(dat)
                        #print(dat,end="")
                print(data)
                try:
                        sock.send(data)
                        print(data)
                except:
                        print("Failed to send some data")
listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
printer_ip = "192.168.122.10"
try:
        user_in = str(input("Enter printer IP(default:192.168.122.10):")).strip()
        if len(user_in) > 0 and len(user_in.split(".")) == 4:
                printer_ip = user_in
        elif user_in == "":
                print("Using default printer ip")
        else:
                print("You entered an invalid ip address...Using default")
except:
        print("Using default printer ip")
ip_to_use = str(input("Enter ip to bind to(Default: 127.0.0.1):"))
if ip_to_use == "":
        ip_to_use = "127.0.0.1"
try:
        port_to_use = int(input("Enter port to use(default:9100):"))
except:
        port_to_use = 9100
print("Binding to",ip_to_use+":"+str(port_to_use))
try:
        listener.bind((ip_to_use,port_to_use))
        listener.listen(100)
except:
        input("Could not bind to specified address. Press enter to exit...")
while True:
        client,addr = listener.accept()
        print("Got connection from",addr[0]+":"+str(addr[1]))
        data = b"";
        recv_len = 0
        data = client.recv(1024*100)
        recv_len = len(data)
        if len(data) > 0:
                print("Just received",recv_len," bytes from client")
        while recv_len > 0:
                current_data = client.recv(1024*100)
                recv_len = len(current_data)
                data += current_data
                print("Just received",recv_len," bytes from client")
        if len(data) > 0:
                print("Total bytes received:",len(data))
                print("Printing now... Do not close the program!")
                printer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                try:
                        printer.connect((printer_ip,9100))
                        try:
                                printer.send(data)
                                print("Data has been sent to printer. You may exit now or print more")
                        except:
                                print("Something went wrong while sending data to printer...")
                        printer.close()
                        client.close()
                        del data
                        printer = 0
                except:
                        print("An error occured while connecting to printer")
