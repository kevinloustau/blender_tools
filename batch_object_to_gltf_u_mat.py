bl_info = {
    "name": "Unique Mat to Object",
    "author": "Kevin Loustau",
    "blender": (3, 4, 0)
}

import bpy
import os

def remove_data_materials():
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)

# func create all materials
def assign_unique_mat():
    scene = bpy.context.scene
    for obj in scene.objects:
        material = bpy.data.materials.new(name=obj.name)
        obj.data.materials.clear()
        obj.data.materials.append(material)    

def exports_objects_to_gltf():
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
        obj.location = [0,0,0]
        view_layer.objects.active = obj
        name = bpy.path.clean_name(obj.name)
        fn = os.path.join(basedir, name)
        bpy.ops.export_scene.gltf(filepath=fn + ".glb", use_selection=True)
        obj.select_set(False)
        print("written:", fn)
        obj.location = previous_location
        
    view_layer.objects.active = obj_active

    for obj in selection:
        obj.select_set(True)


class BatchObjectToGLTFWithUniqueMat(bpy.types.Operator):
    """Batch Object-To-GLTF- with unique material"""  
    bl_idname = "object.batch_objects"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Objects -> Unique Mat -> Export GLTF"         # Display name in the interface.
    
    def execute(self, context): 
        remove_data_materials()
        assign_unique_mat()
        exports_objects_to_gltf()
        return {'FINISHED'}
    
def menu_func(self, context):
    self.layout.operator(BatchObjectToGLTFWithUniqueMat.bl_idname)

def register():
    bpy.utils.register_class(BatchObjectToGLTFWithUniqueMat)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(ObjectMoveX)



if __name__ == "__main__":
    register()


