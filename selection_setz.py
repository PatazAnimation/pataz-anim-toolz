#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

import bpy
import addon_utils

# Operators
        
class pataz_set_select(bpy.types.Operator):
    """Select bones in the set. Shift to add, Ctrl to remove"""
    bl_idname = "pose.pataz_set_select"
    bl_label = "Select bones in set"
    bl_options = {'REGISTER', 'UNDO'}
    
    index: bpy.props.IntProperty(
        name = 'index',
        default = 0,
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        return (addon_utils.check('bone_selection_sets')[0])&(context.mode == 'POSE')
            
    def invoke(self, context, event):
        arm = context.active_object
        arm.active_selection_set = self.index
        if self.index == -1:
            idx = arm.active_selection_set
        else:
            idx = self.index
            sel_set = arm.selection_sets[idx]

        if (not event.shift)&(not event.ctrl):
            bpy.ops.pose.select_all(action='DESELECT')
        if not event.ctrl:
            for bone in arm.data.bones:
                if bone.name in sel_set.bone_ids:
                    bone.select = True            
        else:
            for bone in arm.data.bones:
                if bone.name in sel_set.bone_ids:
                    bone.select = False

        return {'FINISHED'}

    def execute(self, context):
        arm = context.object
        arm.selection_sets[self.index].name = self.set_name
        return {'FINISHED'}

class pataz_set_new(bpy.types.Operator):
    """Creates a new selection set with the current selection."""
    bl_idname = "pose.pataz_set_new"
    bl_label = "Create new selection set"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty(
        name = 'name',
        default = 'Selection Set'
    )

    @classmethod
    def poll(cls, context):
        return (addon_utils.check('bone_selection_sets')[0])&(context.mode == 'POSE')

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_popup(self, event)
    
    def draw(self,context):
        layout = self.layout
        layout.prop(self,"name")
            
    def execute(self, context):
        arm = context.object
        bpy.ops.pose.selection_set_add()
        bpy.ops.pose.selection_set_assign()
        i = arm.active_selection_set.numerator
        arm.selection_sets[i].name = self.name

        return {'FINISHED'}

class pataz_sets_copy(bpy.types.Operator):
    """Copies the selection sets to the clipboard."""
    bl_idname = "pose.pataz_sets_copy"
    bl_label = "Copy selection sets."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (addon_utils.check('bone_selection_sets')[0])&(context.mode == 'POSE')
            
    def execute(self, context):
        arm = context.active_object
        for i in range( 0, len(arm.selection_sets), 1):
            print('fwarp')
            print(arm.selection_sets[i].name)
            arm.selection_sets[i].is_selected = True

        bpy.ops.pose.selection_set_copy()

        return {'FINISHED'}


class pataz_sets_enable(bpy.types.Operator):
    """Enable the official Blender selection sets addon"""
    bl_idname = "pose.pataz_sel_set_addon_enable"
    bl_label = "Enable selection sets"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        addon_utils.enable('bone_selection_sets', default_set=True)
        return {'FINISHED'}


# UI

class pataz_selection_sets_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Pataz'
    bl_label = "Selection Sets"
    bl_idname = "OBJECT_PT_le_selection_panel_ui"

    def draw(self, context):
        layout = self.layout
        arm = context.object
        layout.panel('pose.pataz_selection_buttons_ui')

class pataz_selection_sets_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Pataz'
    bl_label = "Bone Selection Sets"
    bl_idname = "OBJECT_PT_le_pataz_selection_set_buttons"
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'POSE'

    def draw(self, context):
        layout = self.layout
        arm = context.object

        # UI list
        row = layout.row()

        if (addon_utils.check('bone_selection_sets')[0]):
            row.operator('pose.pataz_sets_copy', text="Copy", icon="COPYDOWN")
            row.operator('pose.selection_set_paste', text="Paste", icon="PASTEDOWN")
            row.operator('pose.selection_set_delete_all', text="Clear", icon="CANCEL")

            box = layout.box()
            split = box.split(factor=0.9)
            col_1 = split.column()
            col_2 = split.column()
            for i in range( 0, len(arm.selection_sets), 1):
                set_name = arm.selection_sets[i].name
                button = col_1.operator('pose.pataz_set_select', text=set_name)
                button.index = i
                button = col_2.operator('pose.pataz_selection_set_options', text = '...')
                button.index = i
            row = layout.row()
            row.operator('pose.pataz_set_new', text="New", icon="PLUS")
        else:
            row.operator('pose.pataz_sel_set_addon_enable', text="Enable selection sets.")
            

class pataz_selection_set_options_popup(bpy.types.Operator):
    """Change the selection set"""
    bl_idname = "pose.pataz_selection_set_options"
    bl_label = "Selection Set Options"
    bl_options = {'REGISTER', 'UNDO'}
    
    index: bpy.props.IntProperty(
        name = 'index',
        default = 0,
        options={'HIDDEN'}
    )

    def draw(self, context):

        layout = self.layout
        layout.ui_units_x = 8

        row = layout.row()
        row.prop(context.object.selection_sets[self.index],"name", text='')
        row = layout.row()
        row.operator('pose.selection_set_assign', icon="ADD", text='Add selection')
        row = layout.row()
        row.operator('pose.selection_set_unassign', icon="REMOVE", text='Remove selection')
        row = layout.row()
        row.operator('pose.selection_set_remove', icon="PANEL_CLOSE", text='Delete set')

    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
        context.object.active_selection_set = self.index
        return context.window_manager.invoke_popup(self)

# Register classes

classes = (
    pataz_set_select,
    pataz_set_new,
    pataz_sets_copy,
    pataz_sets_enable,
    pataz_selection_sets_panel,
    pataz_selection_set_options_popup
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()
