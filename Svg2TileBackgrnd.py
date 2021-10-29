bl_info = {
    "name": "Svg2TileBackgrnd",
    "blender": (2, 83, 0),
    "category": "Object",
}


import bpy
import bmesh
import numpy as np

class ObjectSvg2TileBackgrnd(bpy.types.Operator):
    """Object Svg2TileBackgrnd"""
    bl_idname = "object.svg2tilebackgrnd"
    bl_label = "Svg2TileBackgrnd"
    bl_options = {'REGISTER', 'UNDO'}

    #total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)
    #FloatProperty(name="", description="", default=0.0, min=-3.402823e+38, max=3.402823e+38, soft_min=-3.402823e+38, soft_max=3.402823e+38, step=3, precision=2, options={'ANIMATABLE'}, tags={}, subtype='NONE', unit='NONE', update=None, get=None, set=None)
    thresh_low: bpy.props.FloatProperty(name="thresh_low" 
                                        , description="all svg curves with areas below median*thresh_low are Artifacts (no Tiles)" 
                                        , default=0.25 
                                        , min=0.01, max=1.00 
                                        , soft_min=0.01, soft_max=1.00
                                        , step=2, precision=2
                                        , options={'ANIMATABLE'}, subtype='NONE'
                                        , unit='NONE', update=None, get=None, set=None)
    #thresh_low = 0.25
    thresh_high: bpy.props.FloatProperty(name="thresh_high" 
                                        , description="all svg curves with areas higher as  median*thresh_high are Background (no Tiles)" 
                                        , default=4.00 
                                        , min=1.00, max=40.00 
                                        , soft_min=1.00, soft_max=40.00
                                        , step=5, precision=1
                                        , options={'ANIMATABLE'}, subtype='NONE'
                                        , unit='NONE', update=None, get=None, set=None)

    #thresh_high = 4
    USE_FILTER_FACES = True

    def is_face_skip(self, f):
        """Ignore faces that pass this test!"""
        return f.hide is False
        # You may want to filter based on material.
        # return f.material_index == 0

    def bmesh_from_object_final(self, ob):
        matrix = ob.matrix_world
        #me = ob.to_mesh(bpy.context.scene, apply_modifiers=True, settings='PREVIEW')
        me = ob.to_mesh(preserve_all_data_layers=True, depsgraph=None)
        me.transform(matrix)
        bm = bmesh.new()
        bm.from_mesh(me)
        #bpy.data.meshes.remove(me)
        if self.USE_FILTER_FACES:
            faces_remove = [f for f in bm.faces if not self.is_face_skip(f)]
            for f in faces_remove:
                bm.faces.remove(f)
        return (bm, matrix.is_negative)

    def volume_and_area_from_object(self, ob):
        bm, is_negative = self.bmesh_from_object_final(ob)
        volume = bm.calc_volume(signed=True)
        area = sum(f.calc_area() for f in bm.faces)
        bm.free()
        if is_negative:
            volume = -volume
        return volume, area

    def execute(self, context):
        obj = bpy.context.selected_objects[0]
        #collection des ersten selektierten objects, heisst wie der SVG Import
        collection = obj.users_collection[0]
        
        for obj in collection.objects:
            if obj.name == 'Curve':
                bpy.data.objects['Curve'].name = 'Curve.000'
        
        area_d = {}
        area_sum = 0
        for obj in collection.objects:
            volume, area = self.volume_and_area_from_object(obj)
            if volume == 0 :
                area_sum += area
            area_d.update({obj.name: (area, volume)})

#        print('area_d: ', area_d)

        area_part_d = {}
        for obj in collection.objects:
            if area_d.get(obj.name)[1] == 0:
                area_part_d.update({obj.name: area_d.get(obj.name)[0]})
        area_part_mean = np.array(list(area_part_d.values())).mean()

#        thresh_low = 0.25
#        thresh_high = 4


        for obj in collection.objects:
            if area_d[obj.name][1] == 0: #kein Volume
                if area_d[obj.name][0] > area_part_mean*self.thresh_low and area_d[obj.name][0] < area_part_mean*self.thresh_high:
                    obj.name = "Tile." + obj.name.split('.')[1]
                    obj.select_set(False)
                elif area_d[obj.name][0] >=  area_part_mean*self.thresh_high:
                    obj.name = "Background." + obj.name.split('.')[1]
                    obj.select_set(False)
                elif area_d[obj.name][0] < area_part_mean*self.thresh_low:
                    obj.name = "Artifact." + obj.name.split('.')[1]
                    obj.select_set(True)

#        print('area_part_mean: ',area_part_mean)
#        print('area_part_mean*thresh_low: ', area_part_mean*self.thresh_low)
#        print('area_part_mean*thresh_high: ', area_part_mean*self.thresh_high)
        
            

        return {'FINISHED'}

# def menu_func(self, context):
    # self.layout.operator(ObjectSvg2TileBackgrnd.bl_idname)

# def register():
    # bpy.utils.register_class(ObjectSvg2TileBackgrnd)
    # bpy.types.VIEW3D_MT_object.append(menu_func)
    
# def unregister():
    # bpy.utils.unregister_class(ObjectSvg2TileBackgrnd)
    # bpy.types.VIEW3D_MT_object.remove(menu_func)
    
# if __name__ == "__main__":
    # register()