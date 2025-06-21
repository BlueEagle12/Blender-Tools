bl_info = {
    "name": "Select by Base Name",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
import re
from collections import defaultdict

def get_base_name(name):
    return name.split('.', 1)[0].strip()


class OBJECT_OT_rename_selected_unique(bpy.types.Operator):
    """Rename all selected objects to unique base, base_1, base_2... skipping conflicts"""
    bl_idname = "object.rename_selected_unique"
    bl_label = "Rename Selected Objects Unique"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None and len(context.selected_objects) > 0

    def execute(self, context):
        # Get a working set of all names except for selected objects
        all_names = {obj.name for obj in bpy.context.scene.objects}
        for obj in context.selected_objects:
            all_names.discard(obj.name)  # Don't block self
        
        # For each selected object, assign unique name
        renamed = 0
        for obj in context.selected_objects:
            base = get_base_name(obj.name)
            i = 0
            while True:
                if i == 0:
                    new_name = base
                else:
                    new_name = f"{base}_{i}"
                if new_name not in all_names:
                    obj.name = new_name
                    all_names.add(new_name)
                    renamed += 1
                    break
                i += 1
        self.report({'INFO'}, f"Renamed {renamed} objects with unique names.")
        return {'FINISHED'}
    

class OBJECT_OT_select_by_base_name(bpy.types.Operator):
    """Select all objects that share the base name of any selected object"""
    bl_idname = "object.select_by_base_name"
    bl_label = "Select by Base Name"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None and len(context.selected_objects) > 0

    def execute(self, context):
        # Get all unique base names from the selection
        base_names = set(get_base_name(obj.name) for obj in context.selected_objects)
        count = 0
        for obj in context.scene.objects:
            if get_base_name(obj.name) in base_names:
                obj.select_set(True)
                count += 1
        self.report({'INFO'}, f"Selected {count} objects sharing base names.")
        return {'FINISHED'}



class OBJECT_OT_hide_unique_base_name(bpy.types.Operator):
    """Hide all objects whose base name is unique (no siblings)"""
    bl_idname = "object.hide_unique_base_name"
    bl_label = "Hide Unique Named Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Count base names
        base_count = defaultdict(int)
        for obj in context.scene.objects:
            base = get_base_name(obj.name)
            base_count[base] += 1

        hidden = 0
        for obj in context.scene.objects:
            base = get_base_name(obj.name)
            if base_count[base] == 1:
                obj.hide_set(True)
                obj.hide_render = True
                hidden += 1

        self.report({'INFO'}, f"Hid {hidden} unique-named objects.")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(OBJECT_OT_hide_unique_base_name.bl_idname, icon="HIDE_OFF")

def draw_func(self, context):
    self.layout.operator(OBJECT_OT_select_by_base_name.bl_idname)
    self.layout.operator(OBJECT_OT_rename_selected_unique.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_select_by_base_name)
    bpy.utils.register_class(OBJECT_OT_rename_selected_unique)
    bpy.utils.register_class(OBJECT_OT_hide_unique_base_name)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_func)
    bpy.types.VIEW3D_MT_object_showhide.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_func)
    bpy.types.VIEW3D_MT_object_showhide.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_select_by_base_name)
    bpy.utils.unregister_class(OBJECT_OT_rename_selected_unique)
    bpy.utils.unregister_class(OBJECT_OT_hide_unique_base_name)

if __name__ == "__main__":
    register()
