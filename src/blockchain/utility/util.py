import json

import nacl.utils
from nacl.public import PrivateKey, Box
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder


def read_json_data_from_file(filename):
    f = open(filename, 'r')
    return json.load(f)


def write_json_data_to_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)


def get_node_id(constants):
    data = read_json_data_from_file(constants.ledger_file)
    if data and data.get("node_list") is not None and len(data.get("node_list")) > 0:
        nodes = list(data.get("node_list"))
        nodes.append((int(nodes[-1]) + 1))
        data["node_list"] = nodes
        write_json_data_to_file(constants.ledger_file, data)
        return nodes[-1]
    else:
        nodes = [1]
        data["node_list"] = nodes
        write_json_data_to_file(constants.ledger_file, data)
        return nodes[-1]


def generate_user_keys():
    userPK = PrivateKey.generate()
    userPuK = userPK.public_key
    return [userPK, userPuK]


def encrypt_message(box, message):
    nonce = nacl.utils.random(Box.NONCE_SIZE)
    return box.encrypt(message, nonce)


def decrypt_message(userPK, userPuK, message):
    user_box = Box(userPK, userPuK)
    plain_message = user_box.decrypt(message)
    return plain_message.decode("utf-8")


def generate_signature_for_a_transaction_set(txns):
    signing_key = SigningKey.generate()
    signed_data = signing_key.sign(txns, encoder=HexEncoder)
    verify_key = signing_key.verify_key
    hex_verify_key = verify_key.encode(encoder=HexEncoder)
    return [signed_data, hex_verify_key]


def check_last_txn_time():
    pass