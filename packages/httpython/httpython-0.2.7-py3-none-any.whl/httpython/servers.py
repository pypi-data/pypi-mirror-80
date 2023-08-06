import ssl
import socket
import threading

from . import RequestMethod
from .requests import Request


# Server class
class Server:
    def __init__(self, host, port, filedir):
        self._host = host
        self._port = port
        self.filedir = filedir

    @property
    def host(self):
        return self._host
    
    @host.setter
    def host_set(self, newhost):
        if not isinstance(newhost, str):
            raise Exception("Placeholder")
        self._host = newhost
        
    @host.deleter
    def host_delete(self):
        raise Exception("You cannot delete the host attribute")
    
    @property
    def port(self):
        return self._port
    
    @port.setter
    def port_set(self, newport):
        if not isinstance(newport, int):
            raise Exception("Placeholder")
        self._port = newport

    @port.deleter
    def port_delete(self):
        raise Exception("You cannot delete the port attribute")

    def method(self, method: RequestMethod=RequestMethod.ANY, host="*", route="*"):
        def wrapper(function):
            if method not in self.functions:
                self.functions[method] = {}
                
            if host not in self.functions[method]:
                self.functions[method][host] = {}
            self.functions[method][host].update({route: function})
        return wrapper

    def _call_methods(self, method: RequestMethod, route, request):
        host = request.headers["Host"] if "Host" in request.headers else "*"
        
        if method not in self.functions:
            method = RequestMethod.ANY
            
        if method in self.functions:
            if host not in self.functions[method]:
                host = "*"
            if route in self.functions[method][host]:
                return self.functions[method][host][route](request, self)
            elif "*" in self.functions[method][host]:
                return self.functions[method][host]["*"](request, self)
        return Request.response(502, "Not Implemented", {"Server": "Webpy/2.0", "Connection": "closed"})


# HTTP Server class
class HTTP_Server(Server):
    def __init__(self, host, port, filedir):
        super().__init__(host, port, filedir)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.functions = {}
        self.threads = []

    def handler(self, connection, address):
        data = b""
        length = None
        ended = False
        body = b""
        while True:
            incoming = connection.recv(1024)
            data += incoming
            
            for line in data.split(b"\r\n"):
                if line.startswith(b"Content-Length:"):
                    length = int(line.replace(b"Content-Length: ", b"").replace(b"\r\n", b""))

            
            if b"\r\n\r\n" in data and length:
                body += b"\r\n\r\n".join(data.split(b"\r\n\r\n")[1:])

            if b"\r\n\r\n" in data and not length: break
                
            if not incoming or incoming == b"" or len(body) >= length: break
        x = Request.from_request(data, address)
        response = self._call_methods(x.method, x.path, x)
        connection.send(response)
        connection.close()
    def run(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(50)
        while True:
            conn, addr = self.socket.accept()
            thread = threading.Thread(target=self.handler, args=(conn, addr))
            self.threads.append(thread)
            thread.start()

# HTTPS Server class
class HTTPS_Server(Server):
    def __init__(self, host, port, filedir, certfile, keyfile):
        super().__init__(host, port, filedir)
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.functions = {}
        self.threads = []

    def handler(self, connection, address):
        data = b""
        length = None
        ended = False
        body = b""
        while True:
            incoming = connection.read()
            data += incoming
            
            for line in data.split(b"\r\n"):
                if line.startswith(b"Content-Length:"):
                    length = int(line.replace(b"Content-Length: ", b"").replace(b"\r\n", b""))

            
            if b"\r\n\r\n" in data and length:
                body += b"\r\n\r\n".join(data.split(b"\r\n\r\n")[1:])

            if b"\r\n\r\n" in data and not length: break
                
            if not incoming or incoming == b"" or len(body) >= length: break
            
        try:
            x = Request.from_request(data, address)
        except ValueError:
            response = Request.response(502, "Not Implemented", {"Server": "Webpy/2.0", "Connection": "closed"})
        else:
            response = self._call_methods(x.method, x.path, x)
        connection.send(response)
        connection.shutdown(socket.SHUT_RDWR)

    def run(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(50)
        while True:
            try:
                conn, addr = self.socket.accept()
                conn = self.context.wrap_socket(conn, server_side=True)
                thread = threading.Thread(target=self.handler, args=(conn, addr))
                self.threads.append(thread)
                thread.start()
            except:
                pass
