# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_retuber
#
# Version history:
#   0.0. (2018.06.12) - start dev
#   0.1. (2018.06.18) - renamed to 'retuber'
#   1.0. (2018.06.20) - first release
#   1.1. (2018.06.20) - Esc - esit without mesh modification; + All selection button - show all selected edges (para + perp)
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

    arrange_vert_selection = True
    environment = {
        'mesh_select_mode': None
    }

    @staticmethod
    def get_perpendicular_loops(bm):
        loops = []
        bm.edges.ensure_lookup_table()
        selected_edges = [edge for edge in bm.edges if edge.select]
        for edge in selected_edges:
            edge.tag = True
        bm.verts.ensure_lookup_table()
        selected_verts = [vert for vert in bm.verts if vert.select]
        # --- may be: to arange vertexes from one extreme and so on
        if __class__.arrange_vert_selection:
            selected_verts = __class__.get_arranged_verts_from_selection(bm)
        # -- end may be : now selected vertexes guarantee ranged from extreme and so on
        if selected_verts :
            # from any vertex build continious selection loop (mark by 'tag')
            for vert in selected_verts:
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
                        # vert_loop.append(next_loop.edge)
                        next_loop = next_loop.link_loop_next.link_loop_radial_next.link_loop_next
                        if len(next_loop.vert.link_edges) != 4:     # comes to mesh cut
                            break
        return loops

    @staticmethod
    def get_parallel_loops(bm):
        loops = []
        bm.edges.ensure_lookup_table()
        # selected edges - only with same count of edges on extreme verts (prevent if edge comes to mesh cut (from 4 verts to 3 in one edge)
        # selected_edges = [edge for edge in bm.edges if edge.select and len(edge.verts[0].link_loops) == len(edge.verts[1].link_loops)]
        selected_edges = [edge for edge in bm.edges if edge.select]
        for edge in selected_edges:
            edge.tag = True
        if selected_edges:
            # start selection (use only part not connected to mesh cut)
            # loops.append([edge.index for edge in selected_edges if len(edge.verts[0].link_loops) == len(edge.verts[1].link_loops) == 4])
            loops.append([edge.index for edge in selected_edges])
            # from extreme edge comes by link_loop_next.link_loop_next and so on
            curr_edge = __class__.get_extreme_edge(selected_edges)
            next_edge = curr_edge.link_loops[0].link_loop_next.link_loop_next.edge
            if len(next_edge.verts[0].link_loops) != 4 or len(next_edge.verts[1].link_loops) != 4:
                next_edge = curr_edge.link_loops[1].link_loop_next.link_loop_next.edge
            while next_edge:
                # if next_edge.tag or len(next_edge.verts[0].link_loops) != 4 or len(next_edge.verts[1].link_loops) != 4:   # closed or comes to mesh cut
                if next_edge.tag:   # closed or comes to mesh cut
                    break
                # get all edges from current edge (next_edge) - make loop checking parallel selection
                next_loop = [next_edge.index]
                loops.append(next_loop)
                next_edge_loop = next_edge.link_loops[0].link_loop_next.link_loop_radial_next.link_loop_next
                if not next_edge_loop.link_loop_next.link_loop_next.edge.tag and not next_edge_loop.link_loop_radial_next.link_loop_next.link_loop_next.edge.tag and len(next_edge.link_loops) > 1:
                    next_edge_loop = next_edge.link_loops[1].link_loop_next.link_loop_radial_next.link_loop_next
                if not next_edge_loop.link_loop_next.link_loop_next.edge.tag and not next_edge_loop.link_loop_radial_next.link_loop_next.link_loop_next.edge.tag:
                    next_edge_loop = None
                while next_edge_loop:
                    if next_edge_loop.edge.tag:     # loop selection is closed
                        break
                    next_edge_loop.edge.tag = True
                    next_loop.append(next_edge_loop.edge.index)
                    next_edge_loop = next_edge_loop.link_loop_next.link_loop_radial_next.link_loop_next
                    if not next_edge_loop.link_loop_next.link_loop_next.edge.tag and not next_edge_loop.link_loop_radial_next.link_loop_next.link_loop_next.edge.tag:
                        next_edge_loop = None
                    if next_edge_loop and len(next_edge_loop.vert.link_edges) != 4:  # comes to mesh cut
                        break
                next_edge.tag = True
                # get next edge
                if len(next_edge.link_loops) == 1:  # comes to mesh cut
                    break
                else:
                    next_edge_tmp = next_edge.link_loops[0].link_loop_next.link_loop_next.edge
                    # if mesh cut or already selected - try opposite direction
                    # if next_edge_tmp.tag or len(next_edge_tmp.verts[0].link_loops) != 4 or len(next_edge_tmp.verts[1].link_loops) != 4:
                    if next_edge_tmp.tag:
                        next_edge = next_edge.link_loops[1].link_loop_next.link_loop_next.edge
                    else:
                        next_edge = next_edge_tmp
        return loops

    @staticmethod
    def get_extreme_edge(edge_list):
        # return any extreme edge from edge list
        rez = None
        for edge in edge_list:
            l1 = len([edge for edge in edge.verts[0].link_edges if edge.tag])
            l2 = len([edge for edge in edge.verts[1].link_edges if edge.tag])
            if l1 == 1 or l2 == 1:
                rez = edge
        if not rez:     # closed selection - return any edge
            rez = edge_list[0]
        return rez

    @staticmethod
    def get_arranged_verts_from_selection(bm):
        # get the list of selected verts arranged by starting from one extreme and so on
        # selected edges mast be tagged (edge.tag = True)
        selected_verts = [vert for vert in bm.verts if vert.select]
        if selected_verts:
            # find extreme vert
            extreme_vert = None
            for vert in selected_verts:
                taged_edges = [edge for edge in vert.link_edges if edge.tag]
                if len(taged_edges) == 1:
                    extreme_vert = vert
                    break
            extreme_vert = selected_verts[0] if not extreme_vert else extreme_vert  # for closed selection (no extreme vert) can start from any vert
            # from extreme moving to the end of the selection
            selected_verts = [extreme_vert]
            curr_vert = extreme_vert
            while curr_vert:
                taged_edges = [edge for edge in curr_vert.link_edges if edge.tag]
                curr_vert = None
                for edge in taged_edges:
                    if edge.verts[0] not in selected_verts:
                        curr_vert = edge.verts[0]
                    if edge.verts[1] not in selected_verts:
                        curr_vert = edge.verts[1]
                if curr_vert:
                    selected_verts.append(curr_vert)
        return selected_verts

    @staticmethod
    def save_environment(context):
        __class__.environment['mesh_select_mode'] = context.tool_settings.mesh_select_mode[:]

    @staticmethod
    def restore_environment(context):
        context.tool_settings.mesh_select_mode = __class__.environment['mesh_select_mode']


