import json, os
import echo, color
# from blocks import BLOCKS
from typing import Any

potentialScriptBlocks = []


CLEARING_KEYS = ["version", "ScriptType", "SourceFile"]
def _clean_parsed(parsed_data: dict) -> dict:
    for key, data in parsed_data.copy().items():
        if key in CLEARING_KEYS:
            del parsed_data[key]
        if isinstance(data, dict):
            parsed_data[key] = _clean_parsed(data)
    return parsed_data

def load_existing(parameters: list) -> dict:
    existing = {}
    for param in parameters:
        existing[param["name"]] = param
    return existing

def find_existing(parameters: list, key: str) -> int|None:
    for i, param in enumerate(parameters):
        if "name" in param and param["name"] == key:
            return i
    return None

# verify all previously documented parameters are still present
def verify_existing(parameters: list, uniques: dict) -> None:
    for param in parameters:
        key = param.get("name")
        if key not in uniques.values():
            echo.warning(f"Previously documented parameter ('{color.red(key)}') not present in current scripts version")

# check if the parameter name has multiple case variations across definitions
def verify_multiple_cases(uniques: dict, param_key: str) -> None:
    lower_key = param_key.lower()
    if lower_key not in uniques:
        uniques[lower_key] = param_key
    else:
        if uniques[lower_key] != param_key:
            echo.warning(f"Parameter name has multiple cases for '{lower_key}': '{uniques[lower_key]}' vs '{param_key}'")

def verify_complex_parameter(existing: int|None, checked: list, param_key: str, param_value: Any) -> bool:
    # register parameter
    namedLikeBlock = param_key.lower() in EXISTING_BLOCKS
    if type(param_value) == dict or namedLikeBlock:
        blockStr = color.debug('(named like existing block)') if namedLikeBlock else ''
        inExisting = existing is not None
        inExistingStr = color.debug2('(in existing parameters)') if inExisting else ''
        if param_key not in checked:
            echo.warning(f"Skipping complex parameter '{color.red(param_key)}' {blockStr} {inExistingStr}")
            checked.append(param_key)
        return True
    return False



def find_parameters(parsed_path: str, parameters: list, block_name: str) -> list:
    echo.debug(f"Searching for {color.blue(block_name)}")
    # parse the data from the parser output
    with open(parsed_path, "r") as f:
        parsed_data = _clean_parsed(json.load(f))
        echo.info(f"Loaded parsed data from {parsed_path}")

    uniques = {}
    for id, data in parsed_data.items():
        for param_key, param_value in data.items():
            verify_multiple_cases(uniques, param_key)
            
            existing = find_existing(parameters, param_key)
            if existing is None:
                parameters.append({
                    "name": param_key,
                })

    verify_existing(parameters, uniques)
    
    return parameters


def find_item_parameters(parsed_path: str, parameters: list, block_name: str) -> list:
    echo.debug(f"Searching for {color.blue(block_name)}")
    # parse the item data from the parser output
    with open(parsed_path, "r") as f:
        parsed_data = _clean_parsed(json.load(f))
        echo.info(f"Loaded parsed data from {parsed_path}")

    uniques = {}
    checked = []
    for item_id, item_data in parsed_data.items():
        for param_key, param_value in item_data.items():
            lower_key = param_key.lower()

            verify_multiple_cases(uniques, param_key)

            existing = find_existing(parameters, param_key)
            if verify_complex_parameter(existing, checked, param_key, param_value): continue

            itemType = item_data["ItemType"]
            if existing is None:
                parameters.append({
                    "name": param_key,
                    "itemTypes": [itemType],
                })
            else:
                # check if parameter is used by a different class of items
                itemTypes = parameters[existing]["itemTypes"]
                if itemType not in itemTypes:
                    itemTypes.append(itemType)

    verify_existing(parameters, uniques)
    
    return parameters

_ignore_params_recipe = ["name", "default", "inputs", "outputs", "itemMapper"]
def find_craftRecipe_parameters(parsed_path: str, parameters: list, block_name: str) -> list:
    echo.debug(f"Searching for {color.blue(block_name)}")
    # parse the data from the parser output
    with open(parsed_path, "r") as f:
        parsed_data = _clean_parsed(json.load(f))
        echo.info(f"Loaded parsed data from {parsed_path}")

    uniques = {}
    checked = []
    for model_id, model_data in parsed_data.items():
        for param_key, param_value in model_data.items():
            lower_key = param_key.lower()
            if lower_key in _ignore_params_recipe: continue

            verify_multiple_cases(uniques, param_key)

            existing = find_existing(parameters, param_key)
            if verify_complex_parameter(existing, checked, param_key, param_value): continue
            
            if existing is None:
                parameters.append({
                    "name": param_key,
                })

    verify_existing(parameters, uniques)
    
    return parameters




def find_component_FluidContainer_parameters(parsed_path: str, parameters: list, block_name: str) -> list:
    echo.debug(f"Searching for {color.blue(block_name)}")

    # parse the data from the parser output
    with open(parsed_path, "r") as f:
        parsed_data = _clean_parsed(json.load(f))
        echo.info(f"Loaded parsed data from {parsed_path}")

    uniques = {}
    checked = []
    for item_id, item_data in parsed_data.items():
        components = item_data.get("component", {})
        fluidContainer = components.get("FluidContainer", None)
        if not fluidContainer:
            continue
        # print("\n", item_id)
        for param_key, param_value in fluidContainer.items():
            verify_multiple_cases(uniques, param_key)

            existing = find_existing(parameters, param_key)
            if verify_complex_parameter(existing, checked, param_key, param_value): continue
            # print(param_key)
            
            if existing is None:
                parameters.append({
                    "name": param_key,
                })

    verify_existing(parameters, uniques)
    
    return parameters


def find_component_CraftRecipe_parameters(parsed_path: str, parameters: list, block_name: str) -> list:
    echo.debug(f"Searching for {color.blue(block_name)}")
    # parse the data from the parser output
    with open(parsed_path, "r") as f:
        parsed_data = _clean_parsed(json.load(f))
        echo.info(f"Loaded parsed data from {parsed_path}")

    # load craftRecipe data
    data_craftRecipe_path = BLOCKS["craftRecipe"]["json"]
    with open(data_craftRecipe_path, "r") as f:
        data_craftRecipe_data = _clean_parsed(json.load(f))

    craftRecipe_parameters = load_existing(data_craftRecipe_data.get("parameters", []))

    uniques = {}
    checked = []
    for item_id, item_data in parsed_data.items():
        for param_key, param_value in item_data.items():
            lower_key = param_key.lower()
            if lower_key in _ignore_params_recipe: continue

            verify_multiple_cases(uniques, param_key)

            existing = find_existing(parameters, param_key)
            if verify_complex_parameter(existing, checked, param_key, param_value): continue
            
            if existing is None:
                if param_key in craftRecipe_parameters:
                    parameters.append({
                        "name": param_key,
                        "#ref": f"craftRecipe/{param_key}",
                    })
                else:
                    parameters.append({
                        "name": param_key,
                    })

    verify_existing(parameters, uniques)
    
    return parameters








## PREPARE DATA

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
    # "entity": {},
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
    # "component CraftRecipe": {
    #     "parser_function": find_component_CraftRecipe_parameters,
    #     "parser_data": "data/cache/parsed_entity_data.json",
    # },
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
        EXISTING_BLOCKS[block_name.lower()] = os.path.join(_BLOCKS_PATH, filename)