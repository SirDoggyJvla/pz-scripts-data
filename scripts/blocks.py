import os
from findParameters import *

_DEFAULT_PARSER = "data/cache/parsed_{block_key}_data.json"
_DEFAULT_JSON = "data/blocks/{block_key}.json"
_DEFAULT_PARSER_FUNCTION = find_parameters

BLOCKS = {
    "animationsMesh": {},
    "craftRecipe": {
        "parser_function": find_craftRecipe_parameters
    },
    "component": {
        "parser_function": None,
    },
    "entity": {},
    "evolvedrecipe": {},
    "fixing": {
        "parser_function": None,
    },
    "fluid": {},
    "item": {
        "parser_function": find_item_parameters
    },
    "mannequin": {},
    "model": {},
    "sound": {},
    "timedAction": {},
    "vehicle": {},
}


PARSER_PATH = "/home/simon/Documents/Repositories/pz-wiki_parser"
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def setup_block_paths(block_key: str, block_info: dict):
    parser_data = block_info.get("parser_data", _DEFAULT_PARSER).format(block_key=block_key)
    block_info["parser_data"] = os.path.join(PARSER_PATH, parser_data)

    json_data = block_info.get("json", _DEFAULT_JSON).format(block_key=block_key)
    block_info["json"] = os.path.join(PROJECT_DIR, json_data)

    if "parser_function" not in block_info:
        block_info["parser_function"] = _DEFAULT_PARSER_FUNCTION

## init paths to components
for block_key, block_info in BLOCKS.items():
    setup_block_paths(block_key, block_info)