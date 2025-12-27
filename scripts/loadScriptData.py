import os, json
from typing import Callable
from findParameters import *
from blocks import BLOCKS

class BlockData:
    def __init__(self, key: str, path: str, parser: Callable):
        self.key = key
        self.path = path
        self.parser = parser
        self.data = self.load_json()
        self.parameters = []

    @staticmethod
    def get(block_key: str, block_info: dict) -> 'BlockData':
        return BlockData(block_key, block_info["json"], block_info["parser_function"])

    def load_json(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def save_json(self):
        data = self.data
        if "parameters" not in data:
            data["parameters"] = []
        else:
            if type(data["parameters"]) is dict:
                data["parameters"] = list(data["parameters"].values()) 
        parsed_item_path = BLOCKS[self.key]["parser_data"]
        self.parser(parsed_item_path, data["parameters"])
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    for block_key, block_info in BLOCKS.items():
        # skip if not parsable
        if block_info["parser_function"] is None:
            continue

        block_data = BlockData.get(block_key, block_info)
        block_data.save_json()