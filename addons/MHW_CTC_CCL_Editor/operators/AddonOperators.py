import math

import bpy
import os
from math import radians

from bpy.types import Scene
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty
from mathutils import Matrix,Vector,Quaternion
import numpy as np
import copy
import re

from .ctc_function import createctcCollection, createEmpty, lockObjTransforms, findHeaderObj, getCollection, \
    checkNameUsage, orientVectorPair, createCurveEmpty, alignctcs, setctcBoneColor, createFakeEmptySphere, \
    alignCollisions
from .ctc_geometry import getConeGeoNodeTree, getCCLSphereGeoNodeTree, getCCLCapsuleGeoNodeTree
from .file_ccl import CCLCollisionData
from .file_ctc import CTCHeaderData, CTCSettingsData, CTCNodeData
from .general_function import showErrorMessageBox
from .rw_presets import saveAsPreset, readPresetJSON
from ..config import __addon_name__
from ..properties.ctc_properties import getCTCHeader, getctcSettings, getCTCNode, getCCLCollision


def tag_redraw(context, space_type="PROPERTIES", region_type="WINDOW"):
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.spaces[0].type == space_type:
                for region in area.regions:
                    if region.type == region_type:
                        region.tag_redraw()

class CreateCTCHeader(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "ctc.create_ctc_header"
    bl_label = "Create CTC Header"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Create a ctc header object.\nAll ctc objects must be parented to this.\nA new ctc collection will be created"

    #定义一个字符串属性，用于存储新创建的CTC集合名称
    collectionName: bpy.props.StringProperty(name="CTC Name",
                                             description="The name of the newly created ctc collection.\nUse the same name as the ctc file",
                                             default="newctc"
                                             )

    # @classmethod
    # def poll(cls, context: bpy.types.Context):
    #     return context.active_object is not None

    def execute(self, context: bpy.types.Context):

        #如果输入的集合名称不为空，则调用createctcCollection函数创建新的CTC集合，集合名称为输入的内容+“.ctc”
        if self.collectionName.strip() != "":
            ctcCollection = createctcCollection(self.collectionName.strip() + ".ctc")
            #调用createEmpty函数，创建一个空物体，并将其添加到刚创建的CTC集合中
            ctcHeaderObj = createEmpty(f"CTC_HEADER {self.collectionName}.ctc", [("TYPE", "CTC_HEADER")], None,
                                       ctcCollection)
            #创建一个CTCHeaderData实例，并调用getCTCHeader函数获取CTC Header的自定义属性
            ctcHeader = CTCHeaderData()
            getCTCHeader(ctcHeader, ctcHeaderObj)

            #锁定该空物体的变换
            lockObjTransforms(ctcHeaderObj)
            #将该空物体设为当前活动对象
            bpy.context.view_layer.objects.active = ctcHeaderObj
            self.report({"INFO"}, "Created new CTC collection.")
            return {'FINISHED'}
        else:
            self.report({"ERROR"}, "Invalid CTC collection name.")
            return {'CANCELLED'}

        # 弹出一个小窗口，允许用户输入新的集合名称
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class CreateCTCSettings(bpy.types.Operator):
    bl_idname = "ctc.create_ctc_settings"
    bl_label = "Create CTC Settings"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Create a CTC settings object.\nContains parameters to determine how ctc chain should behave.\nMust be parented to a ctc header"

    def execute(self, context):
        #获取当前场景中指定的CTC集合
        ctcCollection = bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection, None)
        #获取该集合中的CTC Header空物体
        headerObj = findHeaderObj()
        #若既能找到指定的CTC集合又能找到CTC Header空物体
        if ctcCollection != None and headerObj != None:
            #获取指定名称的CTC Entries集合，若没有指定集合，则新建一个新集合
            ctcEntryCollection = getCollection(f"CTC Entries - {ctcCollection.name}", ctcCollection, makeNew=False)
            #ctcEntryCollection = getCollection(f"CTC_HEADER {ctcCollection.name}", ctcCollection, makeNew=False)
            currentIndex = 0
            name = "CTC_CHAIN_" + str(currentIndex).zfill(2)
            #调用checkNameUsage函数检查名称是否已被使用，如果已被使用，则递增currentIndex并重新生成名称，直到找到一个未被使用的名称
            while (checkNameUsage(name, checkSubString=True)):
                currentIndex += 1
                name = "CTC_CHAIN_" + str(currentIndex).zfill(2)

            # currentSettingID = 0
            # while checkctcSettingsIDUsage(currentSettingID):
            #     currentSettingID += 1

            ctcSettings = CTCSettingsData()

            #调用createEmpty函数，创建一个空物体，并将其添加到刚创建的CTC Entries集合中
            ctcSettingsObj = createEmpty(name, [("TYPE", "CTC_CHAIN")], headerObj, ctcEntryCollection)
            getctcSettings(ctcSettings, ctcSettingsObj)
            #锁定该空物体的变换
            lockObjTransforms(ctcSettingsObj)
            #ctcSettingsObj.ctc_settings.id = currentSettingID
            self.report({"INFO"}, "Created CTC settings object.")
            #将该空物体设为当前活动对象
            bpy.context.view_layer.objects.active = ctcSettingsObj
        else:
            self.report({"ERROR"}, "No CTC settings object was created because the active CTC collection is not set.")
        return {'FINISHED'}

    #检查是否存在有效的CTC集合,如果不存在，则操作不可用
    @classmethod
    def poll(self,context):
        return bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection,None) is not None


class SwitchToPoseMode(bpy.types.Operator):
    bl_label = "Switch to Pose Mode"
    bl_description = "Switch to Pose Mode to add new chain bones and chain collisions"
    bl_idname = "ctc.switch_to_pose"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            armature = None
            if bpy.context.active_object != None and bpy.context.active_object.type == "ARMATURE":
                armature = bpy.context.active_object
            else:
                for obj in bpy.context.scene.objects:
                    if obj.type == "ARMATURE":
                        armature = obj
                        break
            if armature != None:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = armature

                bpy.ops.object.mode_set(mode='POSE')
        except:
            pass
        return {'FINISHED'}

class SwitchToObjectMode(bpy.types.Operator):
    bl_label = "Switch to Object Mode"
    bl_description = "Switch to Object Mode to configure chain objects"
    bl_idname = "ctc.switch_to_object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            pass
        return {'FINISHED'}

