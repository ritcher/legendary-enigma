import socket
from socket import (
    _intenum_converter,
    AddressFamily,
    SocketKind
)

from _config import dns_cache

af = AddressFamily.AF_INET
socktype = SocketKind.SOCK_STREAM
proto = 6
canonname = ""

def getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    
    sa = (dns_cache[host], port)
    
    addrlist = [(
        _intenum_converter(af, AddressFamily),
        _intenum_converter(socktype, SocketKind),
        proto, canonname, sa
    )]
    
    return addrlist

socket.getaddrinfo = getaddrinfo
