from src.blockchain.utility import util
import listener
import threading


class NodeMain:

    def __init__(self):
        self.listener = threading.Thread(listener.listen())
        self.node_id = util.get_node_id()

    def compute(self):
        pass

    def take_input(self):
        self.listener.start()


if __name__ == "__main__":
    node = NodeMain()