class CreateChainFromBone(bpy.types.Operator):
    bl_label = "Create Chain From Bone"
    bl_idname = "ctc.create_chain_from_bone"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Create new ctc chain objects starting from the selected bone and ending at the last child bone.\nNote that a chain cannot be branching.\nChain must be named with bonefunction_xxx"

    def execute(self, context):
        #获取当前场景中指定的CTC集合
        ctcCollection = bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection, None)
        #获取该集合中的CTC Header空物体
        headerObj = findHeaderObj()
        #若既能找到指定的CTC集合又能找到CTC Header空物体
        if ctcCollection != None and headerObj != None:
            #获取姿态模式选中的骨骼
            selected = bpy.context.selected_pose_bones
            ChainList = []

            if len(selected) == 1:
                startBone = selected[0]
                #获取头骨骼的所有子级骨骼
                ChainList = startBone.children_recursive
                #将头骨也并入链骨骼名单
                ChainList.insert(0, startBone)
                # print(ChainList)
            else:
                #必须只选中头骨以创建链，不选或选中多个骨骼无法创建链。
                showErrorMessageBox("Select only the chain start bone.")
                return {'CANCELLED'}

            #如果链骨骼名单只有一个骨骼，也就是只有头骨，那么无法创建链，一个链必须至少有2个骨骼。
            if len(ChainList) == 1:
                showErrorMessageBox("A chain must have at least 2 bones.")
                return {'CANCELLED'}

            #如果当前链中有某些骨骼不以bonefunction_xxx格式命名，则无法创建链。
            for bone in ChainList:
                match = re.match(r'^bonefunction_\d{3}$', bone.name)
                if not match:
                    showErrorMessageBox("Current chain has some bones that are not named with bonefunction_xxx. Please check the name of the bones.")
                    return {'CANCELLED'}

            valid = True
            for bone in ChainList:
                if len(bone.children) > 1:
                    valid = False
            #如果当前链中有任何一个骨骼有多个直接子级，则表示链有分叉，则无法创建链。
            if not valid:
                showErrorMessageBox("Cannot have branching bones in a chain.")
                return {'CANCELLED'}

            else:
                #获取指定名称的CTC Entries集合，若没有指定集合，则新建一个新集合
                ctcEntryCollection = getCollection(f"CTC Entries - {ctcCollection.name}", ctcCollection, makeNew=False)
                # ctcEntryCollection = getCollection(f"CTC_HEADER {ctcCollection.name}", ctcCollection, makeNew=False)
                currentIndex = 0
                name = "CTC_CHAIN_" + str(currentIndex).zfill(2)
                #调用checkNameUsage函数检查名称是否已被使用，如果已被使用，则递增currentIndex并重新生成名称，直到找到一个未被使用的名称
                while (checkNameUsage(name, checkSubString=True)):
                    currentIndex += 1
                    name = "CTC_CHAIN_" + str(currentIndex).zfill(2)

                ctcSettings = CTCSettingsData()

                #调用createEmpty函数，创建一个空物体，并将其添加到刚创建的CTC Entries集合中
                ctcSettingsObj = createEmpty(name, [("TYPE", "CTC_CHAIN")], headerObj, ctcEntryCollection)
                getctcSettings(ctcSettings, ctcSettingsObj)
                #强制刷新属性值
                ctcSettingsObj.ctc_settings.CollisionAttrFlagValue = ctcSettingsObj.ctc_settings.CollisionAttrFlagValue
                ctcSettingsObj.ctc_settings.ChainAttrFlagValue = ctcSettingsObj.ctc_settings.ChainAttrFlagValue
                #锁定该空物体的变换
                lockObjTransforms(ctcSettingsObj)
                armature = ChainList[0].id_data

                nodeParent = ctcSettingsObj
                #获取尾骨编号
                lastBoneIndex = len(ChainList) - 1


                #调用enumerate函数同时获取每个元素的索引（boneIndex）和值（bone）
                for boneIndex, bone in enumerate(ChainList):
                    #调用createEmpty函数，创建一个空物体，并将其添加到刚创建的CTC Entries集合中，并以刚创建的CTC Settings空物体为父级对象
                    nodeObj = createEmpty(bone.name, [("TYPE", "CTC_NODE")], nodeParent, ctcEntryCollection)

                    node = CTCNodeData()
                    getCTCNode(node, nodeObj)

                    #循环设为节点父级
                    nodeParent = nodeObj

                    #nodeObj.empty_display_size = 0.02
                    nodeObj.empty_display_type = "SPHERE"
                    #链节点显示设置
                    nodeObj.show_name = bpy.context.scene.ctc_toolpanel.showNodeNames
                    nodeObj.show_in_front = bpy.context.scene.ctc_toolpanel.drawNodesThroughObjects

                    #将链节点约束到对应的骨骼
                    constraint = nodeObj.constraints.new(type="COPY_LOCATION")
                    constraint.target = armature
                    constraint.subtarget = bone.name
                    constraint.name = "BoneName"


                    constraint = nodeObj.constraints.new(type="COPY_ROTATION")
                    constraint.target = armature
                    constraint.subtarget = bone.name
                    constraint.name = "BoneRotation"

                    #创建角度限制坐标轴空物体
                    frame = createEmpty(nodeObj.name + "_ANGLE_LIMIT", [("TYPE", "CTC_NODE_FRAME")], nodeObj, ctcEntryCollection)


                    frame.empty_display_type = "ARROWS"
                    #角度限制轴显示设置
                    frame.show_in_front = bpy.context.scene.ctc_toolpanel.drawNodesThroughObjects
                    frame.empty_display_size = 0.01*bpy.context.scene.ctc_toolpanel.angleLimitDisplaySize
                    # frame.empty_display_size = nodeObj.empty_display_size

                    #更新依赖图
                    bpy.context.evaluated_depsgraph_get().update()

                    #将角度限制轴约束到对应的链节点
                    constraint = frame.constraints.new(type="COPY_LOCATION")
                    constraint.target = nodeObj

                    constraint = frame.constraints.new(type="COPY_SCALE")
                    constraint.target = nodeObj

                    #若链有至少两个骨骼，且当前骨骼是链的尾骨
                    if boneIndex != 0 and boneIndex == lastBoneIndex:
                        #print(bone.name)

                        # 定义一个对齐轴，这里选择的是x轴
                        axis_align = Vector((1.0, 0.0, 0.0))

                        M = orientVectorPair(axis_align, Vector((0.0, 0.0, 0.0)))

                    #若链有至少两个骨骼，且当前骨骼不是链的尾骨
                    else:
                        if boneIndex != lastBoneIndex:
                            #print(bone.name)
                            # Point frame towards next bone head
                            targetBone = ChainList[boneIndex + 1]
                            a = armature.matrix_world @ armature.data.bones[bone.name].head_local
                            b = armature.matrix_world @ armature.data.bones[targetBone.name].head_local
                            #计算从当前骨骼头部到目标骨骼头部的方向向量，并进行归一化
                            direction = (b - a)
                            #修正向量为旋转90度后的结果
                            directioncopy = copy.deepcopy(direction)
                            direction[0] = directioncopy[0]
                            direction[1] = directioncopy[2]
                            direction[2] = -directioncopy[1]
                            #定义一个对齐轴，这里选择的是x轴
                            axis_align = Vector((1.0, 0.0, 0.0))

                            M = orientVectorPair(axis_align, direction)


                    #令框架的本地矩阵等于刚计算出的旋转矩阵
                    frame.matrix_local = M.to_4x4()

                    #设置框架旋转模式为XYZ欧拉
                    frame.rotation_mode = "XYZ"

                    #将框架的位置设为与链节点相同的位置
                    frame.location = nodeObj.location
                    #将框架的缩放设为与链节点相同的缩放
                    frame.scale = nodeObj.scale
                    #print(nodeObj.matrix_world)


                    lightObj = createCurveEmpty(nodeObj.name + "_ANGLE_LIMIT_HELPER",
                                                [("TYPE", "CTC_NODE_FRAME_HELPER")], frame, ctcEntryCollection)
                    lightObj.show_wire = True
                    lightObj.matrix_world = frame.matrix_world
                    lightObj.hide_select = True  # Disable ability to select to avoid it getting in the way

                    lightObj.show_in_front = bpy.context.scene.ctc_toolpanel.drawConesThroughObjects
                    lightObj.hide_viewport = not bpy.context.scene.ctc_toolpanel.showAngleLimitCones

                    modifier = lightObj.modifiers.new(name="CTCGeometryNodes", type='NODES')
                    nodeGroup = getConeGeoNodeTree()
                    if modifier.node_group != None and modifier.node_group.name in bpy.data.node_groups:
                        bpy.data.node_groups.remove(modifier.node_group)

                    modifier.node_group = nodeGroup

                    # Force update function to run so that the cone updates
                    nodeObj.ctc_node.AngleLimitRadius = nodeObj.ctc_node.AngleLimitRadius
                    # Determine cone scale
                    xScaleModifier = 1
                    yScaleModifier = 1
                    zScaleModifier = 1
                    if nodeObj.ctc_node.AngleMode == "2":
                        zScaleModifier = .01
                    elif nodeObj.ctc_node.AngleMode == "3":
                        zScaleModifier = nodeObj.ctc_node.WidthRate
                    lightObj.scale = (0.001*bpy.context.scene.ctc_toolpanel.coneDisplaySize * xScaleModifier,
                                      0.001*bpy.context.scene.ctc_toolpanel.coneDisplaySize * yScaleModifier,
                                      0.001*bpy.context.scene.ctc_toolpanel.coneDisplaySize * zScaleModifier)

                lightObj["isLastNode"] = 1
                #隐藏尾骨的角度限制锥体
                lightObj.hide_viewport = bpy.context.scene.ctc_toolpanel.hideLastNodeAngleLimit
                alignctcs()
                #设置姿态模式下被创建链的骨骼的骨骼组颜色
                setctcBoneColor(armature)

            self.report({"INFO"}, "Created CTC chain from bone.")
        else:
            self.report({"ERROR"}, "No CTC chain was created because the active CTC collection is not set.")
        return {'FINISHED'}

    @classmethod
    def poll(self, context):
        return bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection, None) is not None


