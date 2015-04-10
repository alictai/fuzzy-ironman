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
PORT = 9999
BUFF_LEN = 8192

cache = {}

def main():
  global PORT

  if sys.argv[1]:
    PORT = int(sys.argv[1])

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  s.listen(10)

  while 1:
    conn, addr = s.accept()
    handle_req(conn, addr)
    conn.close()

def handle_req(conn, addr):
  req_str = conn.recv(BUFF_LEN)
  if not req_str:
    return

  print "Got " + req_str

  req_key = req_str.split('\n')[0]
  if req_key in cache.keys():
    # print "Cache HIT:"
    # print "Key: " + req_key
    # print "Val: " + cache[req_key]
    resp_str = cache[req_key]
  else:
    # print "Relaying request"
    resp_str = relay_request(req_str)
    cache[req_key] = resp_str

  # print "Sending back:"
  # print resp_str
  conn.send(resp_str)


def relay_request(req_str):
  req = HTTPRequest(req_str)
  http_conn = httplib.HTTPConnection(req.headers['host'])
  http_conn.connect()
  http_conn.request(req.command, req.path, headers=req.headers.dict)
  resp = http_conn.getresponse()
  content = resp.read()

  headers = resp.getheaders()
  headers_str = '\n'.join(map((lambda (k, v): '%s: %s' % (k, v)), headers))
  resp.version = str(float(resp.version)/10)
  resp_str = 'HTTP %s %s %s\n%s\n%s' % (resp.version, resp.status, resp.reason, headers_str, content)

  http_conn.close()
  return resp_str


if __name__ == '__main__':
	main()
