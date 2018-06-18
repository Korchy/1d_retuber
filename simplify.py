# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_simplify
#
# Version history:
#   1.0. (2018.06.12) - start dev
#
# Known issues:
#   - cannot select loops on mesh shear


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
import bmesh


class Simplify:

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
            print(selected_verts)

            # from any vertex build continious selection loop (mark by 'tag')
            # print(len(selected_verts))
            for vert in selected_verts:
                print('vert ', vert)
                vert_loop = []
                loops.append(vert_loop)

                # if len(vert.link_edges) != 4:
                #     continue

                print(len(vert.link_loops))

                for loop in vert.link_loops:
                    print('loop', loop)

                    # loop.link_loop_next.edge.select = True
                    # loop.edge.select = True
                    # vert_loop.append(loop.edge.index)

                    # print('')
                    # print('loop.edge', loop.edge, loop.edge.index)
                    # print('loop.link_loop_prev.edge', loop.link_loop_prev.edge, loop.link_loop_prev.edge.index)
                    # print('loop.link_loop_radial_prev.edge', loop.link_loop_radial_prev.edge, loop.link_loop_radial_prev.edge.index)
                    # print('loop.link_loop_prev.link_loop_radial_prev.edge', loop.link_loop_prev.link_loop_radial_prev.edge, loop.link_loop_prev.link_loop_radial_prev.edge.index)
                    # print('loop.link_loop_prev.link_loop_radial_prev.link_loop_prev.edge', loop.link_loop_prev.link_loop_radial_prev.link_loop_prev.edge, loop.link_loop_prev.link_loop_radial_prev.link_loop_prev.edge.index)

                    # if loop.link_loop_radial_prev.edge in selected_edges:
                    #     print('continue on loop.link_loop_prev.edge in selected edges', loop.link_loop_prev.edge.index)
                    #     continue

                    # if loop.link_loop_prev.link_loop_radial_prev.link_loop_prev.edge in selected_edges:
                    #     print('continue on loop.link_loop_prev.link_loop_radial_prev.link_loop_prev.edge in selected edges', loop.link_loop_prev.link_loop_radial_prev.link_loop_prev.edge.index)
                    #     continue

                    # loop.link_loop_next.link_loop_radial_next.link_loop_next.edge.select = True

                    # пробую через ребро - если ребро не принадлежит фейсу с еще одним ребром в selected - continue (это продолжение выделения)


                    next_loop = loop
                    # if next_loop.link_loop_prev.link_loop_radial_prev.link_loop_prev.edge in selected_edges:    # prevent continue in selection direction
                    # # if next_loop.link_loop_next.link_loop_radial_prev.link_loop_prev.edge in selected_edges:    # prevent continue in selection direction
                    #     print('in selected_edges')
                    #     continue

                    # next_loop.link_loop_next.link_loop_radial_next.link_loop_next.edge.select = True
                    # print(next_loop.link_loop_next.vert)

                    # if len(next_loop.link_loop_next.vert.link_edges) != 4:
                    # # if len(next_loop.vert.link_edges) != 4:
                    #     continue

                    if len(vert.link_edges) != 4 and len(next_loop.link_loop_next.vert.link_edges) != 4:
                    # if len(next_loop.vert.link_edges) != 4:
                        continue

                    # next_loop.link_loop_next.link_loop_radial_next.link_loop_next.vert.select = True

                    # prevent running loop aroun face on mesh shear - have issue: cannot select loops on mesh shear
                    # if len(next_loop.link_loop_next.vert.link_edges) != 4:
                    #     print('len(next_loop.vert.link_edges)', len(next_loop.link_loop_next.vert.link_edges))

                    # if len(next_loop.vert.link_edges) != 4:
                    #     print('len(next_loop.vert.link_edges)', len(next_loop.vert.link_edges))
                    #     if next_loop.edge not in selected_edges:
                    #         next_loop.edge.tag = True
                    #         vert_loop.append(next_loop.edge.index)
                    #     continue

                    # while not next_loop.edge.tag and len(next_loop.vert.link_edges) == 4:
                    # while not next_loop.edge.tag and len(next_loop.link_loop_next.vert.link_edges) == 4:
                    while not next_loop.edge.tag:
                        # if len(next_loop.link_loop_next.vert.link_edges) != 4:
                        #     print('while len', len(next_loop.link_loop_next.vert.link_edges))
                        #     break
                        # print('next_loop', next_loop)
                        next_loop.edge.tag = True
                        vert_loop.append(next_loop.edge.index)
                        next_loop = next_loop.link_loop_next.link_loop_radial_next.link_loop_next
                        # next_loop = next_loop.link_loop_next
                        if len(next_loop.vert.link_edges) != 4:
                            # print('while len', len(next_loop.vert.link_edges))
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


class SimplifyPanel(bpy.types.Panel):
    bl_idname = 'simplify.panel'
    bl_label = 'Simplify'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'

    def draw(self, context):
        button = self.layout.operator('simplify.mesh', icon='NONE', text='Perpendicular')
        button.mode = True
        button = self.layout.operator('simplify.mesh', icon='NONE', text='Parallel')
        button.mode = False


class SimplifyMesh(bpy.types.Operator):
    bl_idname = 'simplify.mesh'
    bl_label = 'Simplify mesh'
    bl_options = {'REGISTER', 'UNDO'}

    mode = bpy.props.BoolProperty(
        default=True
    )

    def execute(self, context):

        mesh = context.object

        if self.mode:
            lst = Simplify.get_parallel_loops(mesh)
        else:
            lst = Simplify.get_perpendicular_loops(mesh)

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
    bpy.utils.register_class(SimplifyMesh)
    bpy.utils.register_class(SimplifyPanel)


def unregister():
    bpy.utils.unregister_class(SimplifyPanel)
    bpy.utils.unregister_class(SimplifyMesh)


if __name__ == '__main__':
    register()
