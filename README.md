Provides information regarding various script blocks and parameters of Project Zomboid [scripts](https://pzwiki.net/wiki/Scripts) system.

# Script blocks
Script blocks can have the following attributes:
- `name`: The name of the block. (required)
- `description`: A brief description of what the block does. (required)
- `shouldHaveParent`: A boolean indicating whether the block should have a parent block or not.
- `parents`: A list of block names that can be parents to this block.
- `needsChildren`: A list of block names that are required as children of this block.
- `ID`: A dictionary about the ID attribute of the block. If not given, the block can't have any ID.
- `parameters`: A list of parameters associated with the block.

## ID
The `ID` dictionary can have the following attributes:
- `parentsWithout`: A list of block names that cannot be parents if this block has an ID.
- `values`: A list of allowed ID values for this block. If not given, any value is allowed.
- `asType`: Specifies if the ID of the block should count as the block type. For example components have specific definitions based on their ID. This means a script block needs to be defined with the name `component <componentID>` as well as `component` to cover all component types available with the `values` attribute.
- 

# Parameters
Parameters can have the following attributes:
- `name`: The name of the parameter. (required)
- `#ref`: A reference to another block parameter.
- `description`: A brief description of what the parameter does.
- `allowedDuplicate`: A boolean indicating whether the parameter can be duplicated.
- `canBeEmpty`: A boolean indicating whether the parameter can be empty.
- `itemTypes`: Specifies an array of the type of items the parameter is associated with (e.g., "vehicle", "item", etc.). Only for item scripts.