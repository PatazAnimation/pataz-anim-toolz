bl_info = {
	'name': 'Pataz Anim Toolz',
	'author': 'Beorn Leonard <beorn@patazanimation.com>, Daniel Salazar <support@blenderaddon.com>',
	'version': (0, 1),
	'blender': (2, 80, 0),
	'location': 'Toolbar > Pataz',
	'description': 'Animation Tools',
	'wiki_url': 'http://blenderaddon.com/',
	'category': 'Animation',
}

import bpy
import addon_utils

# --- PROPERTIES

Pataz_mw = ''
Pataz_mr = ''

class PatazAnim (bpy.types.PropertyGroup):
	
	# Rigify properties
	
	example_enum : bpy.props.EnumProperty (
	name = 'Example Enum',
	description = 'Set the description here',
	items =[('default', 'Default', 'Leave it unchanged'),
			('one', 'One', 'One case'),
			('another', 'Another', 'Another case')],
	default = 'default',
	options = set() # Non animatable
	)
	
	example_float : bpy.props.FloatProperty (
	name = 'Floaty McFloat',
	description = 'A number that floats',
	default = 0.0,
	min = 0.0,
	max = 1.0,
	options = set() # Non animatable
	)
	
	example_bool : bpy.props.BoolProperty (
	name = 'Toggle Me',
	description = 'Turn me on and off',
	default = False,
	options = set() # Non animatable
	)


bpy.utils.register_class(PatazAnim)

bpy.types.Object.Pataz_anim = bpy.props.PointerProperty(type = PatazAnim)

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

def insert_xform_key(obj,fr):
	obj.keyframe_insert(data_path='location', frame=fr, options={'INSERTKEY_AVAILABLE'})
	obj.keyframe_insert(data_path='rotation_quaternion', frame=fr, options={'INSERTKEY_AVAILABLE'})
	obj.keyframe_insert(data_path='rotation_euler', frame=fr, options={'INSERTKEY_AVAILABLE'})
	obj.keyframe_insert(data_path='rotation_axis_angle', frame=fr, options={'INSERTKEY_AVAILABLE'})
	obj.keyframe_insert(data_path='scale', frame=fr, options={'INSERTKEY_AVAILABLE'})


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
		print (str(Pataz_mw))
		if ((obj.type == 'ARMATURE') & (obj.mode == 'POSE')):
			context.active_pose_bone.matrix =  context.active_object.matrix_world.inverted() @ Pataz_mw
		else:
			context.active_object.matrix_world = Pataz_mw
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
		global Pataz_mr
		obj_1 = context.active_pose_bone
		for obj in context.selected_pose_bones:
			if obj != obj_1:
				obj_2 = obj
		matrix_2 = obj_2.id_data.matrix_world @ obj_2.matrix
		obj_1.matrix = matrix_2 @ Pataz_mr
		if context.scene.tool_settings.use_keyframe_insert_auto:
			insert_xform_key(obj_1, context.scene.frame_current)

		return {'FINISHED'}

# --- PANELS

class PatazAnimToolz (bpy.types.Panel):
	bl_idname = 'OBJECT_PT_PatazAnimToolz'
	bl_label = 'Anim Toolz'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'Pataz'
	
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
	bl_category = 'Pataz'
	
	@classmethod
	def poll(cls, context):
		return (context.object)
	
	def draw_header(self, context):
		
		layout = self.layout
		row = layout.row()
		row.label (text = 'Toolz', icon = 'TOOL_SETTINGS')
	
	def draw(self, context):
		
		layout = self.layout
		
		row = layout.row()
		row.label(text="Transform Utils")
		row = layout.row()
		row.operator("scene.pataz_world_matrix_copy", text="Copy", icon="WORLD")
		row.operator("scene.pataz_world_matrix_paste", text="Paste", icon="WORLD")
		row = layout.row()
		row.operator("scene.pataz_rel_xform_copy", text="Copy", icon="GROUP_BONE")
		row.operator("scene.pataz_rel_xform_paste", text="Paste", icon="GROUP_BONE")

