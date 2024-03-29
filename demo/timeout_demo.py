# Andrew Mendelsohn
# Alison Tai
# 
# Comp 112 - Networks
# a5 - HTTP Proxy

import datetime
import httplib
import socket
import sys
import threading
import re
from concprint import prt

from HTTPRequest import HTTPRequest

HOST = 'localhost'
BUFF_LEN = 8192
CACHE_LIFE = 10

cache = {}
past_reqs = set()

stdout_mutex = threading.Lock()

def main():
  if len(sys.argv) > 1 and sys.argv[1]:
    port = int(sys.argv[1])
  else:
    port = 9999

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, port))
  s.listen(10)

  while 1:
    conn, addr = s.accept()
    t = threading.Thread(target=handle_req, args=[conn, addr])
    t.start()
    cleanse_cache()

def handle_req(conn, addr):
  req_str = conn.recv(BUFF_LEN)
  if not req_str:
    return

  resp_str = check_cache(req_str)
  if resp_str:
    conn.send(resp_str)
    links = detect_links(resp_str)
    prefetch_links(links, req_str)

  conn.close()


def check_cache(req_str, force=False):
  req_key = req_str.split('\n')[0] # First line of req
  if req_key in cache.keys():
    prt("+++ Cache HIT: " + req_key, stdout_mutex)
    resp_str = cache[req_key][0]
  else:
    prt("XXX Cache MISS: " + req_key, stdout_mutex)
    resp_str = relay_request(req_str)
    if not resp_str:
      return
    if force or req_key in past_reqs: # Cache if requested multiple times
      prt("--> Cache updated with " + req_key, stdout_mutex)
      cache[req_key] = resp_str, datetime.datetime.now()
    else:
      past_reqs.add(req_key)
  return resp_str


def detect_links(response):
  instances = re.finditer('href[ ]*=[ ]*"([^"]*)"', response, flags=0)
  links = [response[m.start():m.end()].replace(" ", "")[6:-1] for m in instances]
  return links


def prefetch_links(links, req):
  for l in links:
    if len(l) > 3:
      if l[-4] == ".jpg" or l[-4] == ".png" or l[-4] == ".gif" or l[-5:] == ".html" or l[-5] == ".jpeg":
        t = threading.Thread(target=prefetch, args=[l, req])
        t.start()


def prefetch(link, req):
  line1 = req.split('\n')[0]
  url = line1.split(' ')[1]
  if (link[:7] != "http://"):
    parts = url.split('/')
    parts[-1] = link
    new_url = '/'.join(parts)
    req = req.replace(url, new_url, 1)
  else:
    req = req.replace(url, link)
  check_cache(req, True)


def relay_request(req_str):
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


def cleanse_cache():
  to_delete = []
  now = datetime.datetime.now()
  for k, v in cache.iteritems():
    if (now - v[1]).total_seconds() > CACHE_LIFE:
      to_delete.append(k)
  for k in to_delete:
    del cache[k]


if __name__ == '__main__':
  main()