class CTCCollisionFromBones(bpy.types.Operator):
    bl_label = "Create Collision From Bone"
    bl_idname = "ctc.collision_from_bone"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Create collision object from selected bone(s).\nSelect one bone to create a sphere or two bones to create a capsule.\nPlease select bones other than physical bones"

    def execute(self, context):
        selected = bpy.context.selected_pose_bones
        ctcCollection = bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection, None)

        headerObj = findHeaderObj(ctcCollection)
        if ctcCollection != None and (headerObj != None):
            # shape = str(bpy.context.scene.ctc_toolpanel.collisionShape)

            if len(selected) == 1:
                startBone = selected[0]
                shape = "SPHERE"
                valid = True
            elif len(selected) == 2:
                startBone = selected[0]
                endBone = selected[1]
                shape = "CAPSULE"
                valid = True
            else:
                valid = False

            if not valid:
                showErrorMessageBox("Select one bone to create a sphere or two bones to create a capsule.")
            else:
                cclname = ctcCollection.name.split(".")[0]
                collisionCollection = getCollection(f"CCL Entries - {cclname}.ccl", ctcCollection,
                                                        makeNew=False)
                currentCollisionIndex = 0
                subName = "CCL_" + str(currentCollisionIndex).zfill(2)
                while (checkNameUsage(subName, checkSubString=True)):
                    currentCollisionIndex += 1
                    subName = "CCL_" + str(currentCollisionIndex).zfill(2)

                name = subName + "_" + shape
                armature = startBone.id_data

                if shape == "SPHERE":
                    name = "CCL_" + str(currentCollisionIndex).zfill(2) + "_" + shape + " " + startBone.name
                    colSphereObj = createCurveEmpty(name, [("TYPE", "CCL_SPHERE")], headerObj,
                                                    collisionCollection)

                    cclCollision = CCLCollisionData()
                    getCCLCollision(cclCollision, colSphereObj)

                    colSphereObj.ccl_collision.StartColOffset = (
                    cclCollision.startPosX, cclCollision.startPosY, cclCollision.startPosZ)

                    constraint = colSphereObj.constraints.new(type="CHILD_OF")
                    constraint.target = armature
                    constraint.subtarget = startBone.name
                    constraint.name = "BoneName"

                    constraint.use_scale_x = False
                    constraint.use_scale_y = False
                    constraint.use_scale_z = False

                    colSphereObj.show_name = bpy.context.scene.ctc_toolpanel.showCollisionNames
                    colSphereObj.show_in_front = bpy.context.scene.ctc_toolpanel.drawCollisionsThroughObjects


                    modifier = colSphereObj.modifiers.new(name="CCLGeometryNodes", type='NODES')
                    nodeGroup = getCCLSphereGeoNodeTree()

                    if modifier.node_group != None and modifier.node_group.name in bpy.data.node_groups:
                        bpy.data.node_groups.remove(modifier.node_group)
                    modifier.node_group = nodeGroup

                elif shape == "CAPSULE":
                    name = subName + f"_{shape} - {startBone.name} > {endBone.name}"
                    colCapsuleRootObj = createCurveEmpty(name, [("TYPE", "CCL_CAPSULE")], headerObj,
                                                         collisionCollection)
                    lockObjTransforms(colCapsuleRootObj)
                    colCapsuleRootObj.show_in_front = bpy.context.scene.ctc_toolpanel.drawCollisionsThroughObjects

                    cclCollision = CCLCollisionData()
                    getCCLCollision(cclCollision, colCapsuleRootObj)

                    name = subName + f"_{shape}_HEAD" + " " + startBone.name
                    colCapsuleStartObj = createFakeEmptySphere(name, [("TYPE", "CCL_CAPSULE_START")],
                                                               colCapsuleRootObj, collisionCollection)

                    colCapsuleStartObj.ccl_collision.StartColOffset = (
                        cclCollision.startPosX, cclCollision.startPosY, cclCollision.startPosZ)

                    constraint = colCapsuleStartObj.constraints.new(type="CHILD_OF")
                    constraint.target = armature
                    constraint.subtarget = startBone.name
                    constraint.name = "BoneName"

                    constraint.use_scale_x = False
                    constraint.use_scale_y = False
                    constraint.use_scale_z = False

                    colCapsuleStartObj.show_name = bpy.context.scene.ctc_toolpanel.showCollisionNames
                    colCapsuleStartObj.show_in_front = bpy.context.scene.ctc_toolpanel.drawCapsuleHandlesThroughObjects

                    name = subName + f"_{shape}_TAIL" + " " + endBone.name
                    colCapsuleEndObj = createFakeEmptySphere(name, [("TYPE", "CCL_CAPSULE_END")],
                                                             colCapsuleRootObj, collisionCollection)
                    colCapsuleEndObj.ccl_collision.EndColOffset = (
                    cclCollision.endPosX, cclCollision.endPosY, cclCollision.endPosZ)

                    constraint = colCapsuleEndObj.constraints.new(type="CHILD_OF")
                    constraint.target = armature
                    constraint.subtarget = endBone.name
                    constraint.name = "BoneName"

                    constraint.use_scale_x = False
                    constraint.use_scale_y = False
                    constraint.use_scale_z = False

                    constraint2 = colCapsuleEndObj.constraints.new(type="COPY_SCALE")
                    constraint2.target = colCapsuleStartObj

                    colCapsuleEndObj.show_name = bpy.context.scene.ctc_toolpanel.showCollisionNames
                    colCapsuleEndObj.show_in_front = bpy.context.scene.ctc_toolpanel.drawCapsuleHandlesThroughObjects

                    colCapsuleRootObj.ccl_collision.ColRadius = colCapsuleRootObj.ccl_collision.ColRadius

                    modifier = colCapsuleRootObj.modifiers.new(name="CCLGeometryNodes", type='NODES')
                    nodeGroup = getCCLCapsuleGeoNodeTree()

                    if modifier.node_group != None and modifier.node_group.name in bpy.data.node_groups:
                        bpy.data.node_groups.remove(modifier.node_group)
                    modifier.node_group = nodeGroup

                    if bpy.app.version < (4, 0, 0):
                        modifier["Input_0"] = colCapsuleStartObj
                        modifier["Input_1"] = colCapsuleEndObj
                    else:
                        modifier["Socket_0"] = colCapsuleStartObj
                        modifier["Socket_1"] = colCapsuleEndObj

            alignCollisions()
            self.report({"INFO"}, "Created ccl collision from bone.")
        else:
            self.report({"ERROR"}, "No ccl collision was created because the active ctc collection is not set.")
        return {'FINISHED'}

    @classmethod
    def poll(self, context):
        return bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection, None) is not None