class PatazAnimToolzSelectionSetzPanel (bpy.types.Panel):
	bl_parent_id = 'OBJECT_PT_PatazAnimToolz'
	bl_idname = 'OBJECT_PT_PatazAnimToolzSelectionSetzPanel'
	bl_label = ''
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'Pataz'
	
	@classmethod
	def poll(cls, context):
		return (context.object.type=='ARMATURE') & addon_utils.check('bone_selection_sets')[0]
	
	def draw_header(self, context):
		
		layout = self.layout
		row = layout.row()
		row.label (text = 'Selection Setz', icon = 'ARMATURE_DATA')
	
	def draw(self, context):
		arm = context.object
		layout = self.layout
		
		row = layout.row()
		row.enabled = context.mode == 'POSE'

		# UI list
		rows = 4 if len(arm.selection_sets) > 0 else 1
		row.template_list(
			"POSE_UL_selection_set", "",  # type and unique id
			arm, "selection_sets",  # pointer to the CollectionProperty
			arm, "active_selection_set",  # pointer to the active identifier
			rows=rows
		)

		# add/remove/specials UI list Menu
		col = row.column(align=True)
		col.operator("pose.selection_set_add", icon='ADD', text="")
		col.operator("pose.selection_set_remove", icon='REMOVE', text="")
		col.menu("POSE_MT_selection_sets_context_menu", icon='DOWNARROW_HLT', text="")

		# move up/down arrows
		if len(arm.selection_sets) > 0:
			col.separator()
			col.operator("pose.selection_set_move", icon='TRIA_UP', text="").direction = 'UP'
			col.operator("pose.selection_set_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

		# buttons
		row = layout.row()

		sub = row.row(align=True)
		sub.operator("pose.selection_set_assign", text="Assign")
		sub.operator("pose.selection_set_unassign", text="Remove")

		sub = row.row(align=True)
		sub.operator("pose.selection_set_select", text="Select")
		sub.operator("pose.selection_set_deselect", text="Deselect")
		


class PatazAnimToolzSettingsPanel (bpy.types.Panel):
	bl_parent_id = 'OBJECT_PT_PatazAnimToolz'
	bl_idname = 'OBJECT_PT_PatazAnimSettingzPanel'
	bl_label = ''
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'Pataz'
	
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
		
		row = layout.row()
		row.label(text="Keying", icon="KEYINGSET")
		row = layout.row()
		row.prop(context.tool_settings, "use_keyframe_insert_auto", text="")
		row.prop_search(scene.keying_sets_all, "active", scene, "keying_sets_all", text="")
		row = layout.row()
		row.prop(context.preferences.edit, "keyframe_new_interpolation_type", text="")
		row = layout.row()
		row.prop(context.preferences.edit, "keyframe_new_handle_type", text="")
		row = layout.row()
		row.prop(tool_settings, "keyframe_type", text="")
		row = layout.row()
		row.prop(context.preferences.edit, "use_keyframe_insert_needed", text="Only Insert Needed")
		row = layout.row()
		row.prop(context.preferences.edit, "use_keyframe_insert_available", text="Only Insert Available")
		row = layout.row()
		row.prop(context.tool_settings, "use_keyframe_cycle_aware", text="Cycle Aware Keying")
		
		row = layout.row()
		row.label(text="Audio", icon="SOUND")
		row = layout.row()
		row.prop(context.scene, "use_audio", text="", icon='MUTE_IPO_OFF' if scene.use_audio else 'MUTE_IPO_ON')
		row.prop(context.scene, "use_audio_scrub", text="Scrubbing", icon="SEQ_HISTOGRAM")
		
		row = layout.row()
		row.label(text="Playback", icon="PLAY")
		row = layout.row()
		row.prop(context.scene, "sync_mode", text="")
		row = layout.row()
#		row.prop(context.scene, "frame_start", text="Start")
#		row.prop(context.scene, "frame_end", text="End")
		if not scene.use_preview_range:
			row.prop(scene, "frame_start", text="Start")
			row.prop(scene, "frame_end", text="End")
		else:
			row.prop(scene, "frame_preview_start", text="Start")
			row.prop(scene, "frame_preview_end", text="End")
		
		row = layout.row()
		row.label(text="Optimisation", icon="ALIASED")
		row = layout.row()
		row.prop(context.scene.render, "use_simplify", text="Simplify")
		row.prop(context.scene.render, "simplify_subdivision", text="levels")
		



class PatazAnimToolzLinks (bpy.types.Panel):
	bl_parent_id = 'OBJECT_PT_PatazAnimToolz'
	bl_idname = 'OBJECT_PT_PatazAnimToolzLinks'
	bl_label = ''
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'Pataz'
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
#   	row = layout.row()
#   	row.operator('wm.url_open' ,text='Visit Blenderaddon', icon = 'URL').url = 'http://blenderaddon.com'
#   	row = layout.row()
#   	row.operator('wm.url_open', text='Follow us on Twitter', icon = 'BOIDS').url = 'https://twitter.com/BlenderAddon'
#   	row = layout.row()
#   	row.operator('wm.url_open', text='Subscribe on Youtube', icon = 'PLAY').url = 'https://www.youtube.com/channel/UC7mRQZPoClDI3TD2eArLOCA'

# --- REGISTER

classes = (
	PatazAnimToolz,
	PatazAnimToolzOperatorPanel,
	PatazAnimToolzSettingsPanel,
	PatazAnimToolzSelectionSetzPanel,
	PatazAnimToolzLinks,
	
	Pataz_world_matrix_copy,
	Pataz_world_matrix_paste,
	Pataz_rel_xform_copy,
	Pataz_rel_xform_paste,

)
 
reg_cls, unreg_cls = bpy.utils.register_classes_factory (classes)
 
 
def register():
	reg_cls()
 
def unregister():
	unreg_cls()
 
if __name__ == '__main__':
	register()
