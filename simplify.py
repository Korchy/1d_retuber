# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_simplify
#
# Version history:
#   1.0. (2018.06.12) - start dev


bl_info = {
    'name': 'Simplify',
    'category': 'Mesh',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 79, 0),
    'location': 'The 3D_View window - T-panel - the 1D tab',
    'wiki_url': 'https://github.com/Korchy/1d_simplify',
    'tracker_url': 'https://github.com/Korchy/1d_simplify',
    'description': 'Simplify mesh'
}

import bpy


class Simplify:
    pass


class SimplifyPanel(bpy.types.Panel):
    bl_idname = 'simplify.panel'
    bl_label = 'Simplify'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'

    def draw(self, context):
        self.layout.operator('simplify.mesh', icon='NONE', text='Simplify mesh')
        pass


class SimplifyMesh(bpy.types.Operator):
    bl_idname = 'simplify.mesh'
    bl_label = 'Simplify mesh'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        Simplify.simplify_tube(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimplifyMesh)
    bpy.utils.register_class(SimplifyPanel)


def unregister():
    bpy.utils.unregister_class(SimplifyPanel)
    bpy.utils.unregister_class(SimplifyMesh)


if __name__ == '__main__':
    register()