class CopyCTCProperties(bpy.types.Operator):
    bl_label = "Copy"
    bl_idname = "ctc.copy_ctc_properties"
    bl_context = "objectmode"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Copy properties from a ctc object"

    @classmethod
    def poll(cls, context):
        return bpy.context.selected_objects != []

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("TYPE", None)
        clipboard = bpy.context.scene.ctc_clipboard

        if ctcObjType == "CTC_HEADER":
            clipboard.ctc_type = ctcObjType
            clipboard.ctc_type_name = "CTC Header"
            # initialize clipboard entry
            ctcHeader = CTCHeaderData()
            getCTCHeader(ctcHeader, clipboard)
            for key, value in activeObj.ctc_header.items():
                clipboard.ctc_header[key] = value
        elif ctcObjType == "CTC_CHAIN":
            clipboard.ctc_type = ctcObjType
            clipboard.ctc_type_name = "CTC Settings"
            # initialize clipboard entry
            ctcSettings = CTCSettingsData()
            getctcSettings(ctcSettings, clipboard)
            for key, value in activeObj.ctc_settings.items():
                clipboard.ctc_settings[key] = value
        elif ctcObjType == "CTC_NODE":
            clipboard.ctc_type = ctcObjType
            clipboard.ctc_type_name = "CTC Node"
            # initialize clipboard entry
            ctcNode = CTCNodeData()
            getCTCNode(ctcNode, clipboard)
            for key, value in activeObj.ctc_node.items():
                clipboard.ctc_node[key] = value
        elif ctcObjType == "CTC_NODE_FRAME":
            clipboard.ctc_type = ctcObjType
            clipboard.ctc_type_name = "Angle Limit Orientation"
            activeObj.rotation_mode = "XYZ"
            clipboard.frameOrientation = activeObj.rotation_euler

        else:
            showErrorMessageBox("A ctc object must be selected.")
            return {'CANCELLED'}
        self.report({"INFO"}, "Copied properties of " + str(clipboard.ctc_type_name) + " object to clipboard.")
        return {'FINISHED'}


