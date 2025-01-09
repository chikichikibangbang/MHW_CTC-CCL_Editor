import os

import bpy
from ..config import __addon_name__
from ..operators.AddonOperators import CreateCTCHeader, CreateCTCSettings
from ..operators.file_ctc import ColAttrFlag
from ....common.i18n.i18n import i18n


class CTCIOPanel(bpy.types.Panel):
    bl_label = "Import & Export"
    bl_idname = "OBJECT_PT_ctc_io_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "MHW CTC&CCL"
    # bl_context = "objectmode"

    @classmethod
    def poll(self, context: bpy.types.Context):
        mode = context.mode
        return mode == 'OBJECT' or mode == 'POSE'

    def draw(self, context: bpy.types.Context):
        #addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout
        col = layout.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.4
        row.operator("ctc.import_mhw_ctc", text= "Import CTC")
        row.operator("ctc.export_mhw_ctc", text= "Export CTC")
        col.separator()
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.4
        row.operator("ctc.import_mhw_ccl", text="Import CCL")
        row.operator("ctc.export_mhw_ccl", text="Export CCL")


class CTCToolsPanel(bpy.types.Panel):
    bl_label = "CTC & CCL Tools"
    bl_idname = "OBJECT_PT_ctc_tools_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    # name of the side panel
    bl_category = "MHW CTC&CCL"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context: bpy.types.Context):
        return context is not None

    def draw(self, context: bpy.types.Context):
        #addon_prefs = context.preferences.addons[__addon_name__].preferences

        layout = self.layout
        layout.operator(CreateCTCHeader.bl_idname)
        layout.label(text="Active CTC Collection")
        #创建一个集合索引框
        layout.prop_search(bpy.context.scene.ctc_toolpanel, "ctcCollection", bpy.data, "collections", icon="COLLECTION_COLOR_02")
        # layout.operator(CreateCTCSettings.bl_idname)

        layout.operator("ctc.align_frames")
        layout.operator("ctc.apply_angle_limit_ramp")
        layout.label(text="Create new chains in Pose Mode.")
        layout.operator("ctc.switch_to_pose")

    # @classmethod
    # def poll(cls, context: bpy.types.Context):
    #     return True

