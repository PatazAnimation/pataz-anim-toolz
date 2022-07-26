bl_info = {
	'name': 'Pataz Anim Toolz',
	'author': 'Beorn Leonard , Daniel Salazar <support@blenderaddon.com>',
	'version': (0, 1),
	'blender': (2, 80, 0),
	'location': 'Toolbar > Pataz',
	'description': 'Animation Tools',
	'wiki_url': 'http://blenderaddon.com/',
	'category': 'Animation',
}

modulesNames = ['anim_panel', 'anim_toolz', 'selection_setz']
 
import sys
import importlib
 
modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)
 
def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
 
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()


