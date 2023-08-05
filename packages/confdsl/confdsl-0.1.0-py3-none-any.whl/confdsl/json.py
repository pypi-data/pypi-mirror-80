import json


def get_conf(file, key, default=None):
    with open(file, "r") as fp:
        return json.load(fp).get(key) or default
