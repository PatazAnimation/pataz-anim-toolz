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
import mathutils

# --- PROPERTIES

Pataz_mw = ''
Pataz_mr = ''

class PatazAnimProps (bpy.types.PropertyGroup):

    frame_step : bpy.props.IntProperty (
    name = 'frame step',
    description = 'Frame Step for Baking',
    default = 1,
    min = 1,
    max = 50,
    options = set() # Non animatable
    )
    
    paste_to_keys : bpy.props.BoolProperty (
    name = 'Existing keys only',
    description = 'Only bake to existing keys',
    default = False,
    options = set() # Non animatable
    )


bpy.utils.register_class(PatazAnimProps)
bpy.types.Scene.pataz_anim = bpy.props.PointerProperty(type = PatazAnimProps)

# --- FUNCTIONS

def vaildate_rel_xform():
    valid = True
    if bpy.context.active_object is not None:
        for obj in bpy.context.selected_objects:
            if (obj.mode != 'POSE'):
                valid = False
        if valid:
            if len(bpy.context.selected_pose_bones) != 2:
                valid = False
    else:
        valid = False
    return valid

def findChildOf(obj):
    childOf = []
    i = 0
    for con in obj.constraints:
        if con.type == 'CHILD_OF':
            if con.enabled and con.influence == 1.0:
                print("ChildOf constraint "+str(i+1)+" found")
                print(con.influence)

                ChildOf_target = con.target
                if con.subtarget:
                    print("ChildOf parent is a bone.")
                    childOf_parent = ChildOf_target.matrix_world @ ChildOf_target.pose.bones[con.subtarget].matrix
                else:
                    print("ChildOf parent is an object.")
                    childOf_parent = ChildOf_target.matrix_world

                childOf_inv = con.inverse_matrix

                basis = childOf_parent @ childOf_inv
                childOf_new = [con.name, basis]
                childOf.append(childOf_new)
                i += 1
    return childOf

def paste_relative(context, key=True):
    global Pataz_mr
    obj_1 = context.active_pose_bone

    childOf = findChildOf(obj_1)
    if len(childOf) != 0:
        basis = childOf[0][1]
        for i in range(1, len(childOf)):
            basis = basis @ childOf[i][1]
        childOf = True

    for obj in context.selected_pose_bones:
        if obj != obj_1:
            obj_2 = obj
    matrix_2 = obj_2.id_data.matrix_world @ obj_2.matrix

    if childOf:
        obj_1.matrix = basis.inverted() @ matrix_2 @ Pataz_mr
    else:
        obj_1.matrix = matrix_2 @ Pataz_mr
            
#    print("Pasted relative Xform matrix: "+str(obj_1.matrix))
    context.view_layer.update()

    if key:
        insert_xform_key(obj_1, context.scene.frame_current)


def insert_xform_key(obj,fr, key_options='INSERTKEY_AVAILABLE'):
    rot_mode = obj.rotation_mode
    obj.keyframe_insert(data_path='location', frame=fr, options={key_options})
    if rot_mode == 'QUATERNION':
        obj.keyframe_insert(data_path='rotation_quaternion', frame=fr, options={key_options})
    elif rot_mode == 'AXIS_ANGLE':
        obj.keyframe_insert(data_path='rotation_axis_angle', frame=fr, options={key_options})
    else:
        obj.keyframe_insert(data_path='rotation_euler', frame=fr, options={key_options})
    obj.keyframe_insert(data_path='scale', frame=fr, options={key_options})
#    print("Inserted key at "+str(fr))


def get_keyed_frames():
    frames = []
    fcurves = bpy.context.active_object.animation_data.action.fcurves
    bones = bpy.context.selected_pose_bones
    bones = [b.name for b in bones]

    fcurves_selected = [f for f in fcurves if f.data_path.split('"')[1] in bones]
    for fcu in fcurves:
        for kf in fcu.keyframe_points:
            frames.append(int(kf.co[0]))

    print(frames)
    return frames

# --- OPERATORS

class Pataz_world_matrix_copy(bpy.types.Operator):
    """Copy the world coordinates of the active object or bone"""
    bl_idname = "scene.pataz_world_matrix_copy"
    bl_label = "Copy World Matrix"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        global Pataz_mw
        print (str(Pataz_mw))
        if ((obj.type == 'ARMATURE') & (obj.mode == 'POSE')):
            Pataz_mw = obj.matrix_world @ context.active_pose_bone.matrix
        else:
            Pataz_mw = obj.matrix_world.copy()
        print (str(Pataz_mw))
        return {'FINISHED'}

class Pataz_rel_xform_copy(bpy.types.Operator):
    """Copy the relative coordinates of the selected bone to the active bone.\nMust have exactly 2 bones selected"""
    bl_idname = "scene.pataz_rel_xform_copy"
    bl_label = "Copy Relative Transform"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return vaildate_rel_xform()

    def execute(self, context):
        global Pataz_mr
        obj_1 = context.active_pose_bone
        for obj in context.selected_pose_bones:
            if obj != obj_1:
                obj_2 = obj
        matrix_1 = obj_1.id_data.matrix_world @ obj_1.matrix
        matrix_2 = obj_2.id_data.matrix_world @ obj_2.matrix
        Pataz_mr = matrix_2.inverted() @ matrix_1
        return {'FINISHED'}

