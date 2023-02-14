from multiprocessing.connection import Client
import time
import traceback


def send_message(message):
    conn = None
    try:
        conn = Client(('localhost', 6000), authkey=b'secret password')
        conn.send(message)
        time.sleep(1)
    except Exception:
        traceback.print_exc()
    finally:
        if conn is not None:
            conn.close()
