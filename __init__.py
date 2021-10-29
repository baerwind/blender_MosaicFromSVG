bl_info = {
    "name": "MosaicFromSVG",
    "author": "Hans Ulrich Baerwind",
    "location": "View3D > Add Mesh / Sidebar > Create Tab",
    "version": (0, 0, 1),
    "blender": (2, 83, 3),
    "description": "Generate mosaic tiles from a svg import",
    "doc_url": "",
    "category": "Add Mesh"
    }

import sys
import os

# ----------------------------------------------
# Import modules
# ----------------------------------------------
if "bpy" in locals():
    import importlib
    importlib.reload(Svg2TileBackgrnd)
    importlib.reload(TileSolidifyRemesh)
    importlib.reload(TileMatUVxyProjctionFromSVGImage)
    print("MosaicFromSVG: Reloaded multifiles")
else:
    from . import Svg2TileBackgrnd
    from . import TileSolidifyRemesh
    from . import TileMatUVxyProjctionFromSVGImage

    print("MosaicFromSVG: Reloaded multifiles")

# noinspection PyUnresolvedReferences
import bpy
# noinspection PyUnresolvedReferences
from bpy.props import (
        BoolProperty,
        FloatVectorProperty,
        IntProperty,
        FloatProperty,
        StringProperty,
        )
# noinspection PyUnresolvedReferences
from bpy.types import (
        AddonPreferences,
        Menu,
        Scene,
        VIEW3D_MT_mesh_add,
        WindowManager,
        )
# ----------------------------------------------------------
# Registration
# ----------------------------------------------------------


class MosaicFromSVG_MT_CustomMenuAdd(Menu):
    bl_idname = "VIEW3D_MT_mesh_custom_menu_add"
    bl_label = "MosaicFromSVG"

    # noinspection PyUnusedLocal
    def draw(self, context):
        self.layout.operator_context = 'INVOKE_REGION_WIN'
        self.layout.operator("object.svg2tilebackgrnd", text="Svg2TileBackgrnd")
        self.layout.operator("object.tilesolidifyremesh", text="TileSolidifyRemesh")
        self.layout.operator("object.tilematuvxyprojctionfromsvgimage", text="TileMatUVxyProjctionFromSVGImage")

# --------------------------------------------------------------
# Register all operators and panels
# --------------------------------------------------------------

# Define menu
# noinspection PyUnusedLocal
def MosaicFromSVGMenu_func(self, context):
    layout = self.layout
    layout.separator()
    self.layout.menu("VIEW3D_MT_mesh_custom_menu_add", icon="GROUP")

classes = (
    MosaicFromSVG_MT_CustomMenuAdd,
    Svg2TileBackgrnd.ObjectSvg2TileBackgrnd,
    TileSolidifyRemesh.ObjectTileSolidifyRemesh,
    TileMatUVxyProjctionFromSVGImage.TileMatUVxyProjctionFromSVGImage
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    VIEW3D_MT_mesh_add.append(MosaicFromSVGMenu_func)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    VIEW3D_MT_mesh_add.remove(MosaicFromSVGMenu_func)


if __name__ == '__main__':
    register()
