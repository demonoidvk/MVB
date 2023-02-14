import json
import sys
import os
from src.blockchain.utility import util
from src.blockchain.nodes.unCommitedTransactions import UnCommittedTransaction
from sender import send_message


def write_if_empty(data):
    outer_level = {}
    input_data = [data]
    outer_level["data"] = input_data
    return outer_level


def main():
    data = {"message": sys.argv[1], "node": sys.argv[2]}
    msg = json.loads(sys.argv[1])
    node_id = str(int(sys.argv[2]))
    filename = node_id + "--" + "inputMessages.json"
    if os.path.isfile(filename) and os.path.getsize(filename) > 0:
        json_data = util.read_json_data_from_file(filename)
        if json_data and len(json_data) > 0:
            outer_level = {}
            file_data = list(json_data.get("data"))
            file_data.append(data)
            outer_level["data"] = file_data
        else:
            outer_level = write_if_empty(data)

        transaction = UnCommittedTransaction(msg.get("sender"), msg.get("reciever"), msg.get("message"))
        message = {"txn": transaction, "node_id": node_id}
        send_message(message)
        util.write_json_data_to_file(filename, outer_level)
    else:
        outer_level = write_if_empty(data)
        transaction = UnCommittedTransaction(msg.get("sender"), msg.get("reciever"), msg.get("message"))
        message = {"txn": transaction, "node_id": node_id}
        send_message(message)
        util.write_json_data_to_file(filename, outer_level)


if __name__ == "__main__":
    if sys.argv is not None and len(sys.argv) > 0:
        main()
    else:
        print("Please verify the inputs!")
