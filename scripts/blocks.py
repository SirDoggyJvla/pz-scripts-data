import os
from findParameters import *
from typing import Any
from pprint import pprint
import echo, color

_DEFAULT_PARSER = "data/cache/parsed_{block_key}_data.json"
_BLOCKS_PATH = "data/blocks"
_DEFAULT_JSON = os.path.join(_BLOCKS_PATH, "{block_key}.json")
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
    "component FluidContainer": {
        "parser_function": find_component_FluidContainer_parameters,
        "parser_data": "data/cache/parsed_item_data.json",
    },
    "component CraftRecipe": {
        "parser_function": find_component_CraftRecipe_parameters,
        "parser_data": "data/cache/parsed_entity_data.json",
    }
}




PARSER_PATH = "/home/simon/Documents/Repositories/pz-wiki_parser"
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def setup_block_paths(block_key: str, block_info: dict[str, Any]) -> None:
    parser_data = block_info.get("parser_data", _DEFAULT_PARSER).format(block_key=block_key)
    block_info["parser_data"] = os.path.join(PARSER_PATH, parser_data)

    json_data = block_info.get("json", _DEFAULT_JSON).format(block_key=block_key)
    block_info["json"] = os.path.join(PROJECT_DIR, json_data)

    if "parser_function" not in block_info:
        block_info["parser_function"] = _DEFAULT_PARSER_FUNCTION

## init paths to components
for block_key, block_info in BLOCKS.items():
    setup_block_paths(block_key, block_info)


EXISTING_BLOCKS = {}

# read _BLOCKS_PATH, with names of the existing json files the block name
for filename in os.listdir(_BLOCKS_PATH):
    if filename.endswith(".json"):
        block_name = filename[:-5]  # remove .json extension
        echo.info(f"Registering existing block: {block_name}")
        EXISTING_BLOCKS[block_name] = os.path.join(_BLOCKS_PATH, filename)