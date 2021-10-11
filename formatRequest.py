import socket, sys
from os import error
from urllib.parse import urlparse


def formatGet(args):
    headers = {}
    for pairs in args.HEADERS:
        k, v = pairs.split(":")
        headers[k] = v
    url = args.url
    
    parsedUrl = urlparse(url)
    path = "/" if parsedUrl.path == "" else parsedUrl.path
    query = parsedUrl.query
    hostName = parsedUrl.hostname
    port = 80 if parsedUrl.port is None else parsedUrl.port
    
    uri = "{}?{}".format(path, query) if query else path
    headers.setdefault("Host", hostName)
    headers.setdefault("User-Agent", "Concordia-HTTP/1.0")
    getRequest = "GET {} HTTP/1.0".format(uri)
    header = "".join([f'{key}:{value}\r\n' for key, value in headers.items()])
   
    request = "\r\n".join((getRequest, header))
    request += "\r\n"
 
    connection(args, hostName, port, request)

def connection(args, hostName, port, request):
    sock = socket.create_connection((hostName, port))
    # request = "POST /post HTTP/1.0\r\nContent-Type:application/json\r\nHost:httpbin.org\r\nUser-Agent:Concordia-HTTP/1.0\r\nContent-Length:15\r\n\r\n{Assignment: 1}"
    #request = "POST /post HTTP/1.0\r\nContent-Type:application/json\r\nHost:httpbin.org\r\nUser-Agent:Concordia-HTTP/1.0\r\nContent-Length:15\r\n\r\n{Assignment: 1}"
    sock.sendall(request.encode("UTF-8"))
    
    response = sock.recv(1024, socket.MSG_WAITALL)
    response = response.decode("UTF-8")
    
    if args.VERBOSE:
        print(response)  
    else:
        responseBody = response.split("\r\n\r\n")[1]
        print(responseBody)
    
        

def formatPost(args):
    if args.DATA and args.FILE:
        print("Invalid command. Post should have either -d or -f but not both.")
        return
    if args.FILE:
        try:
            with open(args.FILE, mode="r") as f:
                data = f.read()
        except FileNotFoundError:
            print("File not found")
            return
    elif args.DATA:
        data = args.DATA
    # print(data)
    headers = {}
    for pairs in args.HEADERS:
        k, v = pairs.split(":")
        headers[k] = v
    url = args.url
    parsedUrl = urlparse(url)
    path = "/" if parsedUrl.path == "" else parsedUrl.path
    query = parsedUrl.query
    hostName = parsedUrl.hostname
    port = 80 if parsedUrl.port is None else parsedUrl.port
    uri = "{}?{}".format(path, query) if query else path
    headers.setdefault("Host", hostName)
    headers.setdefault("User-Agent", "Concordia-HTTP/1.0")
    headers.setdefault("Content-Length", str(len(data)))
    postRequest = "POST {} HTTP/1.0".format(uri)
    header = "".join([f'{key}:{value}\r\n' for key, value in headers.items()])
    request = "\r\n".join((postRequest, header))
    request += "\r\n"
    # print(repr(request))
    if data != "":
        request += data 
    # print(repr(request))
    connection(args, hostName, port, str(request))