bl_info = {
    "name": "TileSolidifyRemesh",
    "blender": (2, 83, 0),
    "category": "Object",
}


import bpy


class ObjectTileSolidifyRemesh(bpy.types.Operator):
    """Object TileSolidifyRemesh"""
    bl_idname = "object.tilesolidifyremesh"
    bl_label = "TileSolidifyRemesh"
    bl_options = {'REGISTER', 'UNDO'}

    solidify_thickness: bpy.props.FloatProperty(name="solidify_thickness" 
                                        , description="Thickness of the shell (only Tiles)" 
                                        , default=0.01 
                                        , min=0.00, max=0.20 
                                        , soft_min=0.00, soft_max=0.20
                                        , step=1, precision=2
                                        , options={'ANIMATABLE'}, subtype='NONE'
                                        , unit='LENGTH', update=None, get=None, set=None)
    solidify_offset: bpy.props.FloatProperty(name="solidify_offset" 
                                        , description="Offset the thickness from the center (only Tiles)" 
                                        , default=1 
                                        , min=0.01, max=10.00 
                                        , soft_min=0.01, soft_max=10.00
                                        , step=2, precision=2
                                        , options={'ANIMATABLE'}, subtype='NONE'
                                        , unit='NONE', update=None, get=None, set=None)
    solidify_bevel_convex: bpy.props.FloatProperty(name="solidify_bevel_convex" 
                                        , description="Edge bevel weight to be added to outside edges (no Tiles)" 
                                        , default=0.01 
                                        , min=0.00, max=0.50 
                                        , soft_min=0.01, soft_max=0.50
                                        , step=1, precision=2
                                        , options={'ANIMATABLE'}, subtype='NONE'
                                        , unit='NONE', update=None, get=None, set=None)

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if obj.name[0:5]=='Tile.':
                #print('obj.name:', obj.name)
                bpy.ops.object.convert(target='MESH')
                obj.modifiers.new("Solidify",type='SOLIDIFY')
                obj.modifiers["Solidify"].thickness = self.solidify_thickness
                obj.modifiers["Solidify"].offset = self.solidify_offset
                obj.modifiers["Solidify"].bevel_convex = self.solidify_bevel_convex
                obj.modifiers.new('Remesh',type='REMESH')
                obj.modifiers['Remesh'].mode = 'SHARP'

                # Apply modifiers
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Solidify")
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")

                #Scale
        #        obj.scale[0] = 1
        #        obj.scale[1] = 1

        return {'FINISHED'}

# def menu_func(self, context):
    # self.layout.operator(ObjectTileSolidifyRemesh.bl_idname)

# def register():
    # bpy.utils.register_class(ObjectTileSolidifyRemesh)
    # bpy.types.VIEW3D_MT_object.append(menu_func)
    
# def unregister():
    # bpy.utils.unregister_class(ObjectTileSolidifyRemesh)
    # bpy.types.VIEW3D_MT_object.remove(menu_func)
    
# if __name__ == "__main__":
    # register()
