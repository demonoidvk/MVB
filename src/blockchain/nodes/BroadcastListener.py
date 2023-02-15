from multiprocessing.connection import Listener
import traceback
from unCommitedTransactions import UnCommittedTransaction
import listener as txListener
from src.blockchain.utility import constants


class BroadcastListener:
    def __init__(self):
        pass

    def listen(self):
        listener = None
        try:
            listener = Listener(('localhost', constants.broadcast_port), authkey=b'secret password')
            running = True
            while running:
                conn = listener.accept()
                print('connection accepted from', listener.last_accepted)
                while True:
                    msg = conn.recv()
                    if msg.get("txn"):
                        sender = msg.get("sender")
                        reciever = msg.get("reciever")
                        message = msg.get("message")
                        unCommittedtxn = UnCommittedTransaction(sender, reciever, message)
                        txListener.ListenNewTxns.txns.append(unCommittedtxn)
                    elif msg.get("block"):
                        block = msg.get("data")
        except Exception:
            traceback.print_exc()
        finally:
            if listener is not None:
                listener.close()
