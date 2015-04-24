# Andrew Mendelsohn
# Alison Tai
# 
# Comp 112 - Networks
# a5 - HTTP Proxy

import httplib
import socket
import sys

from HTTPRequest import HTTPRequest

HOST = 'localhost'
BUFF_LEN = 8192

cache = {}

def main():
  if sys.argv[1]:
    port = int(sys.argv[1])
  else:
    port = 9999

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, port))
  s.listen(10)

  while 1:
    conn, addr = s.accept()
    handle_req(conn, addr)
    conn.close()


def handle_req(conn, addr):
  req_str = conn.recv(BUFF_LEN)
  if not req_str:
    return

  req_key = req_str.split('\n')[0]
  if req_key in cache.keys():
    print "Cache HIT:"
    print "Key: " + req_key
    resp_str = cache[req_key]
  else:
    print "Cache MISS... Relaying request"
    resp_str = relay_request(req_str)
    if not resp_str:
      return
    cache[req_key] = resp_str
    
  # print resp_str
  conn.send(resp_str)


def relay_request(req_str):
  # print req_str
  req = HTTPRequest(req_str)
  if req.command == 'GET':
    http_conn = httplib.HTTPConnection(req.headers['host'])
    http_conn.connect()
    http_conn.request(req.command, req.path, headers=req.headers.dict)
    resp = http_conn.getresponse()
    content = resp.read()

    headers = resp.getheaders()
    headers_str = '\n'.join(map((lambda (k, v): '%s: %s' % (k, v)), headers))
    resp.version = str(float(resp.version)/10)
    resp_str = 'HTTP/%s %s %s\n%s\n\n%s' % (resp.version, resp.status, resp.reason, headers_str, content)

    http_conn.close()
    return resp_str
  else:
    return None


if __name__ == '__main__':
  main()
