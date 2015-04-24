======================================
Assignment 5, Final Product (4/23/15)
COMP 112 - Networks
Andrew Mendelsohn & Alison Tai
======================================

Files:
- proxy.py: the main proxy file 
- concprint.py: module that forces sequential printing by using a mutex to restrict stdout
- HTTPRequest.py: parses HTTP responses and requests (credit: http://stackoverflow.com/questions/2115410/does-python-have-a-module-for-parsing-http-requests-and-responses)

Running Our Project:
0. Unzip folder.
1. Make sure you have Python installed (must have version less than 3)
2. Make sure you have the following libraries installed: httplib, socket. If you do not, run "pip install [library name]".
3. Run "python proxy.py [port #]"

Implemented Functionality:
- Proxy supports GET requests.
- Caching with a policy of only caching content that has been requested more than once, and an eviction policy which deletes anything in the cache that is older than the constant CACHE_LIFE.
- Requests/clients are handled concurrently.
- Pre-fetching HTML and images and adding them to the cache if they are not there already.