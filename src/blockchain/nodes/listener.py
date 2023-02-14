from multiprocessing.connection import Listener
import traceback
from unCommitedTransactions import UnCommittedTransaction


class ListenNewTxns:
    txns = []

    def __init__(self):
        pass

    def listen(self, nodeId):
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
                    if msg and msg.get("txn") is not None and msg.get("node_id") is not None:
                        if nodeId == int(msg.get("node_id")):
                            new_txn = msg.get("txn")
                            sender = new_txn.get("sender")
                            reciever = new_txn.get("reciever")
                            message = new_txn.get("message")
                            un_committed_txns = UnCommittedTransaction(sender, reciever, message)
                            self.txns.append(un_committed_txns)
        except Exception:
            traceback.print_exc()
        finally:
            if listener is not None:
                listener.close()
