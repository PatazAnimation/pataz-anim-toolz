bl_info = {
	'name': 'Pataz Anim Toolz',
	'author': 'Daniel Salazar <support@blenderaddon.com>',
	'version': (0, 1),
	'blender': (2, 80, 0),
	'location': 'Toolbar > Pataz',
	'description': 'Animation Tools',
	'wiki_url': 'http://blenderaddon.com/',
	'category': 'Animation',
}

import bpy

# --- PROPERTIES

class PatazAnim (bpy.types.PropertyGroup):
	
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

bpy.types.Object.pataz_anim = bpy.props.PointerProperty(type = PatazAnim)


# --- OPERATORS

class PatazOperator (bpy.types.Operator):
	'''This operator does something'''
	bl_idname = 'object.pataz_operator'
	bl_label = 'Pataz Operator'
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		
		objects = context.selected_objects
		
		for object in objects:
			print (object.name)
			
		return {'FINISHED'}

class PatazStoreMatrix (bpy.types.Operator):
	'''Store the matrix of selected objects'''
	bl_idname = 'object.pataz_store_matrix'
	bl_label = 'Store Matrix'
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		
		objects = context.selected_objects
		
		for object in objects:
			object.pataz_anim['matrix'] = object.matrix_world
			
		return {'FINISHED'}

class PatazApplyMatrix (bpy.types.Operator):
	'''Apply the saved matrix of selected objects'''
	bl_idname = 'object.pataz_apply_matrix'
	bl_label = 'Apply Matrix'
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		
		objects = context.selected_objects
		
		for object in objects:
			object.matrix_world = object.pataz_anim['matrix']
			
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
		row.label (text = 'Operator Panel', icon = 'TOOL_SETTINGS')
	
	def draw(self, context):
		
		layout = self.layout
		
		row = layout.row()
		row.operator ('object.pataz_operator', icon = 'SHADING_RENDERED')
		column = layout.column(align = True)
		column.operator ('object.pataz_store_matrix', icon = 'FILE_TICK')
		column.operator ('object.pataz_apply_matrix', icon = 'FILE_REFRESH')

class PatazAnimToolzSettingsPanel (bpy.types.Panel):
	bl_parent_id = 'OBJECT_PT_PatazAnimToolz'
	bl_idname = 'OBJECT_PT_PatazAnimToolzPanel2'
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
		row.label (text = 'Settings Panel', icon = 'SETTINGS')
	
	def draw(self, context):
		
		object = context.object
		
		layout = self.layout
		
		row = layout.row()
		row.prop (object.pataz_anim, 'example_enum', expand = True)
		row = layout.row()
		row.prop (object.pataz_anim, 'example_float')
		row = layout.row()
		row.prop (object.pataz_anim, 'example_bool')

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
		row.operator('wm.url_open', text='Read the Manual', icon = 'HELP').url = 'https://blendermarket.com/products/anim-toolz/docs'
		row = layout.row()
		row.operator('wm.url_open' ,text='Visit Blenderaddon', icon = 'URL').url = 'http://blenderaddon.com'
		row = layout.row()
		row.operator('wm.url_open', text='Follow us on Twitter', icon = 'BOIDS').url = 'https://twitter.com/BlenderAddon'
		row = layout.row()
		row.operator('wm.url_open', text='Subscribe on Youtube', icon = 'PLAY').url = 'https://www.youtube.com/channel/UC7mRQZPoClDI3TD2eArLOCA'

# --- REGISTER

classes = (
	PatazAnimToolz,
	PatazAnimToolzOperatorPanel,
	PatazAnimToolzSettingsPanel,
	PatazAnimToolzLinks,
	
	PatazOperator,
	PatazStoreMatrix,
	PatazApplyMatrix
)
 
reg_cls, unreg_cls = bpy.utils.register_classes_factory (classes)
 
 
def register():
	reg_cls()
 
def unregister():
	unreg_cls()
 
if __name__ == '__main__':
	register()
