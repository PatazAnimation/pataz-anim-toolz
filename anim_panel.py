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

# Pataz Anim Toolz v0.7

import bpy

# --- PANELS

class PatazAnimToolz (bpy.types.Panel):
    bl_idname = 'OBJECT_PT_PatazAnimToolz'
    bl_label = 'Anim Toolz'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Anim'
    
    @classmethod
    def poll(cls, context):
        return (context.object)
    
    def draw(self, context):
        pass

class PatazAnimToolzOperatorPanel (bpy.types.Panel):
    bl_parent_id = 'OBJECT_PT_PatazAnimToolz'
    bl_idname = 'OBJECT_PT_PatazAnimToolzPanel1'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Anim'
    
    @classmethod
    def poll(cls, context):
        return (context.object)
    
    def draw_header(self, context):
        
        layout = self.layout
        row = layout.row()
        row.label (text = 'Toolz', icon = 'TOOL_SETTINGS')
    
    def draw(self, context):
        
        layout = self.layout
        
        box = layout.box()
        box.label(text="Transform Utils")
        row = box.row()
        row.operator("scene.pataz_world_matrix_copy", text="Copy world coords", icon="WORLD")
        row = box.row()
        row.operator("scene.pataz_world_matrix_paste", text="Paste world coords", icon="WORLD")
        row = box.row()
        row.operator("scene.pataz_rel_xform_copy", text="Copy relative coords", icon="GROUP_BONE")
        row = box.row()
        row.operator("scene.pataz_rel_xform_paste", text="Paste relative coords", icon="GROUP_BONE")
        row.operator("scene.pataz_paste_timeline_options", text="", icon="TIME")


class PatazAnimToolzSettingsPanel (bpy.types.Panel):
    bl_parent_id = 'OBJECT_PT_PatazAnimToolz'
    bl_idname = 'OBJECT_PT_PatazAnimSettingzPanel'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Anim'
    
    @classmethod
    def poll(cls, context):
        return (context.object)
    
    def draw_header(self, context):
        
        layout = self.layout
        row = layout.row()
        row.label (text = 'Settingz', icon = 'SETTINGS')
    
    def draw(self, context):
        
        object = context.object
        scene = context.scene
        tool_settings = context.tool_settings
        
        layout = self.layout
        
        box = layout.box()
        box.label(text="Keying", icon="KEYINGSET")
        row = box.row()
        row.prop(context.tool_settings, "use_keyframe_insert_auto", text="")
        row.prop_search(scene.keying_sets_all, "active", scene, "keying_sets_all", text="")
        row = box.row()
        row.prop(context.preferences.edit, "keyframe_new_interpolation_type", text="")
        row = box.row()
        row.prop(context.preferences.edit, "keyframe_new_handle_type", text="")
        row = box.row()
        row.prop(tool_settings, "keyframe_type", text="")
        row = box.row()
        row.prop(context.preferences.edit, "use_keyframe_insert_needed", text="Only Insert Needed")
        row = box.row()
        row.prop(context.preferences.edit, "use_keyframe_insert_available", text="Only Insert Available")
        row = box.row()
        row.prop(context.tool_settings, "use_keyframe_cycle_aware", text="Cycle Aware Keying")
        
        box = layout.box()
        box.label(text="Playback", icon="PLAY")
        row = box.row()
        row.prop(context.scene, "sync_mode", text="")
        row = box.row()
        if not scene.use_preview_range:
            row.prop(scene, "frame_start", text="Start")
            row.prop(scene, "frame_end", text="End")
        else:
            row.prop(scene, "frame_preview_start", text="Start")
            row.prop(scene, "frame_preview_end", text="End")
        
        box = layout.box()
        box.label(text="Audio", icon="SOUND")
        row = box.row()
        row.prop(context.scene, "use_audio", text="Mute", icon='MUTE_IPO_OFF' if scene.use_audio else 'MUTE_IPO_ON')
        row.prop(context.scene, "use_audio_scrub", text="Scrubbing", icon="SEQ_HISTOGRAM")
        
        box = layout.box()
        box.label(text="Optimisation", icon="ALIASED")
        row = box.row()
        row.prop(context.scene.render, "use_simplify", text="Simplify")
        row.prop(context.scene.render, "simplify_subdivision", text="levels")
        



