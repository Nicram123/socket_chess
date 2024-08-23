import socket
import threading 
import pickle 

PORT = 5010
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 70
FORMAT = 'utf-8'
clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 , TCP
server.bind(ADDR)

def handle_client(conn):
  connected = True
  while connected:
    msg_length = conn.recv(HEADER).decode(FORMAT) # '230  helo' * 5 bajty
    if msg_length:
      msg_length = int(msg_length)
      data = b''
    while len(data) < msg_length:
      packet = conn.recv(msg_length - len(data))
      if not packet:
        break
      data += packet
    board = pickle.loads(data) # deserializacja objektu 
    if board == DISCONNECT_MESSAGE:
      connected = False
    else:
      send_to_other_clients(board, conn)
  conn.close()
  
def send_to_other_clients(board, sender_conn):
  serialized_data = pickle.dumps(board) # serializacja objektu fo bajtow 
  data_header = f'{len(serialized_data):<{HEADER}}'.encode(FORMAT) # '20   '
  for client in clients:
    if client != sender_conn:
      try:
        client.send(data_header + serialized_data)
      except Exception as e:
        print(f"[ERROR] Sending to client: {e}")
        clients.remove(client)
        
    

def start():
  server.listen()
  while True:
    conn, addr = server.accept() # obj klienta, (IP, PORT)
    clients.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    

start()


