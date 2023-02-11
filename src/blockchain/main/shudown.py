from multiprocessing.connection import Client
import time

conn = Client(('localhost', 6000), authkey=b'secret password')
conn.send('close connection')
time.sleep(1)
conn.send('close server')
conn.close()