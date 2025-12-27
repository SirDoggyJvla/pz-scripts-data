import os
from findParameters import *

BLOCKS = {
    "item": {
        "parser_data": "data/cache/parsed_item_data.json",
        "json": "data/blocks/item.json",
        "parser_function": find_item_parameters
    },
    "model": {
        "parser_data": "data/cache/parsed_model_data.json",
        "json": "data/blocks/model.json",
        "parser_function": find_parameters
    },
    "fluid": {
        "parser_data": "data/cache/parsed_fluid_data.json",
        "json": "data/blocks/fluid.json",
        "parser_function": find_parameters
    }
}


PARSER_PATH = "/home/simon/Documents/Repositories/pz-wiki_parser"
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

## init paths
for block_key, block_info in BLOCKS.items():
    block_info["parser_data"] = os.path.join(PARSER_PATH, block_info["parser_data"])
    block_info["json"] = os.path.join(PROJECT_DIR, block_info["json"])