class PasteCTCProperties(bpy.types.Operator):
    bl_label = "Paste"
    bl_idname = "ctc.paste_ctc_properties"
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = "objectmode"
    bl_description = "Paste properties from a ctc object to selected objects.\nThe type of a ctc object must be the same as the object copied from"

    @classmethod
    def poll(cls, context):
        return bpy.context.selected_objects != []

    def execute(self, context):
        clipboard = bpy.context.scene.ctc_clipboard
        # activeObj = bpy.context.active_object
        for activeObj in bpy.context.selected_objects:
            ctcObjType = activeObj.get("TYPE", None)

            if clipboard.ctc_type == ctcObjType:
                if ctcObjType == "CTC_HEADER":
                    for key, value in clipboard.ctc_header.items():
                        activeObj.ctc_header[key] = value
                elif ctcObjType == "CTC_CHAIN":
                    for key, value in clipboard.ctc_settings.items():
                        activeObj.ctc_settings[key] = value
                elif ctcObjType == "CTC_NODE":
                    for key, value in clipboard.ctc_node.items():
                        activeObj.ctc_node[key] = value
                    # Force update functions to run
                    activeObj.ctc_node.AngleLimitRadius = activeObj.ctc_node.AngleLimitRadius
                    activeObj.ctc_node.AngleMode = activeObj.ctc_node.AngleMode
                    activeObj.ctc_node.boneColRadius = activeObj.ctc_node.boneColRadius
                elif ctcObjType == "CTC_NODE_FRAME":
                    activeObj.rotation_mode = "XYZ"
                    activeObj.rotation_euler = clipboard.frameOrientation

                tag_redraw(bpy.context)  # Redraw property panel
                self.report({"INFO"},
                            "Pasted properties of " + str(clipboard.ctc_type_name) + " object from clipboard.")
            else:
                showErrorMessageBox("The contents stored in the clipboard can't be applied to the selected object.")

        return {'FINISHED'}


#隐藏非CTC Nodes对象
class CTCHideNonNodes(bpy.types.Operator):
    bl_label = "Hide Non Nodes"
    bl_description = "Hide all objects that aren't ctc nodes to make selecting and configuring them easier." \
                     "\nPress the \"Unhide All\" button to unhide or check the Viewports box in the Object tab under Visibility"
    bl_idname = "ctc.hide_non_nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.get("TYPE",None) != "CTC_NODE" and obj.get("TYPE",None) != "CTC_NODE_FRAME_HELPER":
                obj.hide_viewport = True
            else:
                if not obj.get("isLastNode") and bpy.context.scene.ctc_toolpanel.hideLastNodeAngleLimit:
                    obj.hide_viewport = False
        self.report({"INFO"},"Hid all non ctc node objects.")
        return {'FINISHED'}

#隐藏非CCL Collision对象
class CCLHideNonCollisions(bpy.types.Operator):
    bl_label = "Hide Non Collisions"
    bl_description = "Hide all objects that aren't collision spheres or capsules to make selecting and configuring them easier." \
                     "\nPress the \"Unhide All\" button to unhide or check the Viewports box in the Object tab under Visibility"
    bl_idname = "ccl.hide_non_collisions"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for obj in bpy.context.scene.objects:
            objType = obj.get("TYPE", None)
            if objType == "CCL_SPHERE" or objType == "CCL_CAPSULE" or objType == "CCL_CAPSULE_START" or objType == "CCL_CAPSULE_END":
                obj.hide_viewport = False
            else:
                obj.hide_viewport = True
        self.report({"INFO"}, "Hid all non collision objects.")
        return {'FINISHED'}

#隐藏非角度限制坐标轴对象
class CTCHideNonAngleLimits(bpy.types.Operator):
    bl_label = "Hide Non Angle Limits"
    bl_description = "Hide all objects that aren't ctc node angle limits to make selecting and configuring them easier." \
                     "\nPress the \"Unhide All\" button to unhide or check the Viewports box in the Object tab under Visibility"
    bl_idname = "ctc.hide_non_angle_limits"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.get("TYPE", None) != "CTC_NODE_FRAME" and obj.get("TYPE", None) != "CTC_NODE_FRAME_HELPER":
                obj.hide_viewport = True
            else:
                if not obj.get("isLastNode") and bpy.context.scene.ctc_toolpanel.hideLastNodeAngleLimit:
                    obj.hide_viewport = False
        self.report({"INFO"}, "Hid all non ctc angle limit objects.")
        return {'FINISHED'}

#取消隐藏全部
class CTCUnhideAll(bpy.types.Operator):
    bl_label = "Unhide All"
    bl_description = "Unhide all objects hidden with \"Hide Non Nodes\" or \"Hide Non Angle Limits\""
    bl_idname = "ctc.unhide_all"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.get("TYPE",None) != "CTC_NODE_FRAME_HELPER":
                obj.hide_viewport = False
            else:
                if bpy.context.scene.ctc_toolpanel.showAngleLimitCones and not (obj.get("isLastNode") and bpy.context.scene.ctc_toolpanel.hideLastNodeAngleLimit):
                    obj.hide_viewport = False
        self.report({"INFO"},"Unhid all objects.")
        return {'FINISHED'}