class Pataz_world_matrix_paste(bpy.types.Operator):
    """Paste the world coordinates of the active object or bone"""
    bl_idname = "scene.pataz_world_matrix_paste"
    bl_label = "Paste World Matrix"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None) & (Pataz_mw != '')

    def execute(self, context):
        obj = context.active_object
        global Pataz_mw

        bone = False
        if ((obj.type == 'ARMATURE') & (obj.mode == 'POSE')):
            bone = True
            arm = obj
            obj = context.active_pose_bone
            target_matrix = obj.matrix
        else:
            target_matrix = obj.matrix_world

        childOf = findChildOf(obj)

        if len(childOf) != 0:
            print("ChildOf constraint(s) found")
            basis = childOf[0][1]
            
            for i in range(1, len(childOf)):
                basis = basis @ childOf[i][1]
            
            if bone:
                obj.matrix = basis.inverted() @ Pataz_mw
            else:
                obj.matrix_world = basis.inverted() @ Pataz_mw
        else:
            print("ChildOf constraint not found")
            if bone:
                obj.matrix =  arm.matrix_world.inverted() @ Pataz_mw
            else:
                obj.matrix_world = Pataz_mw

        if context.scene.tool_settings.use_keyframe_insert_auto:
            insert_xform_key(obj, context.scene.frame_current)

        return {'FINISHED'}

class Pataz_rel_xform_paste(bpy.types.Operator):
    """Paste the relative coordinates of the selected bone to the active bone\nMust have exactly 2 bones selected"""
    bl_idname = "scene.pataz_rel_xform_paste"
    bl_label = "Paste Relative Transform"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        global Pataz_mr
        if Pataz_mr != '':
            return vaildate_rel_xform()
        else :
            return False

    def execute(self, context):
        key = False
        if context.scene.tool_settings.use_keyframe_insert_auto:
            key = True
        paste_relative(context, key)

        return {'FINISHED'}

class Pataz_rel_xform_paste_anim(bpy.types.Operator):
    """Paste the relative coordinates of the selected bone to the active bone\nMust have exactly 2 bones selected"""
    bl_idname = "scene.pataz_rel_xform_paste_anim"
    bl_label = "Paste Relative Transform - Timeline"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        global Pataz_mr
        if Pataz_mr != '':
            return vaildate_rel_xform()
        else :
            return False

    def execute(self, context):
        scene = bpy.context.scene
        paste_to_keys = scene.pataz_anim.paste_to_keys
        frame_step = scene.pataz_anim.frame_step
        frames = []


        curr_time = scene.frame_current
        obj = context.active_pose_bone
        start = scene.frame_start
        end = scene.frame_end
        
        if scene.use_preview_range:
            start = scene.frame_preview_start
            end = scene.frame_preview_end

        if paste_to_keys:
            frames = get_keyed_frames()

        else:
            frames.append(start)
            for fr in range(start, end):
                if ((fr-start)/frame_step).is_integer():
                    frames.append(fr) 

        bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_VisualLocRotScale")


        for fr in frames:
            scene.frame_current = fr
            context.view_layer.update()
            paste_relative(context)

        scene.frame_current = curr_time            

        return {'FINISHED'}

class Pataz_paste_timeline_popup(bpy.types.Operator):
    """Paste transform to the timeline"""
    bl_idname = "scene.pataz_paste_timeline_options"
    bl_label = "Paste Timeline Options"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        global Pataz_mr
        if Pataz_mr != '':
            return vaildate_rel_xform()
        else :
            return False


    def draw(self, context):
        scene = context.scene

        layout = self.layout
        layout.ui_units_x = 8

        row = layout.row()
        row.prop(scene.pataz_anim,"frame_step")
        row = layout.row()
        row.prop(scene.pataz_anim,"paste_to_keys")
        row = layout.row()
        row.operator("scene.pataz_rel_xform_paste_anim", text="Paste", icon="TIME")

    def execute(self, context):
        return {'FINISHED'}
 
    def invoke(self, context, event):
#        context.object.active_selection_set = self.index
        return context.window_manager.invoke_popup(self)

# --- REGISTER

classes = (
    Pataz_world_matrix_copy,
    Pataz_world_matrix_paste,
    Pataz_rel_xform_copy,
    Pataz_rel_xform_paste,
    Pataz_rel_xform_paste_anim,
    Pataz_paste_timeline_popup
)
 
reg_cls, unreg_cls = bpy.utils.register_classes_factory (classes)
 
 
def register():
    reg_cls()
 
def unregister():
    unreg_cls()
 
if __name__ == '__main__':
    register()