class RetuberPanel(bpy.types.Panel):
    bl_idname = 'retuber.panel'
    bl_label = 'Retuber'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'

    def draw(self, context):
        self.layout.operator('retuber.start', icon='NONE', text='Start retube')
        # test
        self.layout.label(text='Select only:')
        row = self.layout.row()
        button = row.operator('retuber.test', icon='NONE', text='Paralel')
        button.mode = 0
        button = row.operator('retuber.test', icon='NONE', text='Perpendicular')
        button.mode = 1
        button = row.operator('retuber.test', icon='NONE', text='All')
        button.mode = 2


class RetuberMeshTest(bpy.types.Operator):
    bl_idname = 'retuber.test'
    bl_label = 'Test'
    bl_options = {'REGISTER', 'UNDO'}

    mode = bpy.props.IntProperty(
        default=0
    )

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        bm = bmesh.new()
        bm.from_mesh(context.object.data)
        para_loops = Retuber.get_parallel_loops(bm)
        bm.from_mesh(context.object.data)
        perp_loops = Retuber.get_perpendicular_loops(bm)
        bm.free()

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        if self.mode == 0:
            print('para select')
            print('para_loops', para_loops)
            # select para loops
            for loop in para_loops:
                for edge_index in loop:
                    context.object.data.edges[edge_index].select = True
        elif self.mode == 1:
            print('perp select')
            print('perp_loops', perp_loops)
            # select pert loops
            for loop in perp_loops:
                for edge_index in loop:
                    context.object.data.edges[edge_index].select = True
        elif self.mode == 2:
            print('all select')
            print('perp_loops', perp_loops)
            print('para_loops', para_loops)
            # select all loops
            for loop in perp_loops:
                for edge_index in loop:
                    context.object.data.edges[edge_index].select = True
            for loop in para_loops:
                for edge_index in loop:
                    context.object.data.edges[edge_index].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


