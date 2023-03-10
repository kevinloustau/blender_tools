import os
import bpy

bl_info = {
    "name": "Super Mostache",
    "blender": (3, 4, 0),
    'version': (0, 0, 1),
    'author': 'Kevin Loustau',
    'description': 'Super Mostache',
}


EXPORT_PATH = ""


def remove_data_materials():
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)


def assign_unique_mat():
    scene = bpy.context.scene
    for obj in scene.objects:
        material = bpy.data.materials.new(name=obj.name)
        obj.data.materials.clear()
        obj.data.materials.append(material)


def export_objects_to(format):
    # export to blend file location
    basedir = os.path.dirname(bpy.data.filepath)

    if not basedir:
        raise Exception("Blend file is not saved")

    view_layer = bpy.context.view_layer

    obj_active = view_layer.objects.active
    selection = bpy.context.selected_objects

    bpy.ops.object.select_all(action='DESELECT')

    for obj in selection:

        obj.select_set(True)
        previous_location = obj.location.copy()
        obj.location = [0, 0, 0]
        view_layer.objects.active = obj
        name = bpy.path.clean_name(obj.name)
        fn = os.path.join(basedir, name)

        match format:
            case "gltf":
                bpy.ops.export_scene.gltf(
                    filepath=fn + ".glb", use_selection=True)
            case "obj":
                bpy.ops.export_scene.obj(
                    filepath=fn + ".obj", use_selection=True)

        obj.select_set(False)
        print("written:", fn)
        obj.location = previous_location

    view_layer.objects.active = obj_active

    for obj in selection:
        obj.select_set(True)


class ExportGltf(bpy.types.Operator):
    """Export to Gltf"""
    bl_idname = "object.export_gltf"        # Unique identifier for buttons and menu items to reference.
    # Display name in the interface.
    bl_label = "Export to GLTF"

    def execute(self, context):
        export_objects_to("gltf")
        return {'FINISHED'}


class ExportObj(bpy.types.Operator):
    """Export to Gltf"""
    bl_idname = "object.export_obj"        # Unique identifier for buttons and menu items to reference.
    # Display name in the interface.
    bl_label = "Export to OBJ"

    def execute(self, context):
        export_objects_to("obj")
        return {'FINISHED'}


class UniqueMat(bpy.types.Operator):
    """Assign unique mat"""
    bl_idname = "object.uniquemat"
    bl_label = "Set unique mat"

    def execute(self, context):
        remove_data_materials()
        assign_unique_mat()
        return {'FINISHED'}


class SP_TOOL_PANEL(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_SUPER_MOSTACHE'
    bl_label = 'Super Mostache'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Super Mostache'

    def draw(self, context):
        self.layout.label(text='Assign unique mat')
        self.layout.operator(UniqueMat.bl_idname, text='Unique Mat')
        self.layout.separator()
        self.layout.label(text='Export to Obj')
        self.layout.operator(ExportObj.bl_idname, text='Export OBJ')
        self.layout.label(text='Export to Gltf')
        self.layout.operator(ExportGltf.bl_idname, text='Export GLTF')


CLASSES = [
    UniqueMat,
    ExportGltf,
    ExportObj,
    SP_TOOL_PANEL,
]


def register():
    for klass in CLASSES:
        bpy.utils.register_class(klass)


def unregister():
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)


if __name__ == "__main__":
    register()
