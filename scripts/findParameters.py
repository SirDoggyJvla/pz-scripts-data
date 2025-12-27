import json
import echo, color

CLEARING_KEYS = ["version", "ScriptType", "SourceFile"]
def _clean_parsed(parsed_data: dict) -> dict:
    for key, data in parsed_data.copy().items():
        if key in CLEARING_KEYS:
            del parsed_data[key]
        if isinstance(data, dict):
            parsed_data[key] = _clean_parsed(data)
    return parsed_data

def find_item_parameters(parsed_path: str, item_parameters: dict) -> dict:
    # parse the item data from the parser output
    with open(parsed_path, "r") as f:
        parsed_data = _clean_parsed(json.load(f))
        echo.info(f"Loaded parsed data from {parsed_path}")

    uniques = {}
    for item_id, item_data in parsed_data.items():
        if item_id == "version": continue

        for param_key in item_data.keys():
            lower_key = param_key.lower()

            # check if the parameter name has multiple case variations
            # this probably isn't needed anymore since TIS generates these automatically now
            if lower_key not in uniques:
                uniques[lower_key] = param_key
            else:
                if uniques[lower_key] != param_key:
                    echo.warning(f"Parameter name has multiple cases for '{lower_key}': '{item_parameters[lower_key]}' vs '{param_key}'")

            # register parameter
            itemType = item_data["ItemType"]
            if param_key not in item_parameters:
                item_parameters[param_key] = {
                    "name": param_key,
                    "itemTypes": [itemType],
                }
            else:
                # check if parameter is used by a different class of items
                itemTypes = item_parameters[param_key]["itemTypes"]
                if itemType not in itemTypes:
                    itemTypes.append(itemType)

    # verify all previously documented parameters are still present
    for key in item_parameters.keys():
        if key not in uniques.values():
            echo.warning(f"Previously documented parameter ('{color.red(key)}') not present in current scripts version")
    
    return item_parameters



def find_parameters(parsed_path: str, parameters: dict) -> dict:
    # parse the data from the parser output
    with open(parsed_path, "r") as f:
        parsed_data = _clean_parsed(json.load(f))
        echo.info(f"Loaded parsed data from {parsed_path}")

    uniques = {}
    for model_id, model_data in parsed_data.items():
        if model_id == "version": continue

        for param_key in model_data.keys():
            lower_key = param_key.lower()

            # check if the parameter name has multiple case variations
            if lower_key not in uniques:
                uniques[lower_key] = param_key
            else:
                if uniques[lower_key] != param_key:
                    echo.warning(f"Parameter name has multiple cases for '{lower_key}': '{parameters[lower_key]}' vs '{param_key}'")

            # register parameter
            if param_key not in parameters:
                parameters[param_key] = {
                    "name": param_key,
                }

    # verify all previously documented parameters are still present
    for key in parameters.keys():
        if key not in uniques.values():
            echo.warning(f"Previously documented parameter ('{color.red(key)}') not present in current scripts version")
    
    return parameters