class CTCAlignFrames(bpy.types.Operator):
    bl_label = "Align Angle Limit Direction"
    bl_idname = "ctc.align_frames"
    bl_description = "Aligns angle limit direction with the next node in the chain.\nNote that additional adjustments may be required for the angle limit to work properly.\nYou can select specific ctc chain objects to align"
    bl_context = "objectmode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        ctcchainList = []

        if bpy.context.selected_objects != []:
            for selectedObject in bpy.context.selected_objects:
                if selectedObject.get("TYPE", None) == "CTC_CHAIN":
                    for childObject in selectedObject.children:
                        if childObject.get("TYPE", None) == "CTC_NODE":
                            currentNode = childObject
                            currentNodeObjList = [childObject]
                            while len(currentNode.children) > 1:
                                for child in currentNode.children:
                                    if child.get("TYPE", None) == "CTC_NODE":
                                        currentNodeObjList.append(child)
                                        currentNode = child
                            ctcchainList.append(currentNodeObjList)

        if ctcchainList == []:
            CTCCollection = bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection, None)
            if CTCCollection != None:
                for selectedObject in CTCCollection.all_objects:
                    if selectedObject.get("TYPE", None) == "CTC_CHAIN":
                        for childObject in selectedObject.children:
                            if childObject.get("TYPE", None) == "CTC_NODE":
                                currentNode = childObject
                                currentNodeObjList = [childObject]
                                while len(currentNode.children) > 1:
                                    for child in currentNode.children:
                                        if child.get("TYPE", None) == "CTC_NODE":
                                            currentNodeObjList.append(child)
                                            currentNode = child
                                ctcchainList.append(currentNodeObjList)


        if ctcchainList != []:
            for ctcchain in ctcchainList:
                lastNodeIndex = len(ctcchain) - 1
                for nodeIndex, ctcNode in enumerate(ctcchain):
                    frame = None
                    for child in ctcNode.children:
                        if child.get("TYPE", None) == "CTC_NODE_FRAME":
                            frame = child

                    armature = ctcNode.constraints["BoneName"].target
                    boneName = str(ctcNode.constraints["BoneName"].subtarget)

                    #若链有至少两个骨骼，且当前骨骼是链的尾骨
                    if nodeIndex != 0 and nodeIndex == lastNodeIndex:
                        # 定义一个对齐轴，这里选择的是x轴
                        axis_align = Vector((1.0, 0.0, 0.0))
                        M = orientVectorPair(axis_align, Vector((0.0, 0.0, 0.0)))
                    #若链有至少两个骨骼，且当前骨骼不是链的尾骨
                    else:
                        if nodeIndex != lastNodeIndex:
                            #targetBone = ChainList[nodeIndex + 1]
                            targetBoneName = ctcchain[nodeIndex + 1].constraints["BoneName"].subtarget
                            a = armature.matrix_world @ armature.data.bones[boneName].head_local
                            b = armature.matrix_world @ armature.data.bones[targetBoneName].head_local
                            #计算从当前骨骼头部到目标骨骼头部的方向向量，并进行归一化
                            direction = (b - a)
                            #修正向量为旋转90度后的结果
                            directioncopy = copy.deepcopy(direction)
                            direction[0] = directioncopy[0]
                            direction[1] = directioncopy[2]
                            direction[2] = -directioncopy[1]
                            #定义一个对齐轴，这里选择的是x轴
                            axis_align = Vector((1.0, 0.0, 0.0))
                            M = orientVectorPair(axis_align, direction)

                    if frame != None:
                        frame.matrix_local = M.to_4x4()
                        # 设置框架旋转模式为XYZ欧拉
                        frame.rotation_mode = "XYZ"
                        # 将框架的位置设为与链节点相同的位置
                        frame.location = ctcNode.location
                        # 将框架的缩放设为与链节点相同的缩放
                        frame.scale = ctcNode.scale
            self.report({"INFO"}, "Aligned angle limit directions.")
            return {'FINISHED'}
        else:
            showErrorMessageBox("No chains found in selection or collection.")
            return {'CANCELLED'}

    @classmethod
    def poll(self, context):
        return bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection, None) is not None


