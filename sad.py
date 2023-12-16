import socket
import threading

def process_client(client):
    while True:
        data = client.recv(1024)
        if not data:
            break
        elif b'GET' in data and b'www.facebook.com' in data:
            client.sendall(b'HTTP/1.1 403 Forbidden\r\n\r\n')
            break
        else:
            client.sendall(data)
    client.close()

def run_proxy_server(port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen(5)
    print('Starting proxy server on port %s' % port)
    while True:
        client, addr = server.accept()a
        print('Connection from %s:%s' % addr)
        client_handler = threading.Thread(target=process_client, args=(client,))
        client_handler.start()

if __name__ == '__main__':
    run_proxy_server()