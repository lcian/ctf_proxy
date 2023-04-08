from src.stream import Stream, TCPStream, HTTPStream
from src.db_manager import DbManager
import string

################################################################################
# HTTP

def curl(self, stream: HTTPStream):
    """block curl user-agent"""
    message = stream.current_http
    return "curl" in message.headers.get("user-agent")

def username(self, stream: HTTPStream):
    """
    block usernames longer than 10 characters for register endpoint
    """
    message = stream.current_http
    if "register" in message.url and "POST" in message.method:
        username = message.parameters.get("username")
        if len(username) > 10:
            return True
    else:
        return False
    
def block_leak(self, stream: HTTPStream):
    """
    if responding to /home request and a flag is in the response, block
    only valid for _out modules
    """
    message = stream.current_http
    previous_message = stream.previous_http
    return "/home" in previous_message.path and "flag{" in message.raw_body

def replace_word(self, stream: HTTPStream):
    """replace leet with l33t"""
    # the actual data sent by the socket is stream.current_data, so you can't just modify stream.current_http
    stream.current_data = stream.current_data.replace(b"leet", b"l33t")
    return False    # do not block message, just change its contents

def giftCard(self, stream:HTTPStream):
    message = stream.current_http

    db = DbManager().db.service_name
    
    if "GET" in message.method and "card" in message.parameters:
        cardNumber = message.parameters.get("card")
        item = {"cardNumber" : cardNumber }
        if db.find_one(item):
            return True
        else:
            db.insert_one(item)
            return False
    return False

################################################################################
# TCP

def nonPrintableChars(self, stream: TCPStream):
    """block packets with non printable chars"""
    return any([chr(c) not in string.printable for c in stream.current_data])

def password(self, stream:TCPStream):
    """block passwords longer than 10 characters"""
    if b"Insert password:" in stream.previous_data.splitlines()[-1] and len(stream.current_data.strip()) > 10:
        return True
    return False

def replace_word(self, stream:TCPStream):
    """replace leet with l33t"""
    stream.current_data = stream.current_data.replace(b"leet", b"l33t")
    return False    # do not block packet, just change its contents