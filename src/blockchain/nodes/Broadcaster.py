from multiprocessing.connection import Client
import time
import traceback
from src.blockchain.utility import constants


def send_message(transaction):
    conn = None
    try:
        conn = Client(('localhost', constants.broadcast_port), authkey=b'secret password')
        conn.send(transaction)
        time.sleep(1)
    except Exception:
        traceback.print_exc()
    finally:
        if conn is not None:
            conn.close()
