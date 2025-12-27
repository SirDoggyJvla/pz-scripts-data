import os, json
from pprint import pprint
import echo, color

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

class SCRIPT_PARSER_DATA:
    PARSER_PATH = "/home/simon/Documents/Repositories/pz-wiki_parser"
    item = "data/cache/parsed_item_data.json"

    @staticmethod
    def get(key):
        assert hasattr(SCRIPT_PARSER_DATA, key), f"{key} not found in SCRIPT_PARSER_DATA."
        return os.path.join(SCRIPT_PARSER_DATA.PARSER_PATH, getattr(SCRIPT_PARSER_DATA, key))

def find_item_parameters(parsed_path, item_parameters):
    with open(parsed_path, "r") as f:
        parsed_data = json.load(f)

    echo.info(f"Loaded parsed data from {parsed_path}")

    uniques = {}
    for item_id, item_data in parsed_data.items():
        if item_id == "version": continue

        for param_key in item_data.keys():
            lower_key = param_key.lower()
            if lower_key not in uniques:
                uniques[lower_key] = param_key
            else:
                if uniques[lower_key] != param_key:
                    echo.warning(f"Parameter name has multiple cases for '{lower_key}': '{item_parameters[lower_key]}' vs '{param_key}'")

            itemType = item_data["ItemType"]

            if param_key not in item_parameters:
                item_parameters[param_key] = {
                    "name": param_key,
                    "itemTypes": [itemType],
                }
            else:
                itemTypes = item_parameters[param_key]["itemTypes"]
                if itemType not in itemTypes:
                    itemTypes.append(itemType)

    for key in item_parameters.keys():
        if key not in uniques.values():
            echo.warning(f"Previously documented parameter ('{color.red(key)}') not present in current scripts version")
    
    return item_parameters

class BlockData:
    item = {"path": "data/blocks/item.json", "parser": find_item_parameters}

    def __init__(self, key: str, path: str, parser):
        self.key = key
        self.path = path
        self.parser = parser
        self.data = self.load_json()
        self.parameters = []

    @staticmethod
    def get(key: str):
        assert hasattr(BlockData, key), f"{key} not found in BLOCK_DATA."
        default = getattr(BlockData, key)
        path = os.path.join(PROJECT_DIR, default["path"])
        return BlockData(key, path, default["parser"])

    def load_json(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def save_json(self):
        data = self.data
        if "parameters" not in data:
            data["parameters"] = {}
        parsed_item_path = SCRIPT_PARSER_DATA.get(script_type)
        self.parser(parsed_item_path, data["parameters"])
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    script_type = "item"
    # parsed_item_path = SCRIPT_PARSER_DATA.get(script_type)
    # item_params = find_item_parameters(parsed_item_path)

    block_data = BlockData.get(script_type)
    block_data.save_json()