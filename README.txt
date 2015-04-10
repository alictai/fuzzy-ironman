======================================
Assignment 5, Checkpoint 1 (4/10/15)
COMP 112 - Networks
Andrew Mendelsohn & Alison Tai
======================================

Running Our Project:
0. Unzip folder.
1. Make sure you have Python installed (must have version less than 3)
2. Make sure you have the following libraries installed: httplib, socket. If you do not, run "pip install [library name]".
2. Run "python proxy.py [port #]"

Functionality to Implement:
- Caching
- Concurrent clients
- Pre-fetching pages that are linked to

Progress So Far:
- Baseline proxy which supports basic GET requests from a single client - Caching 
- Queue of up to 10 requests, but will be fully support concurrent clients in final product