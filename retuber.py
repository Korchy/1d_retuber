# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_retuber
#
# Version history:
#   1.0. (2018.06.12) - start dev
#   1.1. (2018.06.18) - renamed to 'retuber'
#
# Known issues:
#   - cannot select loops on mesh cut


bl_info = {
    'name': 'Retuber',
    'category': 'Mesh',
    'author': 'Nikita Akimov',
    'version': (1, 1, 0),
    'blender': (2, 79, 0),
    'location': 'The 3D_View window - T-panel - the 1D tab',
    'wiki_url': 'https://github.com/Korchy/1d_retuber',
    'tracker_url': 'https://github.com/Korchy/1d_retuber',
    'description': 'Retuber'
}

import bpy
import bmesh


class Retuber:

    @staticmethod
    def get_parallel_loops(mesh):

        bpy.ops.object.mode_set(mode='OBJECT')

        loops = []
        bm = bmesh.new()
        bm.from_mesh(mesh.data)

        bm.edges.ensure_lookup_table()
        selected_edges = [edge for edge in bm.edges if edge.select]
        for edge in selected_edges:
            edge.tag = True

        bm.verts.ensure_lookup_table()
        selected_verts = [vert for vert in bm.verts if vert.select]
        if selected_verts :
            # print(selected_verts)
            # --- may be: to arange vertexes from one extreme and so on
            # find extreme vert
            extreme_vert = None
            for vert in selected_verts:
                taged_edges = [edge for edge in vert.link_edges if edge.tag]
                if len(taged_edges) == 1:
                    extreme_vert = vert
                    break
            extreme_vert = selected_verts[0] if not extreme_vert else extreme_vert    # for closed selection (no extreme vert) can start from any vert
            # from extreme moving to the end of the selection
            selected_verts = [extreme_vert]
            curr_vert = extreme_vert
            while(curr_vert):
                taged_edges = [edge for edge in curr_vert.link_edges if edge.tag]
                curr_vert = None
                for edge in taged_edges:
                    if edge.verts[0] not in selected_verts:
                        curr_vert = edge.verts[0]
                    if edge.verts[1] not in selected_verts:
                        curr_vert = edge.verts[1]
                if curr_vert:
                    selected_verts.append(curr_vert)
            # -- end may be : now selected vertexes guarantee ranged from extreme and so on
            # print(selected_verts)
            # from any vertex build continious selection loop (mark by 'tag')
            for vert in selected_verts:
                print('vert ', vert)
                vert_loop = []
                loops.append(vert_loop)
                for loop in vert.link_loops:
                    # from 3 to 3 - selection on mesh cut - prevent to continue selection direction
                    if len(vert.link_edges) != 4 and len(loop.edge.other_vert(vert).link_edges) != 4:
                        continue
                    # from 4 to 3 or 4 - prevent to continue selection direction
                    if len(vert.link_edges) == 4\
                            and loop.link_loop_radial_next.link_loop_next.link_loop_radial_next.link_loop_next.edge in selected_edges:
                        continue
                    next_loop = loop
                    while not next_loop.edge.tag:
                        next_loop.edge.tag = True
                        vert_loop.append(next_loop.edge.index)
                        next_loop = next_loop.link_loop_next.link_loop_radial_next.link_loop_next
                        if len(next_loop.vert.link_edges) != 4: # comes to mesh cut
                            break
        # bm.to_mesh(mesh.data)
        bm.free()
        return loops

    @staticmethod
    def get_perpendicular_loops(mesh):
        loops = []
        bm = bmesh.new()
        bm.from_mesh(mesh.data)



        # bm.to_mesh(mesh.data)
        bm.free()
        return loops


class RetuberPanel(bpy.types.Panel):
    bl_idname = 'retuber.panel'
    bl_label = 'Retuber'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'

    def draw(self, context):
        button = self.layout.operator('retuber.mesh', icon='NONE', text='Perpendicular')
        button.mode = True
        button = self.layout.operator('retuber.mesh', icon='NONE', text='Parallel')
        button.mode = False


class RetuberMesh(bpy.types.Operator):
    bl_idname = 'retuber.mesh'
    bl_label = 'Retuber mesh'
    bl_options = {'REGISTER', 'UNDO'}

    mode = bpy.props.BoolProperty(
        default=True
    )

    def execute(self, context):

        mesh = context.object

        if self.mode:
            lst = Retuber.get_parallel_loops(mesh)
        else:
            lst = Retuber.get_perpendicular_loops(mesh)

        # bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        print('all loops')
        print(lst)

        for i in range(0, len(lst), 1):
            for edge_index in lst[i]:
                mesh.data.edges[edge_index].select = True

        bpy.ops.object.mode_set(mode='EDIT')


        return {'FINISHED'}


def register():
    bpy.utils.register_class(RetuberMesh)
    bpy.utils.register_class(RetuberPanel)


def unregister():
    bpy.utils.unregister_class(RetuberPanel)
    bpy.utils.unregister_class(RetuberMesh)


if __name__ == '__main__':
    register()
