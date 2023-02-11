from multiprocessing.connection import Listener
import traceback


def listen():
    listener = None
    try:
        listener = Listener(('localhost', 6000), authkey=b'secret password')
        running = True
        while running:
            conn = listener.accept()
            print('connection accepted from', listener.last_accepted)
            while True:
                msg = conn.recv()
                if msg == 'close connection':
                    conn.close()
                    break
                if msg == 'close server':
                    conn.close()
                    running = False
                    break
    except Exception:
        traceback.print_exc()
    finally:
        if listener is not None:
            listener.close()
