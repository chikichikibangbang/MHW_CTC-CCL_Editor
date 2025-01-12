import bpy
import os
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty,PointerProperty
from bpy.types import Operator, OperatorFileListElement,AddonPreferences
from bpy_extras.io_utils import ExportHelper,ImportHelper
# from .preference.AddonPreferences import CTCCCLAddonPreferences
from ... import addon_updater_ops, addon_updater
from .config import __addon_name__
from .i18n.dictionary import dictionary
from .operators.import_export import ImportMHWCTC, ExportMHWCTC, ImportMHWCCL, ExportMHWCCL
from .properties.ctc_properties import CTCToolPanelPG, CTCHeaderPG, CTCSettingsPG, CTCNodePG, CTCClipboardPG, CCLPG
from ...common.class_loader import auto_load
from ...common.class_loader.auto_load import add_properties, remove_properties
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary
from .panels.AddonPanels import CTCToolsPanel, CTCToolsPoseModePanel, CTCHeaderPanel, CTCSettingsPanel, CTCNodePanel, \
    CTCClipboardPanel, CTCVisibilityPanel, CTCNodeVisPanel, CTCAngleLimitVisPanel, CTCColorVisPanel, CTCPresetPanel, \
    CollisionAttrFlagPanel, OtherSettingsPanel, ChainAttrFlagPanel, CCLCollisionVisPanel, ICONS_PATH, \
    preview_collections, CTCCredits, CTCIOPanel

# Add-on info
bl_info = {
    "name": "MHW CTC & CCL Editor",
    "author": "NSA Cloud, AsteriskAmpersand, 诸葛不太亮",
    "blender": (2, 93, 0),
    "version": (1, 1),
    "description": "Import, edit and export MHW ctc & ccl files.",
    "warning": "",
    "wiki_url": "https://github.com/chikichikibangbang/MHW_CTC_CCL_Editor",
    "tracker_url": "https://github.com/chikichikibangbang/MHW_CTC_CCL_Editor/issues",
    "category": "Import-Export"
}

_addon_properties = {}


# You may declare properties like following, framework will automatically add and remove them.
# Do not define your own property group class in the __init__.py file. Define it in a separate file and import it here.
# 注意不要在__init__.py文件中自定义PropertyGroup类。请在单独的文件中定义它们并在此处导入。
# _addon_properties = {
#     bpy.types.Scene: {
#         "property_name": bpy.props.StringProperty(name="property_name"),
#     },
# }

# Best practice: Please do not define Blender classes in the __init__.py file.
# Define them in separate files and import them here. This is because the __init__.py file would be copied during
# addon packaging, and defining Blender classes in the __init__.py file may cause unexpected problems.
# 建议不要在__init__.py文件中定义Blender相关的类。请在单独的文件中定义它们并在此处导入它们。
# __init__.py文件在代码打包时会被复制，在__init__.py文件中定义Blender相关的类可能会导致意外的问题。

panelclasses = [CTCIOPanel,
                CTCToolsPanel,
                CTCToolsPoseModePanel,
                CTCHeaderPanel,
                CTCSettingsPanel,
                CollisionAttrFlagPanel,
                ChainAttrFlagPanel,
                OtherSettingsPanel,
                CTCNodePanel, 
                CTCClipboardPanel,
                CTCPresetPanel,
                CTCVisibilityPanel, 
                CTCNodeVisPanel,
                CCLCollisionVisPanel,
                CTCAngleLimitVisPanel,
                CTCColorVisPanel,
                CTCCredits,
                ]


def mhw_ctc_import(self, context):
    self.layout.operator(ImportMHWCTC.bl_idname, text="MHW CTC (.ctc)")

def mhw_ctc_export(self, context):
    self.layout.operator(ExportMHWCTC.bl_idname, text="MHW CTC (.ctc)")

def mhw_ccl_import(self, context):
    self.layout.operator(ImportMHWCCL.bl_idname, text="MHW CCL (.ccl)")

