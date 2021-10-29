bl_info = {
    "name": "TileMatUVxyProjctionFromSVGImage",
    "blender": (2, 83, 0),
    "category": "Object",
}


import os 
import bpy
from bpy.props import StringProperty, BoolProperty 
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator 
import bmesh
import numpy as np
from mathutils import Matrix, Vector

class TileMatUVxyProjctionFromSVGImage(Operator, ImportHelper):
    """Object TileMatUVxyProjctionFromSVGImage"""
    bl_idname = "object.tilematuvxyprojctionfromsvgimage"
    bl_label = "TileMatUVxyProjctionFromSVGImage"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty( default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp'
                                , options={'ANIMATABLE'} ) 
    uv_xy_projection: BoolProperty( name='UVxyProjction', description='UVxyProjction with xy xoordinates', default=True, )

    def create_new_mat_from_svg_coll(self, collection):
        name = collection.name
        if bpy.data.materials.find(name) >= 0:
            mat = bpy.data.materials[name]
        else:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
            
            
            imagefilename, extension = os.path.splitext(self.filepath)
            if extension in ['.jpg','.jpeg','.png','.tif','.tiff','.bmp']:
                imgpath = self.filepath 
                texImage.image = bpy.data.images.load(imgpath)
            mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
        return mat
    
    def find_obj_xy_minmax(self, obj):
        me = obj.data
        bm = bmesh.new()
        bm.from_mesh(me)
        #bm = bmesh.from_edit_mesh(me)
        x, y, z = np.array([v.co for v in bm.verts]).T
        bm.free()
        return x.min(), x.max(), y.min(), y.max()

    def find_collection_objs_minmax(self, collection):
        M = np.empty((2,2))
        for obj in list(collection.objects):
            if obj.type in ['MESH']:
                xmin, xmax, ymin, ymax = self.find_obj_xy_minmax(obj)
                #print('name, xmin, xmax, ymin, ymax: ', obj.name, xmin, xmax, ymin, ymax) 
                #M = np.array[[x.min(), x.max()], [y.min(), y.max()]]
                #M = np.array([[xmin, xmax], [ymin, ymax]])
                #print(M.shape)
                M = np.concatenate((M, np.array([[xmin, xmax], [ymin, ymax]])), axis = 1)
        x, y = M
        #print('Total x.min(), x.max(), y.min(), y.max():',x.min(), x.max(), y.min(), y.max())
        return x.min(), x.max(), y.min(), y.max()

    def project_obj_on_UV_with_xy(self, obj, transl_xyvec, scale_matrix):
        me = obj.data
        bm = bmesh.new()
        bm.from_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        
        # adjust uv coordinates
        for face in bm.faces:
            for loop in face.loops:
                loop_uv = loop[uv_layer]
                # use xy position of the vertex as a uv coordinate
                #scale
                loop_uv.uv = scale_matrix @ loop.vert.co.xy
                #translate
                loop_uv.uv += scale_matrix @ transl_xyvec

        bm.to_mesh(me)
        me.update()
        bm.free()
        


    def execute(self, context):
        obj = bpy.context.selected_objects[0]
        #collection name des ersten seletierten objects 
        collection = obj.users_collection[0]
        name = collection.name
        self.filename = name + '.png'

        mat = self.create_new_mat_from_svg_coll(collection)
        print('mat:', mat)
        
        xmin, xmax, ymin, ymax = self.find_collection_objs_minmax(collection)
        print('name, xmin, xmax, ymin, ymax: ', collection.name, xmin, xmax, ymin, ymax)

        #Scalen
        xfaktor =  xmax - xmin
        yfaktor =  ymax - ymin
        scale_matrix = Matrix.Diagonal(( 1/xfaktor, 1/yfaktor))

        # Verschieben
        xmove = 0 - xmin
        ymove = 0 - ymin    
        transl_xyvec = Vector((xmove, ymove))

        for obj in bpy.context.selected_objects:
            # Assign it to object
            if obj.data.materials:
                obj.data.materials[0] = mat
                self.project_obj_on_UV_with_xy(obj, transl_xyvec, scale_matrix)
            else:
                obj.data.materials.append(mat)
                self.project_obj_on_UV_with_xy(obj, transl_xyvec, scale_matrix)
        
        return {'FINISHED'}

# def menu_func(self, context):
    # self.layout.operator(TileMatUVxyProjctionFromSVGImage.bl_idname)

# def register():
    # bpy.utils.register_class(TileMatUVxyProjctionFromSVGImage)
    # bpy.types.VIEW3D_MT_object.append(menu_func)
    
# def unregister():
    # bpy.utils.unregister_class(TileMatUVxyProjctionFromSVGImage)
    # bpy.types.VIEW3D_MT_object.remove(menu_func)
    
# if __name__ == "__main__":
    # register()