class CTCApplyAngleLimitRamp(bpy.types.Operator):
    bl_label = "Apply Angle Limit Ramp"
    bl_description = "Apply an increasing angle limit on each ctc node as it gets further away.\nA ctc chain must be selected. If multiple ctc chains are selected, the angle limits will be applied to all of them"
    bl_idname = "ctc.apply_angle_limit_ramp"
    bl_context = "objectmode"
    bl_options = {'REGISTER', 'UNDO'}
    maxAngleLimit : bpy.props.FloatProperty(name = "Max Angle Limit",
                                         description = "The maximum angle limit radius after the max iteration number is reached."
                                                       "\nFor example, if the max angle limit is 60 and the max iteration is 4, the first node angle limit will be 15, the second will be 30 and so on."
                                                       "\nOnce the max iteration is reached, all nodes after that will be the max angle limit value",
                                         default = math.pi/3,
                                         step=100,
                                         soft_min=0.0,
                                         soft_max=180.0,
                                         subtype = "ANGLE",)
    maxIteration : bpy.props.IntProperty(name = "Max Iteration",
                                      description = "The amount of ctc nodes until the angle limit radius is at it's maximum value",
                                      default = 4,
                                      min = 1)

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.get("TYPE") == "CTC_CHAIN"

    def execute(self, context):
        ctcchainList = []  # List of lists of nodes
        for selectedObject in bpy.context.selected_objects:
            if selectedObject.get("TYPE", None) == "CTC_CHAIN":
                for childObject in selectedObject.children:
                    if childObject.get("TYPE", None) == "CTC_NODE":
                        currentNode = childObject
                        currentNodeObjList = [childObject]
                        while len(currentNode.children) > 1:
                            for child in currentNode.children:
                                if child.get("TYPE", None) == "CTC_NODE":
                                    currentNodeObjList.append(child)
                                    currentNode = child
                        ctcchainList.append(currentNodeObjList)

        if ctcchainList != []:
            angleLimitStep = self.maxAngleLimit / self.maxIteration
            for ctcGroup in ctcchainList:
                for nodeIndex, ctcNode in enumerate(ctcGroup):
                    if nodeIndex + 1 < self.maxIteration:
                        ctcNode.ctc_node.AngleLimitRadius = angleLimitStep * (nodeIndex + 1)
                    else:
                        ctcNode.ctc_node.AngleLimitRadius = self.maxAngleLimit
            self.report({"INFO"}, "Applied angle limit ramp to selected ctc chains.")
            return {'FINISHED'}
        else:
            showErrorMessageBox("ctc chains must be selected to apply an angle limit ramp.")
            return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class CTCRenameAndTransferBone(bpy.types.Operator):
    bl_label = "Rename&Transfer Bones"
    bl_description = "Rename and transfer all bones that are a child of the selected bone.\nThe bones cannot be branching.\nSee settings on the right for detailed operation items"
    bl_idname = "ctc.rename_and_transfer_bone"
    bl_context = "posemode"
    bl_options = {'REGISTER', 'UNDO'}

    newStartBoneID: bpy.props.IntProperty(
        name="Start Bone ID",
        description="Current chain will be sorted backwards and renamed with the ID entered",
        default=150,
        min=0,
        max=999,
    )

    @classmethod
    def poll(self, context):
        return context.active_object is not None

    def execute(self, context):
        #获取姿态模式选中的骨骼
        selected = bpy.context.selected_pose_bones
        ChainList = []

        if len(selected) == 1:
            startBone = selected[0]
            #获取头骨骼的所有子级骨骼
            ChainList = startBone.children_recursive
            #将头骨也并入链骨骼名单
            ChainList.insert(0, startBone)
            #print(ChainList)
        else:
            #必须只选中头骨以重命名整条链。
            showErrorMessageBox("Select only the chain start bone.")
            return {'CANCELLED'}

        #如果链骨骼名单只有一个骨骼，也就是只有头骨，那么无法重命名整条链，一个链必须至少有2个骨骼。
        if len(ChainList) == 1:
            showErrorMessageBox("A chain must have at least 2 bones.")
            return {'CANCELLED'}

        valid = True
        for bone in ChainList:
            if len(bone.children) > 1:
                valid = False
        #如果当前链中有任何一个骨骼有多个直接子级，则表示链有分叉，则无法重命名整条链。
        if not valid:
            showErrorMessageBox("Cannot have branching bones in a chain.")
            return {'CANCELLED'}

        else:
            # 如果当前输入的ID值会导致出现重复的骨骼名，则报错
            # valid = True
            # for index, bone in enumerate(ChainList):
            #     newBoneName = "bonefunction_" + str(self.newStartBoneID + index).zfill(3)
            #     for b in bpy.context.active_object.data.bones:
            #         if b.name == newBoneName:
            #             valid = False
            # if not valid:
            #     showErrorMessageBox("Current chain will result in duplicate IDs. Please select another ID.")
            #     return {'CANCELLED'}

            for index, bone in enumerate(ChainList):
                newBoneName = "bonefunction_" + str(self.newStartBoneID + index).zfill(3)

                nodeObj = bpy.data.objects.get(bone.name, None)
                if nodeObj != None and nodeObj.get("TYPE", None) == "CTC_NODE":
                    nodeObj.name = newBoneName

                nodeAngleLimitObj = bpy.data.objects.get(bone.name + "_ANGLE_LIMIT", None)
                if nodeAngleLimitObj != None and nodeAngleLimitObj.get("TYPE", None) == "CTC_NODE_FRAME":
                    nodeAngleLimitObj.name = newBoneName + "_ANGLE_LIMIT"
                elif nodeObj != None:
                    for child in nodeObj.children:
                        if child.get("TYPE", None) == "CTC_NODE_FRAME":
                            child.name = newBoneName + "_ANGLE_LIMIT"

                nodeAngleLimitConeObj = bpy.data.objects.get(bone.name + "_ANGLE_LIMIT_HELPER", None)
                if nodeAngleLimitConeObj != None and nodeAngleLimitConeObj.get("TYPE", None) == "CTC_NODE_FRAME_HELPER":
                    nodeAngleLimitConeObj.name = newBoneName + "_ANGLE_LIMIT_HELPER"
                elif nodeObj != None and nodeAngleLimitObj != None:
                    for child in nodeAngleLimitObj.children:
                        if child.get("TYPE", None) == "CTC_NODE_FRAME_HELPER":
                            child.name = newBoneName + "_ANGLE_LIMIT_HELPER"
                bone.name = newBoneName
            #累加计算下一次重命名应该使用的头骨ID
            self.newStartBoneID = self.newStartBoneID + len(ChainList)

        if context.scene.use_addboneprop:
            bpy.ops.ctc.add_mod3_bone_prop()
        if context.scene.use_bonealign:
            bpy.ops.ctc.bone_vertical_alignment()

        self.report({"INFO"}, "Renamed&Transfered chain bones.")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        boneIDnum = 50
        boneIDlist = list(range(150, 200))
        valid2 = True
        for bone in bpy.context.active_object.data.bones:
            if "bonefunction_" in bone.name:
                try:
                    ID = int(bone.name.split("_")[-1])
                    if 150 <= ID < 200:
                        boneIDnum -= 1
                        boneIDlist.remove(ID)
                    else:
                        valid2 = False
                except ValueError:
                    pass

        layout = self.layout
        col = layout.column(align=True)
        if not valid2:
            row = col.row(align=True)
            row.label(text="Note: There are some IDs outside 150~200!")
        layout.prop(self, "newStartBoneID")
        col = layout.column(align=True)
        row = col.row(align=True)
        row.label(text="number of unused ID (150~200): " + str(boneIDnum))
        row = col.row(align=True)
        row.label(text="unused ID (150~200): ")
        row = col.row(align=True)
        for i in range(len(boneIDlist)):
            # row = col.row(align=True)
            row.label(text=str(boneIDlist[i]))
            if (i+1) % 10 == 0:
                row = col.row(align=True)
        for i in range(10-len(boneIDlist)%10):
            row.label(text="   ")



class CTCAddMod3BoneProp(bpy.types.Operator):
    bl_label = "Add Mod3 Bone Properties"
    bl_description = "Add mod3 bone properties to normal bones"
    bl_idname = "ctc.add_mod3_bone_prop"
    bl_context = "posemode"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return context.active_object is not None

    def execute(self, context):
        ArmatureName = bpy.context.active_object.data.name
        #获取姿态模式选中的骨骼
        selected = bpy.context.selected_pose_bones
        ChainList = []

        startBone = selected[0]
        #获取头骨骼的所有子级骨骼
        ChainList = startBone.children_recursive
        #将头骨也并入链骨骼名单
        ChainList.insert(0, startBone)

        bpy.ops.object.mode_set(mode='EDIT')
        for index, bone in enumerate(ChainList):
            editbone = bpy.data.armatures[ArmatureName].edit_bones[bone.name]
            editbone["child"] = 255
            editbone["unkn2"] = 0.000
        bpy.ops.object.mode_set(mode='POSE')

        #self.report({"INFO"}, "Renamed chain bones.")
        return {'FINISHED'}


class CTCBoneVerticalAlignment(bpy.types.Operator):
    bl_label = "Bone Vertical Alignment"
    bl_description = "Align bones in a vertical and upward direction"
    bl_idname = "ctc.bone_vertical_alignment"
    bl_context = "posemode"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return context.active_object is not None

    def execute(self, context):
        ArmatureName = bpy.context.active_object.data.name
        #获取姿态模式选中的骨骼
        selected = bpy.context.selected_pose_bones
        ChainList = []

        startBone = selected[0]
        #获取头骨骼的所有子级骨骼
        ChainList = startBone.children_recursive
        #将头骨也并入链骨骼名单
        ChainList.insert(0, startBone)

        bpy.ops.object.mode_set(mode='EDIT')
        for index, bone in enumerate(ChainList):
            editbone = bpy.data.armatures[ArmatureName].edit_bones[bone.name]
            editbone.use_connect = False
        for index, bone in enumerate(ChainList):
            editbone = bpy.data.armatures[ArmatureName].edit_bones[bone.name]
            bpy.context.object.data.use_mirror_x = False
            editbone.tail[0] = editbone.head[0]
            editbone.tail[1] = editbone.head[1]
            editbone.tail[2] = editbone.head[2] + 0.03
            editbone.roll = 0.0
        bpy.ops.object.mode_set(mode='POSE')

        #self.report({"INFO"}, "Renamed chain bones.")
        return {'FINISHED'}


