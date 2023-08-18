import os
import json
def read_receipt(receipt):
    """Reads a fixture receipt"""
    current = os.path.dirname(__file__)
    with open(f"{current}/fixtures/{receipt}") as f:
        return json.loads(f.read())