class PatazAnimToolzLinks (bpy.types.Panel):
    bl_parent_id = 'OBJECT_PT_PatazAnimToolz'
    bl_idname = 'OBJECT_PT_PatazAnimToolzLinks'
    bl_label = ''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Anim'
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll (cls, context):
        return (context.object is not None)
    
    def draw_header(self, context):
        
        layout = self.layout
        row = layout.row()
        row.label (text = 'Help & Links', icon = 'HEART')
    
    def draw(self, context):
        
        layout = self.layout
        
        row = layout.row()
        row.operator('wm.url_open', text='Read the Manual', icon = 'HELP').url = 'https://github.com/PatazAnimation/anim-toolz'

class PatazAnimSettingzHeaderPanel(bpy.types.Operator):
    bl_idname = "scene.pataz_anim_settingz_header_panel"
    bl_label = "Animation Settings"
    bl_options = {'REGISTER', 'UNDO'}
    
    index: bpy.props.IntProperty(
        name = 'index',
        default = 0,
        options={'HIDDEN'}
    )
    
    def draw(self, context):
        layout = self.layout
        layout.ui_units_x = 12

        object = context.object
        scene = context.scene
        tool_settings = context.tool_settings
       
        box = layout.box()
        box.label(text="Timeline", icon="TIME")
        row = box.row()
        if not scene.use_preview_range:
            row.prop(scene, "frame_start", text="Start")
            row.prop(scene, "frame_end", text="End")
        else:
            row.prop(scene, "frame_preview_start", text="Start")
            row.prop(scene, "frame_preview_end", text="End")
        box = layout.box()
        box.label(text="Keying", icon="KEYINGSET")
        row = box.row()
        row.prop(context.tool_settings, "use_keyframe_insert_auto", text="")
        row.prop_search(scene.keying_sets_all, "active", scene, "keying_sets_all", text="")
        row = box.row()
        row.prop(context.preferences.edit, "keyframe_new_interpolation_type", text="")
        row.prop(context.preferences.edit, "keyframe_new_handle_type", text="")
        row.prop(tool_settings, "keyframe_type", text="")
        row = box.row()
        row.prop(context.preferences.edit, "use_keyframe_insert_needed", text="Needed")
        row.prop(context.preferences.edit, "use_keyframe_insert_available", text="Available")
        row.prop(context.tool_settings, "use_keyframe_cycle_aware", text="Cycle Aware")
        
        box = layout.box()
        box.label(text="Playback", icon="PLAY")
        row = box.row()
        row.prop(context.scene, "sync_mode", text="")

        box = layout.box()
        box.label(text="Audio", icon="SOUND")
        row = box.row()
        row.prop(context.scene, "use_audio", text="Mute", icon='MUTE_IPO_OFF' if scene.use_audio else 'MUTE_IPO_ON')
        row.prop(context.scene, "use_audio_scrub", text="Scrubbing", icon="SEQ_HISTOGRAM")
        
        box = layout.box()
        box.label(text="Optimisation", icon="ALIASED")
        row = box.row()
        row.prop(context.scene.render, "use_simplify", text="Simplify")
        row.prop(context.scene.render, "simplify_subdivision", text="levels")

    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
#        context.object.active_selection_set = self.index
        return context.window_manager.invoke_popup(self)


class PatazAnimSettingzHeader(bpy.types.Panel):
    bl_space_type = "DOPESHEET"
    bl_region_type = 'HEADER'
    bl_category = 'Anim'
    bl_label = "Animation Settigz"
    bl_idname = "OBJECT_PT_pataz_anim_settings_header"
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'POSE'


def anim_header_button(self, context):
    layout = self.layout
    layout.operator('scene.pataz_anim_settingz_header_panel', text='', icon='SETTINGS')
#        layout.menu('pose.pataz_selection_sets_header_panel', text='Selection Sets', icon='GROUP_BONE')



classes = (
    PatazAnimToolz,
    PatazAnimToolzOperatorPanel,
    PatazAnimToolzSettingsPanel,
    PatazAnimToolzLinks,
    PatazAnimSettingzHeaderPanel
)
 
reg_cls, unreg_cls = bpy.utils.register_classes_factory (classes)
 
 
def register():
    reg_cls()
    bpy.types.DOPESHEET_HT_header.append(anim_header_button)
    bpy.types.GRAPH_HT_header.append(anim_header_button)
 
def unregister():
    unreg_cls()
 
if __name__ == '__main__':
    register()
