# Collection of tools for blender used for map creating

## Unique item utility
A collection of simple utilities for Blender to streamline object selection, renaming, and visibility management based on base names.  
Ideal for managing imported or duplicated assets, and for cleaning up complex scenes.

### Features

- **Select by Base Name:**  
  Selects all objects sharing the same base name (e.g., `Cube`, `Cube.001`, `Cube.002`).

- **Rename Selected Objects Uniquely:**  
  Renames selected objects to unique base names, automatically adding `_1`, `_2`, etc., and avoiding name conflicts.

- **Hide Unique Named Objects:**  
  Hides all objects whose base name is unique in the scene (objects with no siblings sharing their base).


### Installation

1. Download or clone this repository.
2. In Blender, go to `Edit` → `Preferences` → `Add-ons` → `Install`.
3. Select the `unique_obj_tool.py` file and enable the add-on.

### Usage

Once enabled:
- Right-click in the 3D Viewport to open the **Object Context Menu** for access to these tools.
- "Select by Base Name" and "Rename Selected Objects Unique" are found in the context menu.
- "Hide Unique Named Objects" is available in the **Show/Hide** menu.

### Example Scenarios

- Quickly select all variants of an imported asset by their base name.
- Automatically clean up naming collisions after merging objects from different sources.
- Hide all uniquely named clutter to focus on duplicate/variant objects.

# Compatibility

- Blender 3.0 and above.

