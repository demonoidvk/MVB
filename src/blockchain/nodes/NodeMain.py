import threading
import time

from BroadcastListener import BroadcastListener
from listener import ListenNewTxns
from src.blockchain.utility import util, constants
from nacl.public import Box
from Broadcaster import send_message


class NodeMain:
    un_committed_txns = []
    processed_txns = []
    can_be_committed_txns = []

    def __init__(self):
        self.listener = ListenNewTxns()
        self.broadcast_listener = BroadcastListener()
        self.node_id = util.get_node_id(constants)
        self.listener_thread = threading.Thread(self.listener.listen(int(self.node_id)))
        self.broadcast_listener_thread = threading.Thread(self.broadcast_listener.listen())

    def generate_hash_for_message(self, un_committed_txn):
        sender_keys = util.generate_user_keys()
        reciever_keys = util.generate_user_keys()
        encryption_data = Box(sender_keys[0], reciever_keys[1])
        encrypted_message = util.encrypt_message(encryption_data, un_committed_txn.get("message"))
        return encrypted_message

    def compute(self):
        while len(self.un_committed_txns) > 0:
            if len(self.listener.txns) > 0:
                self.un_committed_txns.append(self.listener.txns.pop(0))
                un_committed_txn = self.un_committed_txns.pop(0)
                if self.validate_message(un_committed_txn.get("message")):
                    encrypted_message = self.generate_hash_for_message(un_committed_txn)
                    self.processed_txns.append(encrypted_message)
                    check = self.check_if_can_be_committed()
                    if check:
                        self.commit_processed_block()
        running = False
        while not running:
            time.sleep(10)
            if len(self.un_committed_txns) > 0:
                running = True
        self.compute()

    def check_if_can_be_committed(self):
        if util.check_last_txn_time() or len(self.processed_txns) > 10:
            lock = threading.Lock()
            lock.acquire()
            self.can_be_committed_txns = self.processed_txns[:-2]
            del self.processed_txns[:-2]
            lock.release()
            return True
        return False

    def commit_processed_block(self):
        sign_and_verify = util.generate_signature_for_a_transaction_set(self.can_be_committed_txns)
        signature = sign_and_verify[0]
        verify_key_hex = sign_and_verify[1]
        data = {"signature": signature, "verification_key_hex": verify_key_hex,
                "transactions": self.can_be_committed_txns}
        outer_layer = {"data": data, "block": True}
        self.can_be_committed_txns = []
        send_message(outer_layer)

    def validate_message(self, message):
        pass

    def start_listener(self):
        self.listener_thread.start()
        if self.listener_thread:
            return True
        else:
            return False

    def start_broadcast_listener(self):
        self.broadcast_listener_thread.start()
        if self.broadcast_listener_thread:
            return True
        else:
            return False


if __name__ == "__main__":
    node = NodeMain()
    if node.start_listener() and node.start_broadcast_listener():
        node_thread = threading.Thread(node.compute())
