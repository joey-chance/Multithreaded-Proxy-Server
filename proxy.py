import sys
import socket
import time
import _thread as thread
import threading

BUFFER_SIZE = 100000
def main():

    if len(sys.argv) != 4:
        print("Invalid arguments. Usage: python3 proxy.py <port> <image-flag> <attack-flag>")
        return
    else:
        proxy_port = int(sys.argv[1])
        substitute = bool(int(sys.argv[2]))
        attacker_mode = bool(int(sys.argv[3]))

    proxy_host = ""

    try:
        listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_sock.bind((proxy_host, proxy_port))
        listen_sock.listen()
    except socket.error:
        if listen_sock:
            listen_sock.close()
        print ("Could not open socket")
        sys.exit(1)

    sizes = {}
    mutex = threading.Lock()
    while 1:
        client, client_addr = listen_sock.accept()
        thread.start_new_thread(thread_func, (client, substitute, attacker_mode, sizes, mutex))
        
    listen_sock.close()

def thread_func(client, substitute, attacker_mode, sizes, mutex):

    request = client.recv(BUFFER_SIZE)


    headers = request.split(b'\r\n')
    # for line in range(len(headers)):
    #     print(headers[line])
    # print("\n")
    get_line = headers[0]
    if get_line[:4] != b'GET ':
        client.close()
        return

    url = get_line.split(b' ')[1]
    # print("url:", url)
    pos_http = url.find(b'://')

    if pos_http != -1:
        url = url[(pos_http+3):]
        
    pos_port = url.find(b':')

    webserver_end = url.find(b'/')
    if webserver_end == -1:
        webserver_end = len(url)

    webserver = ""
    server_port = -1
    if pos_port == -1 or webserver_end < pos_port:
        server_port = 80
        webserver = url[:webserver_end]
    else:
        server_port = int((url[(pos_port+1):])[:webserver_end-pos_port-1])
        webserver = url[:pos_port]
    
    referer = find_referer(headers)
    bytes = 0
    try:
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        serv_sock.connect((webserver, server_port))
        serv_sock.send(request)
        serv_sock.settimeout(2)
        if attacker_mode:
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 22\r\n\r\nYou are being attacked"
            bytes = sys.getsizeof(response)
            client.send(response.encode())
        else:
            ctr = 1
            
            while 1:
                response = serv_sock.recv(BUFFER_SIZE)
                if len(response) > 0:
                    if substitute and ctr == 1 and response.split(b'\r\n\r\n')[0].find(b'Content-Type: image/') != -1:
                        serv_sock.close()
                        request = b'GET http://ocna0.d2.comp.nus.edu.sg:50000/change.jpg HTTP/1.1\r\nHost: ocna0.d2.comp.nus.edu.sg:50000\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\n\r\n'
                        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        serv_sock.connect((b'ocna0.d2.comp.nus.edu.sg', 50000))
                        serv_sock.send(request)
                        serv_sock.settimeout(2)
                        while 1:
                            response = serv_sock.recv(BUFFER_SIZE)
                            if len(response) > 0:
                                if ctr == 1:
                                    bytes = sys.getsizeof(response.split(b'\r\n\r\n')[1])
                                else:
                                    bytes += sys.getsizeof(response)
                                client.send(response)
                                ctr += 1
                            else:
                                break
                        break
                    else:
                        if ctr == 1:
                            bytes = sys.getsizeof(response.split(b'\r\n\r\n')[1])
                        else:
                            bytes += sys.getsizeof(response)
                        ctr += 1
                        client.send(response)
                else:
                    break
    except socket.timeout:
        if serv_sock:
            serv_sock.close()
        if client:
            client.close()
        sys.exit(1)
    except socket.error:
        response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\nContent-Length: 15\r\n\r\n400 Bad Request"
        bytes = sys.getsizeof(response)
        client.send(response.encode())
        if serv_sock:
            serv_sock.close()
        if client:
            client.close()
        sys.exit(1)
    finally:
        if attacker_mode:
            if referer == None:
                print("http://"+url.decode()+", "+ str(bytes))
        else:
            if referer != None:
                mutex.acquire()
                sizes[referer] += bytes
                mutex.release()
                if serv_sock:
                    serv_sock.close()
            else:
                mutex.acquire()
                sizes[url] = bytes
                mutex.release()
                if serv_sock:
                    serv_sock.close()
                time.sleep(10)
                print("http://"+url.decode()+", "+ str(sizes[url]))
        if client:
                client.close()

def find_referer(headers):
    for line in range(len(headers)):
        if headers[line][:9] == b'Referer: ':
            return headers[line][16:]
        else:
            continue
    return None

if __name__ == '__main__':
    main()