class RetuberMesh(bpy.types.Operator):
    bl_idname = 'retuber.start'
    bl_label = 'Start retuber for work'
    bl_options = {'REGISTER', 'UNDO'}

    start_mesh_data = None
    para_loops = []
    para_iteration = 0
    perp_loops = []
    perp_iteration = 0

    def execute(self, context):
        Retuber.save_environment(context)
        context.tool_settings.mesh_select_mode = (False, True, False)   # select edges mode
        # get parallel/perpenducular loops
        if context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bm = bmesh.new()
        bm.from_mesh(context.object.data)
        self.para_loops = Retuber.get_parallel_loops(bm)
        bm.from_mesh(context.object.data)
        self.perp_loops = Retuber.get_perpendicular_loops(bm)
        bm.free()
        # cave mesh data to work with
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        self.start_mesh_data = context.object.data.copy()
        # switch to modal mode to interactive dissolving loops
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in ['WHEELUPMOUSE', 'WHEELDOWNMOUSE'] and (event.ctrl or event.shift):
            perp_loops_to_remove = []
            para_loops_to_remove = []
            if event.type == 'WHEELUPMOUSE':
                if event.shift:
                    self.perp_iteration -= 1
                    if self.perp_iteration < 0:
                        self.perp_iteration = 0
                elif event.ctrl:
                    self.para_iteration -= 1
                    if self.para_iteration < 0:
                        self.para_iteration = 0
            elif event.type == 'WHEELDOWNMOUSE':
                if event.shift:
                    self.perp_iteration += 1
                elif event.ctrl:
                    self.para_iteration += 1
            # dissolve edges
            # get edges to dissolve
            perp_loops = self.perp_loops[:]
            for i in range(self.perp_iteration):
                perp_loops_to_remove += perp_loops[::2]
                perp_loops = perp_loops[1::2]
            para_loops = self.para_loops[:]
            for i in range(self.para_iteration):
                para_loops_to_remove += para_loops[::2]
                para_loops = para_loops[1::2]
            # dissolve
            if context.object.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            context.object.data = self.start_mesh_data.copy()
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            # dissolve perp loops
            bpy.ops.object.mode_set(mode='OBJECT')
            for loop in perp_loops_to_remove:
                for edge_index in loop:
                    context.object.data.edges[edge_index].select = True
            bpy.ops.object.mode_set(mode='EDIT')
            # bpy.ops.mesh.dissolve_edges()
            # dissolve para loops
            bpy.ops.object.mode_set(mode='OBJECT')
            for loop in para_loops_to_remove:
                for edge_index in loop:
                    context.object.data.edges[edge_index].select = True
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.dissolve_edges()
        elif event.type in ('RET', 'NUMPAD_ENTER', 'ESC'):
            if event.type == 'ESC':
                # cancel modification
                if context.object.mode != 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')
                context.object.data = self.start_mesh_data.copy()
                bpy.ops.object.mode_set(mode='EDIT')
            # exit
            Retuber.restore_environment(context)
            return {'FINISHED'}
        return {'INTERFACE'}


def register():
    bpy.utils.register_class(RetuberMeshTest)
    bpy.utils.register_class(RetuberMesh)
    bpy.utils.register_class(RetuberPanel)


def unregister():
    bpy.utils.unregister_class(RetuberPanel)
    bpy.utils.unregister_class(RetuberMesh)
    bpy.utils.unregister_class(RetuberMeshTest)


if __name__ == '__main__':
    register()
