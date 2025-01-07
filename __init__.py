from .addons.MHW_CTC_CCL_Editor import register as addon_register, unregister as addon_unregister

bl_info = {
    "name": 'MHW CTC & CCL Editor',
    "author": 'NSA Cloud, AsteriskAmpersand, 诸葛不太亮',
    "blender": (2, 93, 0),
    "version": (1, 0),
    "description": 'Import, edit and export MHW ctc & ccl files.',
    "warning": '',
    "wiki_url": 'https://github.com/chikichikibangbang/MHW_CTC_CCL_Editor',
    "tracker_url": 'https://github.com/chikichikibangbang/MHW_CTC_CCL_Editor/issues',
    "category": 'Import-Export'
}

def register():
    addon_register()

def unregister():
    addon_unregister()

    