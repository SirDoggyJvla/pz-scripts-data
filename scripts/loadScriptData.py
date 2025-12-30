import os, json
from pprint import pprint
from typing import Callable
from findParameters import *
from blocks import BLOCKS, setup_block_paths

class BlockData:
    def __init__(self, key: str, path: str, parser: Callable):
        self.key = key
        self.path = path
        self.parser = parser
        self.data = self.load_json()

    @staticmethod
    def get(block_key: str, block_info: dict) -> 'BlockData':
        return BlockData(block_key, block_info["json"], block_info["parser_function"])

    def load_json(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def save_json(self):
        data = self.data
        # ensure parameters field exists
        if "parameters" not in data:
            data["parameters"] = []
        if self.parser is not None:
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

    # load components
    block_key = "component"
    component_info = BLOCKS[block_key]
    block_data = BlockData.get(block_key, component_info)

    # load data for each component variant
    component_data = block_data.data
    values = component_data["ID"]["values"]

    for value in values:
        variant_name = block_key + " " + value
        block_info = {
            "parser_function": None,
        }
        setup_block_paths(variant_name, block_info)

        # if json file doesn't exist, create it as a copy of the base component
        json_path: str = block_info["json"]
        if not os.path.exists(json_path):
            with open(json_path, "w") as f:
                json.dump(component_data, f, indent=4)

        variant_data = BlockData.get(variant_name, block_info)
        variant_data.data["name"] = variant_name # force correct name
        variant_data.save_json()

    pprint(component_data)