class CTCToolsPoseModePanel(bpy.types.Panel):
    bl_label = "CTC & CCL Tools"
    bl_idname = "OBJECT_PT_ctc_tools_pose_mode_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW CTC&CCL"
    bl_context = "posemode"

    @classmethod
    def poll(self,context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout
        ctc_toolpanel = bpy.context.scene.ctc_toolpanel
        # layout.label(text="Chain Tools")
        layout.label(text="Active CTC Collection")
        layout.prop_search(ctc_toolpanel, "ctcCollection",bpy.data,"collections",icon = "COLLECTION_COLOR_02")
        layout.operator("ctc.create_chain_from_bone",text=ctc_toolpanel.ChainFromBoneLabelName)
        split = layout.row(align=True)
        row = split.row(align=True)
        row.operator("ctc.rename_and_transfer_bone")
        row = split.row(align=True)
        row.alignment = 'RIGHT'
        row.operator("ctc.transfer_bone_settings", text="", icon='MODIFIER')
        # layout.label(text="Collision Tools")
        layout.operator("ctc.collision_from_bone")
        # layout.label(text="Extra Tools")
        layout.label(text="Configure chains in Object Mode.")
        layout.operator("ctc.switch_to_object")

class CTCHeaderPanel(bpy.types.Panel):
    bl_label = "CTC Header Settings"
    bl_idname = "OBJECT_PT_ctc_header_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "CTC Header Settings"
    bl_context = "object"

    #检查当前上下文是否有效、是否有一个激活的对象、该对象是否有get方法，并且该对象通过get方法获取的TYPE属性是否等于"CTC_HEADER"。只有当所有这些条件都满足时，面板才会被显示。
    @classmethod
    def poll(self, context):
        return context and context.active_object and context.active_object.get and context.active_object.get("TYPE",None) == "CTC_HEADER"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Note: The header settings here will affect all chains.", icon="ERROR")
        object = context.active_object
        ctc_header = object.ctc_header
        #创建分割布局，col1为左列，col2为右列
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        #列对齐方式
        col2.alignment = 'RIGHT'
        #属性分割显示
        col2.use_property_split = True
        #绘制CTC Header的自定义属性
        row = col2.row()
        row.prop(ctc_header, "AttributeFlags")
        row.operator("ctc.set_attr_flags", icon='DOWNARROW_HLT', text="")
        col2.prop(ctc_header, "StepTime")
        col2.label(text="")
        col2.prop(ctc_header, "GravityScaling", slider=True)
        col2.prop(ctc_header, "GlobalDamping", slider=True)
        col2.prop(ctc_header, "GlobalTransForceCoef", slider=True)
        col2.prop(ctc_header, "SpringScaling", slider=True)
        col2.label(text="")
        col = col2.column(align=True)
        col.prop(ctc_header, "WindScale")
        col.prop(ctc_header, "WindScaleMin")
        col.prop(ctc_header, "WindScaleMax")
        col = col2.column()
        col.label(text="")
        col.prop(ctc_header, "WindScaleWeight")


class CTCSettingsPanel(bpy.types.Panel):
    bl_label = "CTC Chain Settings"
    bl_idname = "OBJECT_PT_ctc_settings_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "CTC Settings"
    bl_context = "object"

    #检查当前上下文是否有效、是否有一个激活的对象、该对象是否有get方法，并且该对象通过get方法获取的TYPE属性是否等于"CTC_CHAIN"。只有当所有这些条件都满足时，面板才会被显示。
    @classmethod
    def poll(self, context):
        return context and context.object.mode == "OBJECT" and context.active_object.get("TYPE",None) == "CTC_CHAIN"

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        ctc_settings = object.ctc_settings


class CollisionAttrFlagPanel(bpy.types.Panel):
    bl_label = "Collision AttrFlag Settings"
    bl_idname = "OBJECT_PT_ctc_collision_attrflag_panel"
    bl_parent_id = "OBJECT_PT_ctc_settings_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        ctc_settings = object.ctc_settings
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment = 'RIGHT'
        col2.use_property_split = True
        col2.prop(ctc_settings, "CollisionAttrFlagValue")
        col2.prop(ctc_settings, "CollisionSelfEnable")
        col2.prop(ctc_settings, "CollisionModelEnable")
        col2.prop(ctc_settings, "CollisionVGroundEnable")

class ChainAttrFlagPanel(bpy.types.Panel):
    bl_label = "Chain AttrFlag Settings"
    bl_idname = "OBJECT_PT_ctc_chain_attrflag_panel"
    bl_parent_id = "OBJECT_PT_ctc_settings_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        ctc_settings = object.ctc_settings
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment = 'RIGHT'
        col2.use_property_split = True
        col2.prop(ctc_settings, "ChainAttrFlagValue")
        col2.prop(ctc_settings, "AngleLimitEnable")
        col2.prop(ctc_settings, "AngleLimitRestitutionEnable")
        col2.prop(ctc_settings, "EndRotConstraintEnable")
        col2.prop(ctc_settings, "TransAnimationEnable")
        col2.prop(ctc_settings, "AngleFreeEnable")
        col2.prop(ctc_settings, "StretchBothEnable")
        col2.prop(ctc_settings, "PartBlendEnable")

class OtherSettingsPanel(bpy.types.Panel):
    bl_label = "Other Chain Settings"
    bl_idname = "OBJECT_PT_ctc_other_settings_panel"
    bl_parent_id = "OBJECT_PT_ctc_settings_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'


    def draw(self, context):
        layout = self.layout
        object = context.active_object
        ctc_settings = object.ctc_settings
        # 创建分割布局，col1为左列，col2为右列
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        # 列对齐方式
        col2.alignment = 'RIGHT'
        # 属性分割显示
        col2.use_property_split = True
        col2.prop(ctc_settings, "unknAttrFlag1")
        col2.prop(ctc_settings, "unknAttrFlag2")
        col2.label(text="")
        col2.prop(ctc_settings, "ColAttribute")
        col2.prop(ctc_settings, "ColGroup")
        col2.prop(ctc_settings, "ColType")
        col2.label(text="")
        col2.prop(ctc_settings, "Gravity")
        col2.label(text="")
        col2.prop(ctc_settings, "Damping", slider=True)
        col2.prop(ctc_settings, "TransForceCoef", slider=True)
        col2.prop(ctc_settings, "SpringCoef", slider=True)
        col2.label(text="")
        col2.prop(ctc_settings, "LimitForce")
        col2.prop(ctc_settings, "FrictionCoef", slider=True)
        col2.prop(ctc_settings, "ReflectCoef", slider=True)
        col2.label(text="")
        col2.prop(ctc_settings, "WindRate", slider=True)
        col2.prop(ctc_settings, "WindLimit")


class CTCNodePanel(bpy.types.Panel):
    bl_label = "CTC Node Settings"
    bl_idname = "OBJECT_PT_ctc_node_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "CTC Node Settings"
    bl_context = "object"

    #检查当前上下文是否有效、是否有一个激活的对象、该对象是否有get方法，并且该对象通过get方法获取的TYPE属性是否等于"CTC_NODE"。只有当所有这些条件都满足时，面板才会被显示。
    @classmethod
    def poll(self, context):
        return context and context.object.mode == "OBJECT" and context.active_object.get("TYPE", None) == "CTC_NODE"

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        ctc_node = object.ctc_node
        #创建分割布局，col1为左列，col2为右列
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        #列对齐方式
        col2.alignment = 'RIGHT'
        #属性分割显示
        col2.use_property_split = True
        #绘制CTC Node的自定义属性

        col2.prop(ctc_node, "unknByte1")
        col2.prop(ctc_node, "unknByte2")
        col2.prop(ctc_node, "AngleMode")
        col2.prop(ctc_node, "CollisionShape")
        col2.prop(ctc_node, "unknownEnum")

        col2.prop(ctc_node, "boneColRadius")
        col2.prop(ctc_node, "AngleLimitRadius")
        col2.prop(ctc_node, "WidthRate", slider=True)
        col2.prop(ctc_node, "Mass")
        col2.prop(ctc_node, "ElasticCoef", slider=True)


class CCLCollisionPanel(bpy.types.Panel):
    bl_label = "CCL Collision Settings"
    bl_idname = "OBJECT_PT_ccl_collision_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "CCL Collision Settings"
    bl_context = "object"

    @classmethod
    def poll(self, context):
        return context and context.object.mode == "OBJECT" and (
                    context.active_object.get("TYPE", None) == "CCL_SPHERE" or context.active_object.get(
                "TYPE", None) == "CCL_CAPSULE")

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        ccl_collision = object.ccl_collision

        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment = 'RIGHT'
        col2.use_property_split = True

        col2.prop(ccl_collision, "ColRadius")
        col2.label(text="")
        if object.get("TYPE", None) == "CCL_SPHERE":
            col2.prop(ccl_collision, "StartColOffset", text="Collision Offset")
        elif object.get("TYPE", None) == "CCL_CAPSULE":
            col2.prop(ccl_collision, "StartColOffset")
            col2.label(text="")
            col2.prop(ccl_collision, "EndColOffset")



class CTCClipboardPanel(bpy.types.Panel):
    bl_label = "Clipboard"
    bl_idname = "OBJECT_PT_ctc_clipboard_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW CTC&CCL"
    bl_context = "objectmode"

    @classmethod
    def poll(self,context):
        return context is not None

    def draw(self, context):
        layout = self.layout
        layout.label(text="Copy CTC&CCL Object Properties")
        row = layout.row()
        row.operator("ctc.copy_ctc_properties")
        row.operator("ctc.paste_ctc_properties")
        layout.label(text="Clipboard Contents:")
        layout.label(text=str(context.scene.ctc_clipboard.ctc_type_name))


class CTCPresetPanel(bpy.types.Panel):
    bl_label = "Presets"
    bl_idname = "OBJECT_PT_ctc_presets_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW CTC&CCL"
    bl_context = "objectmode"

    @classmethod
    def poll(self,context):
        return context is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ctc_toolpanel = context.scene.ctc_toolpanel
        layout.operator("ctc.save_selected_as_preset")
        layout.operator("ctc.open_preset_folder")
        layout.label(text="CTC Chain Preset")
        layout.prop(ctc_toolpanel, "CTCChainPresets")
        layout.operator("ctc.apply_ctc_chain_preset")
        layout.label(text="CTC Node Preset")
        layout.prop(ctc_toolpanel, "CTCNodePresets")
        layout.prop(ctc_toolpanel,"applyPresetToChildNodes")
        layout.operator("ctc.apply_ctc_node_preset")

        # layout.label(text="CCL Collision Preset")
        # layout.prop(ctc_toolpanel, "CCLCollisionPresets")
        # layout.operator("ctc.create_ccl_collision_preset")


class CTCVisibilityPanel(bpy.types.Panel):
    bl_label = "Visibility"
    bl_idname = "OBJECT_PT_ctc_visibility_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW CTC&CCL"
    bl_context = "objectmode"

    @classmethod
    def poll(self,context):
        return context is not None

    def draw(self, context):
        ctc_toolpanel = context.scene.ctc_toolpanel
        layout = self.layout
        layout.operator("ctc.hide_non_nodes")
        layout.operator("ctc.hide_non_angle_limits")
        layout.operator("ccl.hide_non_collisions")
        layout.operator("ctc.unhide_all")

class CTCNodeVisPanel(bpy.types.Panel):
    bl_label = "CTC Node Settings"
    bl_idname = "OBJECT_PT_ctc_node_vis_panel"
    bl_parent_id = "OBJECT_PT_ctc_visibility_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        ctc_toolpanel = context.scene.ctc_toolpanel
        layout.prop(ctc_toolpanel, "showRelationLines")
        layout.prop(ctc_toolpanel, "showNodeNames")
        layout.prop(ctc_toolpanel, "drawNodesThroughObjects")


class CTCAngleLimitVisPanel(bpy.types.Panel):
    bl_label = "Angle Limit Settings"
    bl_idname = "OBJECT_PT_ctc_angle_limit_vis_panel"
    bl_parent_id = "OBJECT_PT_ctc_visibility_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        ctc_toolpanel = context.scene.ctc_toolpanel
        layout.prop(ctc_toolpanel, "showAngleLimitCones")
        layout.prop(ctc_toolpanel, "drawConesThroughObjects")
        layout.prop(ctc_toolpanel, "hideLastNodeAngleLimit")
        layout.prop(ctc_toolpanel, "angleLimitDisplaySize")
        layout.prop(ctc_toolpanel, "coneDisplaySize")


class CCLCollisionVisPanel(bpy.types.Panel):
    bl_label = "CCL Collision Settings"
    bl_idname = "OBJECT_PT_ccl_collision_vis_panel"
    bl_parent_id = "OBJECT_PT_ctc_visibility_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        ctc_toolpanel = context.scene.ctc_toolpanel

        layout.prop(ctc_toolpanel, "showCollisionNames")
        layout.prop(ctc_toolpanel, "drawCollisionsThroughObjects")
        # layout.prop(ctc_toolpanel, "drawCapsuleHandlesThroughObjects")


class CTCColorVisPanel(bpy.types.Panel):
    bl_label = "Color Settings"
    bl_idname = "OBJECT_PT_ctc_color_vis_panel"
    bl_parent_id = "OBJECT_PT_ctc_visibility_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        ctc_toolpanel = context.scene.ctc_toolpanel

        layout.prop(ctc_toolpanel, "collisionColor")
        layout.prop(ctc_toolpanel, "coneColor")





DIR_PATH = os.path.dirname(os.path.split(os.path.abspath(__file__))[0])
ICONS_PATH = os.path.join(DIR_PATH, "icons")
PCOLL = None
preview_collections = {}
class CTCCredits(bpy.types.Panel):
    global PCOLL
    bl_label = "Credits"
    bl_idname = "OBJECT_PT_ctcccl_credits"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MHW CTC&CCL"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}


    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=False)
        row.label(text = f"MHW CTC&CCL Editor", icon_value=preview_collections["icons"]["korone"].icon_id)
        col.separator()
        row = col.row(align=False) ; row.scale_y = 0.75
        row.label(text = "Modified by:")
        row = col.row(align=False) ; row.scale_y = 0.75
        row.label(text = "Korone")
        col.separator()
        row = col.row(align=False) ; row.scale_y = 0.75
        row.label(text = "Special thanks:")
        row = col.row(align=False) ; row.scale_y = 0.75
        row.label(text = "NSACloud, xzhuah")
        col.separator()
        row = col.row() ; row.scale_y = 1.1
        button = row.operator("ctc.github_website", icon_value=preview_collections["icons"]["github"].icon_id)
        row = col.row() ; row.scale_y = 1.1
        button = row.operator("ctc.bilibili_website", icon_value=preview_collections["icons"]["bilibili"].icon_id)
        row = col.row() ; row.scale_y = 1.1
        button = row.operator("ctc.qq_website", icon_value=preview_collections["icons"]["qq"].icon_id)
        row = col.row() ; row.scale_y = 1.1
        button = row.operator("ctc.caimogu_website", icon_value=preview_collections["icons"]["caimogu"].icon_id)