class CTCTransferBoneSettings(bpy.types.Operator):
    bl_label = "Transfer Bone Settings"
    bl_description = ""
    bl_idname = "ctc.transfer_bone_settings"
    bl_context = "posemode"
    bl_options = {'REGISTER', 'UNDO'}

    Scene.use_addboneprop = BoolProperty(
        name="Add Mod3 Bone Properties",
        description="Add mod3 bone properties to normal bones",
        default=True
    )
    Scene.use_bonealign = BoolProperty(
        name="Bone Vertical Alignment",
        description="Align bones in a vertical and upward direction",
        default=True
    )


    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def check(self, context):
        # Important for changing options
        return True

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        row = col.row(align=True)
        row.prop(context.scene, "use_addboneprop")
        row = col.row(align=True)
        row.prop(context.scene, "use_bonealign")


#已知的常见Header AttributeFlags数值
AttrFlagsItems = [
    ("0", "AttrFlags_0", ""),
    ("16", "AttrFlags_16", ""),
    ("64", "AttrFlags_64", ""),
    ("80", "AttrFlags_80", ""),
]

class CTCSetAttrFlags(bpy.types.Operator):
    bl_label = "Set Attribute Flag"
    bl_description = "Set header attribute flag value from a list of known values"
    bl_idname = "ctc.set_attr_flags"
    bl_context = "objectmode"
    bl_options = {'UNDO', 'INTERNAL'}
    AttrFlagsEnum: bpy.props.EnumProperty(
        name="Attribute Flags",
        description="Set Attribute Flags value",
        items=AttrFlagsItems,
        default="64",
    )

    @classmethod
    def poll(self, context):
        return context.active_object is not None

    def execute(self, context):
        activeObject = bpy.context.active_object
        if activeObject != None:
            activeObjectType = activeObject.get("TYPE", None)
            if activeObjectType == "CTC_HEADER":
                activeObject.ctc_header.AttributeFlags = int(self.AttrFlagsEnum)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class CTCSavePreset(bpy.types.Operator):
    bl_label = "Save Selected As Preset"
    bl_idname = "ctc.save_selected_as_preset"
    bl_context = "objectmode"
    bl_description = "Save selected ctc&ccl object as a preset for easy reuse and sharing.\nPresets can be accessed using the Open Preset Folder button"
    presetName: bpy.props.StringProperty(name="Preset Name", default="newPreset")

    @classmethod
    def poll(self, context):
        return context.active_object is not None

    def execute(self, context):
        finished = saveAsPreset(context.selected_objects, self.presetName)
        if finished:
            self.report({"INFO"}, "Saved preset.")
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

        return {'FINISHED'}


class CTCOpenPresetFolder(bpy.types.Operator):
    bl_label = "Open Preset Folder"
    bl_description = "Opens the preset folder in File Explorer"
    bl_idname = "ctc.open_preset_folder"

    def execute(self, context):
        presetsPath = os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]),"presets")
        os.startfile(presetsPath)
        return {'FINISHED'}

class CTCApplyCTCChainPreset(bpy.types.Operator):
    bl_label = "Apply CTC Chain Preset"
    bl_idname = "ctc.apply_ctc_chain_preset"
    bl_description = "Apply preset to selected ctc chain objects"
    bl_options = {'UNDO', 'INTERNAL'}

    def execute(self, context):
        enumValue = bpy.context.scene.ctc_toolpanel.CTCChainPresets
        finished = False
        presetsPath = os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]),"presets")
        #activeObj = bpy.context.active_object
        print("Reading Preset: " + enumValue)
        for activeObj in bpy.context.selected_objects:
            finished = readPresetJSON(os.path.join(presetsPath,enumValue),activeObj)
        tag_redraw(bpy.context)
        if finished:
            self.report({"INFO"},"Applied ctc chain preset.")
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class CTCApplyCTCNodePreset(bpy.types.Operator):
    bl_label = "Apply CTC Node Preset"
    bl_idname = "ctc.apply_ctc_node_preset"
    bl_description = "Apply preset to selected ctc node objects.\nNote that frame orientations are not changed by presets"
    bl_options = {'UNDO', 'INTERNAL'}

    def execute(self, context):
        enumValue = bpy.context.scene.ctc_toolpanel.CTCNodePresets
        finished = False
        presetsPath = os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]), "presets")
        # activeObj = bpy.context.active_object
        print("Reading Preset: " + enumValue)
        for activeObj in bpy.context.selected_objects:
            if activeObj.get("TYPE", None) == "CTC_NODE":
                currentNode = activeObj
                nodeObjList = [currentNode]
                if bpy.context.scene.ctc_toolpanel.applyPresetToChildNodes:
                    while len(currentNode.children) > 1:
                        for child in currentNode.children:
                            if child.get("TYPE", None) == "CTC_NODE":
                                nodeObjList.append(child)
                                currentNode = child
                # print(nodeObjList)
                for nodeObj in nodeObjList:
                    finished = readPresetJSON(os.path.join(presetsPath, enumValue), nodeObj)
                tag_redraw(bpy.context)
        if finished:
            self.report({"INFO"}, "Applied ctc node preset.")
            return {'FINISHED'}
        else:
            showErrorMessageBox("Must select a ctc node in order to apply the preset to it.")
            return {'CANCELLED'}


# class CreateCCLCollisionPreset(bpy.types.Operator):
#     bl_label = "Create Preset CCL Collision"
#     bl_idname = "ctc.create_ccl_collision_preset"
#     bl_description = "Create objects from preset ccl collision"
#     bl_options = {'UNDO', 'INTERNAL'}
#
#     def execute(self, context):
#         enumValue = bpy.context.scene.ctc_toolpanel.CCLCollisionPresets
#         finished = False
#         presetsPath = os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]),"presets")
#         #activeObj = bpy.context.active_object
#         print("Reading Preset: " + enumValue)
#         for activeObj in bpy.context.selected_objects:
#             finished = readPresetJSON(os.path.join(presetsPath,enumValue),activeObj)
#         tag_redraw(bpy.context)
#         if finished:
#             self.report({"INFO"},"Created preset ccl collision.")
#             return {'FINISHED'}
#         else:
#             return {'CANCELLED'}