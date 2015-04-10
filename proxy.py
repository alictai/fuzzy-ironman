# Andrew Mendelsohn
# Alison Tai
# 
# Comp 112 - Networks
# a5 - HTTP Proxy

import httplib
# import request
import socket
import sys

from HTTPRequest import HTTPRequest

HOST = 'localhost'
PORT = 9999
BUFF_LEN = 8192

def main():
  global PORT

  if sys.argv[1]:
    PORT = int(sys.argv[1])

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  s.listen(10)

  while 1:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    while 1:
      handle_req(conn, addr)
       
def handle_req(conn, addr):
  req_str = conn.recv(BUFF_LEN)
  print "Got " + req_str
  req = HTTPRequest(req_str)
  print req.error_code     
  print req.command        
  print req.path           
  print req.request_version
  print len(req.headers)   
  print req.headers.keys() 
  print req.headers['host']

def send_http():
  pass

if __name__ == '__main__':
	main()
