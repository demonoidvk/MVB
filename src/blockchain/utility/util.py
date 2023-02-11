import json
import constants


def read_json_data_from_file(filename):
    f = open(filename, 'r')
    return json.load(f)


def write_json_data_to_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)


def get_node_id():
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
