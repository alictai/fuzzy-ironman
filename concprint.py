def prt(to_print, mutex):
	mutex.acquire()
	print to_print
	mutex.release()