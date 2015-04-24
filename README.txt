======================================
Assignment 5, Final Product (4/23/15)
COMP 112 - Networks
Andrew Mendelsohn & Alison Tai
======================================

Running Our Project:
0. Unzip folder.
1. Make sure you have Python installed (must have version less than 3)
2. Make sure you have the following libraries installed: httplib, socket. If you do not, run "pip install [library name]".
3. Run "python proxy.py [port #]"

Implemented Functionality:
- Proxy supports GET requests.
- Caching of HTML, CSS, and JS with a policy of only caching content that has been requested more than once. 
- Requests/clients are handled concurrently.
- Pre-fetching HTML, CSS, and JS that are linked to and adding them to the cache if they are not there already.