def mhw_ccl_export(self, context):
    self.layout.operator(ExportMHWCCL.bl_idname, text="MHW CCL (.ccl)")


updatemodules = [
                 addon_updater,
                 addon_updater_ops,
]

updateclasses = [
                 addon_updater_ops.AddonUpdaterUpdateTarget,
                 addon_updater_ops.AddonUpdaterCheckNow,
                 addon_updater_ops.AddonUpdaterEndBackground,
                 addon_updater_ops.AddonUpdaterInstallManually,
                 addon_updater_ops.AddonUpdaterUpdateNow,
                 addon_updater_ops.AddonUpdaterIgnore,
                 addon_updater_ops.AddonUpdaterRestoreBackup,
                 addon_updater_ops.AddonUpdaterUpdatedSuccessful,
                 addon_updater_ops.AddonUpdaterInstallPopup,
]




def register():
    # Register classes



    global preview_collections
    auto_load.init()
    # auto_load.modules.remove(auto_load.modules[0])
    # auto_load.modules.remove(auto_load.modules[0])
    # auto_load.ordered_classes.remove(auto_load.ordered_classes[1])
    for i in range(len(updatemodules)):
        if updatemodules[i] in auto_load.modules:
            auto_load.modules.remove(updatemodules[i])
    for i in range(len(updateclasses)):
        if updateclasses[i] in auto_load.ordered_classes:
            auto_load.ordered_classes.remove(updateclasses[i])

    addon_updater_ops.register(bl_info)
    # print(auto_load.modules)
    # for i in range(len(auto_load.ordered_classes)):
    # print(auto_load.ordered_classes)
    # if updateclasses in auto_load.ordered_classes:
    #     print(666)
    # print(auto_load.frame_work_classes)
    auto_load.register()
    # CTCCCLAddonPreferences.register()
    for classEntry in panelclasses:
        bpy.utils.unregister_class(classEntry)
    for classEntry in panelclasses:
        bpy.utils.register_class(classEntry)

    icon_names = ["github", "korone", "bilibili", "qq", "caimogu"]
    pcoll = bpy.utils.previews.new()
    for icon_name in icon_names:
        pcoll.load(icon_name, os.path.join(ICONS_PATH, icon_name + ".png"), 'IMAGE')
    if preview_collections.get('icons'):
        bpy.utils.previews.remove(preview_collections['icons'])
    preview_collections['icons'] = pcoll

    add_properties(_addon_properties)

    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)

    bpy.types.TOPBAR_MT_file_import.append(mhw_ctc_import)
    bpy.types.TOPBAR_MT_file_export.append(mhw_ctc_export)
    bpy.types.TOPBAR_MT_file_import.append(mhw_ccl_import)
    bpy.types.TOPBAR_MT_file_export.append(mhw_ccl_export)

    bpy.types.Scene.ctc_toolpanel = PointerProperty(type=CTCToolPanelPG)
    bpy.types.Object.ctc_header = PointerProperty(type=CTCHeaderPG)
    bpy.types.Object.ctc_settings = PointerProperty(type=CTCSettingsPG)
    bpy.types.Object.ctc_node = PointerProperty(type=CTCNodePG)
    bpy.types.Object.ccl_collision = PointerProperty(type=CCLPG)

    bpy.types.Scene.ctc_clipboard = bpy.props.PointerProperty(type=CTCClipboardPG)
    print("{} addon is installed.".format(__addon_name__))


def unregister():
    addon_updater_ops.unregister()
    global preview_collections
    bpy.types.TOPBAR_MT_file_import.remove(mhw_ctc_import)
    bpy.types.TOPBAR_MT_file_export.remove(mhw_ctc_export)
    bpy.types.TOPBAR_MT_file_import.remove(mhw_ccl_import)
    bpy.types.TOPBAR_MT_file_export.remove(mhw_ccl_export)
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    # unRegister classes
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    auto_load.unregister()
    remove_properties(_addon_properties)
    print("{} addon is uninstalled.".format(__addon_name__))
