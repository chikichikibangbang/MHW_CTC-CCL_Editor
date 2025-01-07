import bpy
import os
from mathutils import Matrix,Vector,Quaternion
from math import radians

from .ctc_geometry import getConeGeoNodeTree, getCCLSphereGeoNodeTree, getCCLCapsuleGeoNodeTree
from .file_ccl import readCCL, CCLFile, writeCCL, CCLCollisionData
from .file_ctc import readCTC, CTCFile, CTCSettingsData, CTCNodeData, writeCTC
from .general_function import textColors, raiseWarning, raiseError, showMessageBox, showErrorMessageBox
from ..properties.ctc_properties import getCTCHeader, getctcSettings, getCTCNode, setCTCHeaderData, setctcSettingsData, \
    setCTCNodeData, getCCLCollision, setCCLCollisionData


def orientVectorPair(v0,v1):
    v0 = v0.normalized()
    v1 = v1.normalized()
    if v0 == v1:
        return Matrix.Identity(3)
    v = v0.cross(v1)
    #s = v.length
    c = v0.dot(v1)
    if c == -1: return Matrix([[-1,0,0],[0,-1,0],[0,0,1]])
    vx = Matrix([[0,-v[2], v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]])
    return Matrix.Identity(3)+vx+(1/(1+c))*vx@vx

# def orientVectorSystem(obj, target, axis, origin=None):
#     star = obj if checkIsStarFrame(obj) else getStarFrame(obj)
#     if origin is None:
#         origin = star
#     # sscale = star.empty_draw_size * accessScale(star.matrix_world.to_scale())
#     # star.empty_draw_size = sscale
#     loc = star.location
#     targetVector = armature.matrix_world @ target.head_local.translation - origin.matrix_world.translation
#     M = orientVectorPair(axis, targetVector)
#     star.matrix_local = M.to_4x4()
#     star.location = loc

#从Blender数据中获取指定的骨架对象
def findArmatureObjFromData(armatureData):
    armatureObj = None
    for obj in bpy.context.scene.objects:
        if obj.type == "ARMATURE" and obj.data == armatureData:
            armatureObj = obj
            break
    return armatureObj


def findBone(boneName, armature=None):
    if armature == None:  # Find an armature if one is not specified
        if bpy.context.active_object != None and bpy.context.active_object.type == "ARMATURE":
            armature = bpy.context.active_object
        else:
            for obj in bpy.context.scene.objects:
                if armature != None:
                    raiseError(
                        "More than one armature was found in the scene. Select an armature before importing the chain.")
                if obj.type == "ARMATURE":
                    armature = obj
    if armature != None:
        bones = armature.data.bones
        searchBone = bones.get(boneName, None)
        if searchBone == None:

            for bone in armature.data.bones:  # If the armature has bone numbers, loop through every bone with bone numbers removed
                if bone.name.startswith("a") and ":" in bone.name and bone.name.split(":")[1] == boneName:
                    searchBone = bone
            if searchBone == None:
                raiseWarning(str(boneName) + " is not a part of armature: " + armature.name)
        return searchBone
    else:  # No armature in scene
        return None


def findCCLPathFromCTCPath(filepath):
    split = filepath.split(".ctc")
    fileRoot = split[0]

    CCLPath = f"{fileRoot}.ccl"
    # if not os.path.isfile(CCLPath):
    #     print(f"Could not find {CCLPath}.")

    if CCLPath == None or not os.path.isfile(CCLPath):
        print(f"Could not find {CCLPath}.")
        CCLPath = None

    return CCLPath


#导入ctc文件
#参数：filepath（要导入的ctc文件路径），options（导入选项，包含目标骨架的名称）
def importCTCFile(filepath, options):
    #初始化变量armature，用于存储找到的骨架对象
    armature = None
    #检查在Blender数据中是否存在指定名称的骨架，如果存在，则调用findArmatureObjFromData函数获取该骨架对象，并将其赋值给armature
    if bpy.data.armatures.get(options["targetArmature"]) != None:
        armature = findArmatureObjFromData(bpy.data.armatures[options["targetArmature"]])
    try:
        #如果之前没有找到骨架，并且当前活动对象存在且为骨架类型，则将当前活动对象赋值给armature
        if armature == None and bpy.context.active_object != None and bpy.context.active_object.type == "ARMATURE":
            armature = bpy.context.active_object
    except:
        pass
    #如果仍然未找到骨架，则遍历当前场景中所有的对象
    if armature == None:
        for obj in bpy.context.scene.objects:
            #如果找到多个骨架，则报错提示
            if obj.type == "ARMATURE" and armature != None:
                showErrorMessageBox(
                    "More than one armature was found in the scene. Select an armature before importing the ctc file.")
                return False
            if obj.type == "ARMATURE":
                armature = obj
    #如果到最后都没有找到骨架，则报错提示
    if armature == None:
        showErrorMessageBox(
            "No armature in scene. The armature from the mod3 file must be present in order to import the ctc file.")
        return False

    fileName = os.path.split(filepath)[1].split(".mesh")[0]

    #将ctc文件的Header部分转换为CTC_Header空物体
    CTCFile = readCTC(filepath)

    removedItems = []
    NodeNumList = []
    k = 0

    for groupIndex, chainGroup in enumerate(CTCFile.CTCSettingsList):
        NodeNumList.append(chainGroup.NodeNum)
    # 检查ctc文件中的boneFunctionID是否存在对应的骨骼
    for groupIndex, chainGroup in enumerate(CTCFile.CTCSettingsList):
        if chainGroup.NodeNum > 0:
            #索引每节CTCChain包含的CTCNode ID
            for i in range(k, k + chainGroup.NodeNum):

                boneIDname = "bonefunction_" + str(CTCFile.CTCNodesList[i].boneFunctionID).zfill(3)
                BoneID = findBone(boneIDname, armature)
                #若找不到对应的骨骼，则移除当前CTC Node节
                if BoneID == None:
                    removedItems.append(CTCFile.CTCNodesList[i])
                    #链长度减1
                    NodeNumList[groupIndex] -= 1
        #累加序列号
        k += chainGroup.NodeNum

    for i in range(len(NodeNumList)):
        CTCFile.CTCSettingsList[i].NodeNum = NodeNumList[i]
    for item in removedItems:
        CTCFile.CTCNodesList.remove(item)

    removedItems = []
    # CTCFile.Header.ChainGroupCount = len(CTCFile.CTCSettingsList)
    # CTCFile.Header.ChainNodeTotalCount = len(CTCFile.CTCNodesList)

    #导入CTC Header
    headerObj = None
    if bpy.data.collections.get(options["mergeChain"]):  # Merge with existing ctc header if this is set
        headerObj = findHeaderObj(bpy.data.collections[options["mergeChain"]])
        CTCCollection = bpy.data.collections[options["mergeChain"]]
        mergedChain = True

    if headerObj == None:
        mergedChain = False
        # CTCFileName = os.path.splitext(os.path.split(filepath)[1])[0]
        CTCFileName = os.path.split(filepath)[1]
        CTCCollection = createctcCollection(CTCFileName)
        headerPropertyList = [("TYPE", "CTC_HEADER")]
        headerObj = createEmpty(f"CTC_HEADER {CTCFileName}", headerPropertyList, None, CTCCollection)

        getCTCHeader(CTCFile.Header, headerObj)
        lockObjTransforms(headerObj)

    j = 0
    if len(CTCFile.CTCSettingsList) > 0:
        ctcEntryCollection = getCollection(f"CTC Entries - {CTCCollection.name}", CTCCollection,
                                             makeNew=not mergedChain)
        ctcEntryCollection["TYPE"] = "CTC_ENTRY_COLLECTION"
    else:
        ctcEntryCollection = CTCCollection
    for i in range(len(CTCFile.CTCSettingsList)):
        if CTCFile.CTCSettingsList[i].NodeNum > 1:
            j += 1
    print(f"CTC Chain Count: {len(CTCFile.CTCSettingsList)}", f"Imported Count: {j}" )
    #
    unusedSettings = set(range(0, len(CTCFile.CTCSettingsList)))

    #导入CTC Settings
    CTCSettingsObjList = []
    currentCTCSettingsNameIndex = 0
    startctcnodeindex = 0
    for settingsIndex, chainSettings in enumerate(CTCFile.CTCSettingsList):
        #如果CTC Settings组的链长度值不为0（至少为2）
        if chainSettings.NodeNum > 1:
            #移除链长度值为0的CTC Settings索引序号
            unusedSettings.remove(settingsIndex)
            name = "CTC_CHAIN_" + str(currentCTCSettingsNameIndex).zfill(2)
            if mergedChain:
                while checkNameUsage(name, checkSubString=True):
                    currentCTCSettingsNameIndex += 1
                    name = "CTC_CHAIN_" + str(currentCTCSettingsNameIndex).zfill(2)
            else:
                currentCTCSettingsNameIndex += 1
            chainSettingsObj = createEmpty(name, [("TYPE", "CTC_CHAIN")], headerObj,
                                           ctcEntryCollection)
            getctcSettings(chainSettings, chainSettingsObj)
            #强制刷新数值
            chainSettingsObj.ctc_settings.CollisionAttrFlagValue = chainSettingsObj.ctc_settings.CollisionAttrFlagValue
            chainSettingsObj.ctc_settings.ChainAttrFlagValue = chainSettingsObj.ctc_settings.ChainAttrFlagValue
            lockObjTransforms(chainSettingsObj)
            CTCSettingsObjList.append(chainSettings)
            nodeParent = chainSettingsObj
            #startBone = findBone(chainSettings.terminateNodeName, armature)

            #name = str(chainSettings.NodeNum.rsplit("_", 1)[0])

            childchainList = []
            for i in range(chainSettings.NodeNum):
                childchainList.append(CTCFile.CTCNodesList[i+startctcnodeindex])
            startctcnodeindex += chainSettings.NodeNum

            #导入CTC Nodes
            for nodeIndex,node in enumerate(childchainList):
                # if boneList != [None]:
                #     name = boneList[nodeIndex].name
                #     currentBone = boneList[nodeIndex]
                # else:
                #     raiseWarning("Could not find chain bones in armature, guessing node names.")
                #     if nodeIndex == len(chainGroup.nodeList) - 1:
                #         name = baseNodeName + "_end"
                #     else:
                #         name = baseNodeName + "_" + str(nodeIndex).zfill(2)
                name = "bonefunction_" + str(node.boneFunctionID).zfill(3)
                nodeObj = createEmpty(name, [("TYPE", "CTC_NODE")], nodeParent, ctcEntryCollection)
                getCTCNode(node, nodeObj)
                nodeParent = nodeObj
                #nodeObj.empty_display_size = 2
                nodeObj.empty_display_type = "SPHERE"
                nodeObj.show_name = bpy.context.scene.ctc_toolpanel.showNodeNames
                nodeObj.show_in_front = bpy.context.scene.ctc_toolpanel.drawNodesThroughObjects

                # 将链节点约束到对应的骨骼
                constraint = nodeObj.constraints.new(type="COPY_LOCATION")
                constraint.target = armature
                constraint.subtarget = name
                constraint.name = "BoneName"

                constraint = nodeObj.constraints.new(type="COPY_ROTATION")
                constraint.target = armature
                constraint.subtarget = name
                constraint.name = "BoneRotation"

                #创建角度限制空物体
                frame = createEmpty(nodeObj.name + "_ANGLE_LIMIT", [("TYPE", "CTC_NODE_FRAME")], nodeObj,
                                    ctcEntryCollection)
                frame.empty_display_type = "ARROWS"
                frame.empty_display_size = 0.01*bpy.context.scene.ctc_toolpanel.angleLimitDisplaySize
                frame.show_in_front = bpy.context.scene.ctc_toolpanel.drawNodesThroughObjects

                constraint = frame.constraints.new(type="COPY_LOCATION")
                constraint.target = nodeObj

                constraint = frame.constraints.new(type="COPY_SCALE")
                constraint.target = nodeObj

                frame.matrix_local = Matrix([[node.row1_0, node.row1_1,node.row1_2,node.row1_3],
                                             [node.row2_0, node.row2_1,node.row2_2,node.row2_3],
                                             [node.row3_0, node.row3_1,node.row3_2,node.row3_3],
                                             [node.row4_0, node.row4_1,node.row4_2,node.row4_3]])

                frame.rotation_mode = "XYZ"
                frame.location = nodeObj.location
                frame.scale = nodeObj.scale

                #创建角度限制锥体
                lightObj = createCurveEmpty(nodeObj.name + "_ANGLE_LIMIT_HELPER",
                                            [("TYPE", "CTC_NODE_FRAME_HELPER")], frame, ctcEntryCollection)
                lightObj.matrix_world = frame.matrix_world
                lightObj.show_wire = True
                lightObj.hide_select = True

                lightObj.show_in_front = bpy.context.scene.ctc_toolpanel.drawConesThroughObjects
                lightObj.hide_viewport = not bpy.context.scene.ctc_toolpanel.showAngleLimitCones

                modifier = lightObj.modifiers.new(name="CTCGeometryNodes", type='NODES')
                nodeGroup = getConeGeoNodeTree()

                if modifier.node_group != None and modifier.node_group.name in bpy.data.node_groups:
                    bpy.data.node_groups.remove(modifier.node_group)

                modifier.node_group = nodeGroup

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
            # 隐藏尾骨的角度限制锥体
            lightObj.hide_viewport = bpy.context.scene.ctc_toolpanel.hideLastNodeAngleLimit
        elif chainSettings.NodeNum == 1:
            startctcnodeindex += 1
        alignctcs()
        # 设置姿态模式下被创建链的骨骼的骨骼组颜色
    setctcBoneColor(armature)

    CTCSettingsObjList.clear()

    if options["loadccl"]:
        CCLPath = findCCLPathFromCTCPath(filepath)
    try:
        if CCLPath != None:
            print("Loading CCL File...")
            try:
                importCCLFile(CCLPath, options)
            except Exception as err:
                raiseWarning("Could not import CCL File from " + CCLPath + ":" + str(err))
                # warningList.append("Could not import CCL File from " + CCLPath + ":" + str(err))
        else:
            k = 0
            # warningList.append("CCL file not found.")
    except Exception as err:
        k = 0
        # print(str(err))
        # warningList.append("Could not import ccl file from " + CCLPath + ":" + str(err))

    return True


def ctcErrorCheck(ctcCollectionName):
    print("\nChecking for problems with ctc structure...")

    # Check that there is ctc data collection
    # Check that there is only one header
    # Check that all nodes have one frame
    # Check that there is at least one ctc group with 2 nodes
    # Check that all ctc objects are parented to the header
    # Check that parenting structure is valid
    # Check that all nodes objects have valid child of constraints

    errorList = []

    # Check that there is ctc data collection
    if bpy.data.collections.get(ctcCollectionName) != None:
        objList = bpy.data.collections[ctcCollectionName].all_objects
    else:
        errorList.append("CTC objects must be contained in a collection.")
        objList = []
    headerCount = 0

    for obj in objList:

        if obj.get("TYPE", None) == "CTC_HEADER":
            # Check that there is only one header
            headerCount += 1
            if obj.parent != None:
                errorList.append("CTC Header cannot be a child of another object.")

        elif obj.get("TYPE", None) == "CTC_NODE":
            # Check that all nodes have one frame
            childFrame = None
            for child in obj.children:
                if child.get("TYPE", None) == "CTC_NODE_FRAME":
                    if childFrame != None:
                        errorList.append("CTC Node " + obj.name + " has more than one frame parented to it.")
                    else:
                        childFrame = child
            if childFrame == None:
                errorList.append("CTC Node " + obj.name + " has no frame parented to it.")
            # Check that nodes parenting structure is valid
            validParentTypeList = ["CTC_CHAIN", "CTC_NODE"]
            if obj.parent != None:
                if obj.parent.get("TYPE", None) not in validParentTypeList:
                    errorList.append(obj.name + " node cannot be parented to an object of type: " + str(
                        obj.parent.get("TYPE", None)))
            else:
                errorList.append(obj.name + " node must be parented to a CTC Chain or a CTC Node object.")
            # Check that all nodes have valid child of constraints
            if obj.constraints.get("BoneName", False):
                if obj.constraints["BoneName"].target == "" or obj.constraints["BoneName"].target == None or \
                        obj.constraints["BoneName"].subtarget == "":
                    errorList.append("Invalid child of constraint on " + obj.name)
            else:
                errorList.append("Child of constraint missing on " + obj.name)
        # Check that all ctc objects are parented to the header
        elif obj.get("TYPE", None) == "CTC_CHAIN":
            # Check that chains parenting structure is valid
            validParentTypeList = ["CTC_HEADER"]
            if obj.parent != None:
                if obj.parent.get("TYPE", None) not in validParentTypeList:
                    errorList.append(obj.name + " must be parented to a CTC Header object.")
            else:
                errorList.append(obj.name + " must be parented to a CTC Header object.")
            # Check that there is at least one ctc group with 2 nodes
            validctcGroup = False
            for child in obj.children:
                if child.get("TYPE") == "CTC_NODE":
                    # validctcGroup = True
                    for nodeChild in child.children:
                        if nodeChild.get("TYPE") == "CTC_NODE":
                            validctcGroup = True
            if not validctcGroup:
                errorList.append(obj.name + " must contain at least 2 nodes.")

    if headerCount == 0:
        errorList.append("No CTC Header object in collection.")

    elif headerCount > 1:
        errorList.append("Cannot export with more than one CTC Header in a collection.")

    if errorList == []:
        print("No problems found.")
        return True
    else:
        errorString = ""
        for error in errorList:
            errorString += textColors.FAIL + "ERROR: " + error + textColors.ENDC + "\n"
        showMessageBox(
            "CTC structure contains errors and cannot export. Check Window > Toggle System Console for details.",
            title="Export Error", icon="ERROR")
        print(errorString)
        print(textColors.FAIL + "__________________________________\nCTC export failed." + textColors.ENDC)
        return False


class reportINFO1(bpy.types.Operator):
    bl_idname = "ctc.report_info1"
    bl_label = "Report INFO1"
    bl_options = {"UNDO"}

    def execute(self, context):
        self.report({"INFO"}, "Successfully exported MHW CCL.")
        return {'FINISHED'}

class reportINFO2(bpy.types.Operator):
    bl_idname = "ctc.report_info2"
    bl_label = "Report INFO2"
    bl_options = {"UNDO"}

    def execute(self, context):
        self.report({"INFO"}, "MHW CCL export failed. See Window > Toggle System Console for details.")
        return {'FINISHED'}

def exportCTCFile(filepath,options):
    valid = ctcErrorCheck(options["targetCollection"])
    # valid = True
    ctcCollection = bpy.data.collections.get(options["targetCollection"],None)
    if valid and ctcCollection != None:
        print(textColors.OKCYAN + "__________________________________\nCTC export started." + textColors.ENDC)
        newctcFile = CTCFile()

        objList = ctcCollection.all_objects
        ctcSettingsObjList = []
        ctcNodeObjList = []

        for obj in objList:
            objType = obj.get("TYPE", None)
            if objType == "CTC_HEADER":
                headerObj = obj
            elif objType == "CTC_CHAIN":
                ctcSettingsObjList.append(obj)
            elif objType == "CTC_NODE":
                ctcNodeObjList.append(obj)


        # ctcSettingsObjList.sort(key=lambda item: item.name)
        # ctcNodeObjList.sort(key=lambda item: item.name)

        newctcFile.Header.ChainGroupCount = len(ctcSettingsObjList)
        newctcFile.Header.ChainNodeTotalCount = len(ctcNodeObjList)

        setCTCHeaderData(newctcFile.Header, headerObj)

        for ctcSettingsObj in ctcSettingsObjList:
            ctcSettings = CTCSettingsData()
            setctcSettingsData(ctcSettings, ctcSettingsObj)

            nodeNumList = []
            currentNode = ctcSettingsObj.children[0]
            nodeNumList = [currentNode]
            hasChildNode = True
            while hasChildNode:
                currentNodeHasChildNode = False
                for child in currentNode.children:
                    if child.get("TYPE", None) == "CTC_NODE":
                        nodeNumList.append(child)
                        currentNode = child
                        currentNodeHasChildNode = True
                if not currentNodeHasChildNode:
                    hasChildNode = False
            ctcSettings.NodeNum = len(nodeNumList)
            newctcFile.CTCSettingsList.append(ctcSettings)

        for ctcNodeObj in ctcNodeObjList:
            ctcNode = CTCNodeData()
            setCTCNodeData(ctcNode, ctcNodeObj)
            #print(ctcNode.boneFunctionID)
            newctcFile.CTCNodesList.append(ctcNode)



        print("CTC Conversion Finished")
        writeCTC(newctcFile, filepath)

        if options["exportccl"]:
            filepath = filepath.split(".ctc")[0] + ".ccl"
            success = exportCCLFile(filepath, options)
            if success:
                bpy.ops.ctc.report_info1()

            else:
                bpy.ops.ctc.report_info2()



        return True



def importCCLFile(filepath, options):
    #初始化变量armature，用于存储找到的骨架对象
    armature = None
    #检查在Blender数据中是否存在指定名称的骨架，如果存在，则调用findArmatureObjFromData函数获取该骨架对象，并将其赋值给armature
    if bpy.data.armatures.get(options["targetArmature"]) != None:
        armature = findArmatureObjFromData(bpy.data.armatures[options["targetArmature"]])
    try:
        #如果之前没有找到骨架，并且当前活动对象存在且为骨架类型，则将当前活动对象赋值给armature
        if armature == None and bpy.context.active_object != None and bpy.context.active_object.type == "ARMATURE":
            armature = bpy.context.active_object
    except:
        pass
    #如果仍然未找到骨架，则遍历当前场景中所有的对象
    if armature == None:
        for obj in bpy.context.scene.objects:
            #如果找到多个骨架，则报错提示
            if obj.type == "ARMATURE" and armature != None:
                showErrorMessageBox(
                    "More than one armature was found in the scene. Select an armature before importing the ccl file.")
                return False
            if obj.type == "ARMATURE":
                armature = obj
    #如果到最后都没有找到骨架，则报错提示
    if armature == None:
        showErrorMessageBox(
            "No armature in scene. The armature from the mod3 file must be present in order to import the ccl file.")
        return False

    CCLFile = readCCL(filepath)

    removedItems = []
    j = len(CCLFile.CCLCollisionList)
    #检查ccl文件中的boneFunctionID是否存在对应的骨骼
    for groupIndex, cclGroup in enumerate(CCLFile.CCLCollisionList):
        # 索引每节cclGroup包含的ID
        startboneIDname = "bonefunction_" + str(cclGroup.startboneID).zfill(3)
        endboneIDname = "bonefunction_" + str(cclGroup.endboneID).zfill(3)
        startBoneID = findBone(startboneIDname, armature)
        endBoneID = findBone(endboneIDname, armature)

        #若头尾其中之一找不到对应的骨骼，则移除当前CCLGroup
        if startBoneID == None or endBoneID == None:
            removedItems.append(cclGroup)

    for item in removedItems:
        CCLFile.CCLCollisionList.remove(item)
    #若导入时设置要merge的集合，则搜索该集合以及其ctcheader是否存在
    headerObj = None
    if bpy.data.collections.get(options["mergeChain"]):  # Merge with existing ctc header if this is set
        headerObj = findHeaderObj(bpy.data.collections[options["mergeChain"]])
        ctcCollection = bpy.data.collections[options["mergeChain"]]
        mergedChain = True
    #若上一步未设置merge或未搜索到指定的集合，则默认导入到当前激活的ctc集合内
    if headerObj == None:
        mergedChain = False
        ctcCollection = bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection, None)
        headerObj = findHeaderObj(ctcCollection)

    print(f"CCL Collisions Count: {j}", f"Imported Count: {len(CCLFile.CCLCollisionList)}")

    if ctcCollection != None and (headerObj != None):
        if len(CCLFile.CCLCollisionList) > 0:
            cclname = ctcCollection.name.split(".")[0]
            if mergedChain == True:
                cclCollection = getCollection(f"CCL Entries - {cclname}.ccl", ctcCollection,
                                                makeNew=not mergedChain)
            else:
                cclCollection = getCollection(f"CCL Entries - {cclname}.ccl", ctcCollection,
                                              makeNew=False)

            cclCollection["TYPE"] = "CCL_COLLISION_COLLECTION"

        for collisionIndex, cclCollision in enumerate(CCLFile.CCLCollisionList):
            currentCollisionIndex = collisionIndex
            subName = "CCL_" + str(currentCollisionIndex).zfill(2)

            while (checkNameUsage(subName, checkSubString=True)):
                currentCollisionIndex += 1
                subName = "CCL_" + str(currentCollisionIndex).zfill(2)

            if cclCollision.ColShape != 1:
                shape = "SPHERE"
                name = "CCL_" + str(currentCollisionIndex).zfill(2) + "_" + shape + " " + "bonefunction_" + str(cclCollision.startboneID).zfill(3)
                colSphereObj = createCurveEmpty(name, [("TYPE", "CCL_SPHERE")], headerObj,
                                                cclCollection)
                getCCLCollision(cclCollision, colSphereObj)

                colSphereObj.ccl_collision.StartColOffset = (
                    cclCollision.startPosX, cclCollision.startPosY, cclCollision.startPosZ)

                constraint = colSphereObj.constraints.new(type="CHILD_OF")
                constraint.target = armature
                constraint.subtarget = "bonefunction_" + str(cclCollision.startboneID).zfill(3)
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

            else:
                shape = "CAPSULE"
                name = subName + f"_{shape} - " + "bonefunction_" + str(cclCollision.startboneID).zfill(3) + " > " + "bonefunction_" + str(cclCollision.endboneID).zfill(3)
                colCapsuleRootObj = createCurveEmpty(name, [("TYPE", "CCL_CAPSULE")], headerObj,
                                                     cclCollection)
                lockObjTransforms(colCapsuleRootObj)
                getCCLCollision(cclCollision, colCapsuleRootObj)
                name = subName + f"_{shape}_HEAD" + " " + "bonefunction_" + str(cclCollision.startboneID).zfill(3)

                colCapsuleStartObj = createFakeEmptySphere(name, [("TYPE", "CCL_CAPSULE_START")],
                                                           colCapsuleRootObj, cclCollection)

                colCapsuleRootObj.show_in_front = bpy.context.scene.ctc_toolpanel.drawCollisionsThroughObjects
                colCapsuleStartObj.ccl_collision.StartColOffset = (
                    cclCollision.startPosX, cclCollision.startPosY, cclCollision.startPosZ)

                constraint = colCapsuleStartObj.constraints.new(type="CHILD_OF")
                constraint.target = armature
                constraint.subtarget = "bonefunction_" + str(cclCollision.startboneID).zfill(3)
                constraint.name = "BoneName"

                constraint.use_scale_x = False
                constraint.use_scale_y = False
                constraint.use_scale_z = False

                colCapsuleStartObj.show_name = bpy.context.scene.ctc_toolpanel.showCollisionNames
                colCapsuleStartObj.show_in_front = bpy.context.scene.ctc_toolpanel.drawCapsuleHandlesThroughObjects

                name = subName + f"_{shape}_TAIL" + " " + "bonefunction_" + str(cclCollision.endboneID).zfill(3)
                colCapsuleEndObj = createFakeEmptySphere(name, [("TYPE", "CCL_CAPSULE_END")],
                                                         colCapsuleRootObj, cclCollection)

                colCapsuleEndObj.ccl_collision.EndColOffset = (
                    cclCollision.endPosX, cclCollision.endPosY, cclCollision.endPosZ)

                constraint = colCapsuleEndObj.constraints.new(type="CHILD_OF")
                constraint.target = armature
                constraint.subtarget = "bonefunction_" + str(cclCollision.endboneID).zfill(3)
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
    return True

def cclErrorCheck(ctcCollectionName):
    print("\nChecking for problems with ccl structure...")

    # Check that there is ctc data collection
    # Check that there is only one header
    # Check that all capsule collisions have both ends
    # Check that all ccl objects are parented to the header
    # Check that parenting structure is valid
    # Check that ccl collision objects have valid child of constraints

    errorList = []

    # Check that there is ctc data collection
    if bpy.data.collections.get(ctcCollectionName) != None:
        objList = bpy.data.collections[ctcCollectionName].all_objects
    else:
        errorList.append("CCL objects must be contained in a ctc collection.")
        objList = []
    headerCount = 0

    for obj in objList:

        if obj.get("TYPE", None) == "CTC_HEADER":
            # Check that there is only one header
            headerCount += 1
            if obj.parent != None:
                errorList.append("CTC Header cannot be a child of another object.")

        elif obj.get("TYPE", None) == "CCL_SPHERE":
            # Check that all ccl objects are parented to the header
            if obj.parent != None:
                if obj.parent.get("TYPE", None) != "CTC_HEADER":
                    errorList.append(obj.name + " object must be parented to a ctc header object")
            else:
                errorList.append(obj.name + " object must be parented to a ctc header object")
            # Check that ccl collision objects have valid child of constraints
            if obj.constraints.get("BoneName", False):
                if obj.constraints["BoneName"].target == "" or obj.constraints["BoneName"].target == None or \
                        obj.constraints["BoneName"].subtarget == "":
                    errorList.append("Invalid child of constraint on " + obj.name)
            else:
                errorList.append("Child of constraint missing on " + obj.name)

        elif obj.get("TYPE", None) == "CCL_CAPSULE":
            # Check that all ccl objects are parented to the header
            if obj.parent != None:
                if obj.parent.get("TYPE", None) != "CTC_HEADER":
                    errorList.append(obj.name + " object must be parented to a ctc header object")
            else:
                errorList.append(obj.name + " object must be parented to a ctc header object")

            startCapsule = None
            for child in obj.children:
                if child.get("TYPE", None) == "CCL_CAPSULE_START":
                    if startCapsule != None:
                        errorList.append(
                            "Collision capsule " + obj.name + " has more than one head node parented to it.")
                    else:
                        startCapsule = child
            if startCapsule == None:
                errorList.append("Collision capsule " + obj.name + " has no head node parented to it.")
            # Check that ccl collision objects have valid child of constraints
            else:
                if startCapsule.constraints.get("BoneName", False):
                    if startCapsule.constraints["BoneName"].target == "" or startCapsule.constraints[
                        "BoneName"].target == None or startCapsule.constraints["BoneName"].subtarget == "":
                        errorList.append("Invalid child of constraint on " + startCapsule.name)
                else:
                    errorList.append("Child of constraint missing on " + startCapsule.name)

            endCapsule = None
            for child in obj.children:
                if child.get("TYPE", None) == "CCL_CAPSULE_END":
                    if endCapsule != None:
                        errorList.append(
                            "Collision capsule " + obj.name + " has more than one tail node parented to it.")
                    else:
                        endCapsule = child
            if endCapsule == None:
                errorList.append("Collision capsule " + obj.name + " has no tail node parented to it.")
            # Check that ccl collision objects have valid child of constraints
            else:
                if endCapsule.constraints.get("BoneName", False):
                    if endCapsule.constraints["BoneName"].target == "" or endCapsule.constraints[
                        "BoneName"].target == None or endCapsule.constraints["BoneName"].subtarget == "":
                        errorList.append("Invalid child of constraint on " + endCapsule.name)
                else:
                    errorList.append("Child of constraint missing on " + endCapsule.name)

    if headerCount == 0:
        errorList.append("No CTC Header object in collection.")

    elif headerCount > 1:
        errorList.append("Cannot export with more than one CTC Header in a collection.")

    if errorList == []:
        print("No problems found.")
        return True
    else:
        errorString = ""
        for error in errorList:
            errorString += textColors.FAIL + "ERROR: " + error + textColors.ENDC + "\n"
        showMessageBox(
            "CCL structure contains errors and cannot export. Check Window > Toggle System Console for details.",
            title="Export Error", icon="ERROR")
        print(errorString)
        print(textColors.FAIL + "__________________________________\nCCL export failed." + textColors.ENDC)
        return False



def exportCCLFile(filepath,options):
    valid = cclErrorCheck(options["targetCollection"])
    # valid = True
    ctcCollection = bpy.data.collections.get(options["targetCollection"],None)
    if valid and ctcCollection != None:
        print(textColors.OKCYAN + "__________________________________\nCCL export started." + textColors.ENDC)
        newcclFile = CCLFile()

        objList = ctcCollection.all_objects
        cclCollisionsObjList = []


        for obj in objList:
            objType = obj.get("TYPE", None)
            if objType == "CCL_SPHERE" or objType == "CCL_CAPSULE":
                cclCollisionsObjList.append(obj)


        # cclCollisionsObjList.sort(key=lambda item: item.name)

        newcclFile.Header.CCLCollisionCount = len(cclCollisionsObjList)
        newcclFile.Header.CCLCollisionTotalOffset = len(cclCollisionsObjList)*64

        for cclCollisionObj in cclCollisionsObjList:
            cclCollision = CCLCollisionData()
            setCCLCollisionData(cclCollision, cclCollisionObj)
            newcclFile.CCLCollisionList.append(cclCollision)

        print("CCL Conversion Finished")
        writeCCL(newcclFile, filepath)
        return True


#创建新的CTC集合
#参数：collectionName（表示新集合的名称），parentCollection（表示新集合的父集合，默认为None，即没有父集合）
def createctcCollection(collectionName,parentCollection = None):
    #创建一个新集合，集合名称为collectionName
    collection = bpy.data.collections.new(collectionName)
    #给新集合设置一个颜色标签
    collection.color_tag = "COLOR_02"
    #给新集合添加一个自定义属性 ~TYPE，并将其值设置为 "ctc_COLLECTION"
    collection["~TYPE"] = "CTC_COLLECTION"
    #如果有父集合，则将新集合作为子集合；如果没有父集合，则将新集合添加到当前场景的主集合中
    if parentCollection != None:
        parentCollection.children.link(collection)
    else:
        bpy.context.scene.collection.children.link(collection)
    #更新CTC Tools面板中集合索引框内的集合名称
    bpy.context.scene.ctc_toolpanel.ctcCollection = collection.name
    #返回新创建的集合对象
    return collection

#根据提供的集合名称（collectionName）获取对应的集合
#参数：collectionName（要获取或创建的集合的名称），parentCollection（表示新集合的父集合，默认为None，即没有父集合），makeNew（布尔值，指定当集合不存在时是否创建新集合，默认为False）
def getCollection(collectionName,parentCollection = None,makeNew = False):
    if makeNew or not bpy.data.collections.get(collectionName):
        collection = bpy.data.collections.new(collectionName)
        collectionName = collection.name
        if parentCollection != None:
            parentCollection.children.link(collection)
        else:
            bpy.context.scene.collection.children.link(collection)
    return bpy.data.collections[collectionName]

#创建新的空物体
#参数：name（表示新空物体的名称），propertyList（一个二元元组列表，是该空物体的自定义属性列表），parent（表示新空物体的父级对象，默认为None，即没有父级），collection（表示新空物体的父集合，默认为None，即没有父集合）
def createEmpty(name, propertyList, parent=None, collection=None):
    #创建一个新空物体，None表示空物体不需要网格数据
    obj = bpy.data.objects.new(name, None)
    #设置空物体的显示尺寸为0.1，以及显示类型为“纯轴”
    obj.empty_display_size = .10
    obj.empty_display_type = 'PLAIN_AXES'
    #如果提供了parent参数，将新创建的空物体设为其子级
    obj.parent = parent
    #遍历propertyList列表，为每个属性设置相应的值。其中property[0]是属性名，property[1]是属性值
    for property in propertyList:
        obj[property[0]] = property[1]
    #如果没有指定collection参数，则将新创建的空物体添加到当前场景的活动集合中
    if collection == None:
        collection = bpy.context.scene.collection
    #将新创建的空物体链接到指定的集合中
    collection.objects.link(obj)
    #返回新创建的空物体对象
    return obj

#创建新的空曲线
#参数：name（表示新空曲线的名称），propertyList（一个二元元组列表，是该空曲线的自定义属性列表），parent（表示新空曲线的父级对象，默认为None，即没有父级），collection（表示新空曲线的父集合，默认为None，即没有父集合）
def createCurveEmpty(name, propertyList, parent=None, collection=None):
    CURVE_DATA_NAME = "emptyCurve"
    #检查Blender数据中是否已经存在名为"emptyCurve"的曲线数据，如果存在，则将其赋值给curveData；如果不存在，则创建一个新的曲线数据
    if CURVE_DATA_NAME in bpy.data.curves:
        curveData = bpy.data.curves[CURVE_DATA_NAME]
    else:
        curveData = bpy.data.curves.new(CURVE_DATA_NAME, 'CURVE')
        #曲线不作为路径使用
        curveData.use_path = False

    obj = bpy.data.objects.new(name, curveData)
    obj.parent = parent
    for property in propertyList:
        obj[property[0]] = property[1]
    if collection == None:
        collection = bpy.context.scene.collection

    collection.objects.link(obj)

    return obj


splinePointList = [([(-1.1, 0.0, 0.0), (0.0, 1.1, 0.0), (1.1, 0.0, 0.0), (0.0, -1.1, 0.0)],
                    [(-1.1, -0.6073, 0.0), (-0.6073, 1.1, 0.0), (1.1, 0.6073, 0.0), (0.6073, -1.1, 0.0)],
                    [(-1.1, 0.6073, 0.0), (0.6073, 1.1, 0.0), (1.1, -0.6073, 0.0), (-0.6073, -1.1, 0.0)]), (
                   [(-1.1, 0.0, 0.0), (0.0, -0.0, -1.1), (1.1, 0.0, 0.0), (0.0, 0.0, 1.1)],
                   [(-1.1, 0.0, 0.6073), (-0.6073, -0.0, -1.1), (1.1, -0.0, -0.6073), (0.6073, 0.0, 1.1)],
                   [(-1.1, -0.0, -0.6073), (0.6073, -0.0, -1.1), (1.1, 0.0, 0.6073), (-0.6073, 0.0, 1.1)]), (
                   [(0.0, 0.0, 1.1), (0.0, 1.1, -0.0), (-0.0, -0.0, -1.1), (-0.0, -1.1, 0.0)],
                   [(0.0, -0.6073, 1.1), (0.0, 1.1, 0.6073), (-0.0, 0.6073, -1.1), (-0.0, -1.1, -0.6073)],
                   [(0.0, 0.6073, 1.1), (0.0, 1.1, -0.6073), (-0.0, -0.6073, -1.1), (-0.0, -1.1, 0.6073)])]
def createFakeEmptySphere(name, propertyList, parent=None, collection=None):
    CURVE_DATA_NAME = "fakeEmptySphere"  # Share the data for all empty curves since it's not needed and it prevents unnecessary duplicates
    if CURVE_DATA_NAME in bpy.data.curves:
        curveData = bpy.data.curves[CURVE_DATA_NAME]
    else:
        curveData = bpy.data.curves.new(CURVE_DATA_NAME, 'CURVE')
        curveData.use_path = False
        for pointSet in splinePointList:
            coordList = pointSet[0]
            leftList = pointSet[1]
            rightList = pointSet[2]
            spline = curveData.splines.new(type='BEZIER')
            spline.use_cyclic_u = True
            spline.bezier_points.add(3)
            for index, point in enumerate(spline.bezier_points):
                point.co = coordList[index]
                point.handle_left = leftList[index]
                point.handle_right = rightList[index]

    obj = bpy.data.objects.new(name, curveData)
    obj.parent = parent
    for property in propertyList:
        obj[property[0]] = property[1]
    if collection == None:
        collection = bpy.context.scene.collection
    collection.objects.link(obj)
    return obj



def alignctcs():
    for ctc in [obj for obj in bpy.context.scene.objects if obj.get("TYPE", None) == "CTC_CHAIN"]:
        if len(ctc.children) > 0:
            currentNode = ctc.children[0]
            nodeObjList = [currentNode]
            while len(currentNode.children) > 1:
                currentNode.location = (0.0, 0.0, 0.0)
                currentNode.rotation_euler = (0.0, 0.0, 0.0)
                currentNode.scale = (1.0, 1.0, 1.0)

                hasNodeChild = False
                for child in currentNode.children:
                    if child.get("TYPE", None) == "CTC_NODE":
                        nodeObjList.append(child)
                        hasNodeChild = True

                        currentNode = child
                if not hasNodeChild:  # Avoid infinite loop in the case of a ctc group consisting of a single node that contains a jiggle node
                    break
            nodeObjList.reverse()
            for recurse in nodeObjList:
                if recurse.ctc_node.boneColRadius != 0:
                    recurse.empty_display_size = 0.01*recurse.ctc_node.boneColRadius  # * 100
                else:
                    recurse.empty_display_size = .01
                for obj in nodeObjList:
                    try:
                        obj.constraints["BoneName"].inverse_matrix = obj.parent.matrix_world.inverted()
                    except:
                        pass
                bpy.context.view_layer.update()

def alignCollisions():#TODO Fix matrices
    collisionTypeList = [
        "CCL_SPHERE",
        "CCL_CAPSULE",
        ]
    for collisionObj in [obj for obj in bpy.context.scene.objects if (obj.get("TYPE",None) in collisionTypeList)] :
        if collisionObj.get("TYPE",None) == "CCL_SPHERE":
            collisionObj.constraints["BoneName"].inverse_matrix = collisionObj.parent.matrix_world.inverted()
            collisionObj.ccl_collision.radius = collisionObj.scale[0]
        else:
            for child in collisionObj.children:
                if child.get("TYPE",None) == "CCL_CAPSULE_END" or child.get("TYPE",None) == "CCL_CAPSULE_START":
                    child.constraints["BoneName"].inverse_matrix = child.parent.matrix_world.inverted()
                    if child["TYPE"] == "CCL_CAPSULE_START":
                        collisionObj.ccl_collision.radius = child.scale[0]
    bpy.context.view_layer.update()


def setctcBoneColor(armatureObj):
    #TODO Add theme option in preferences
    THEME = "THEME03"
    if armatureObj != None:
        if bpy.app.version < (4,0,0):
            if armatureObj.pose.bone_groups.get("CTC Chain Bones",None) != None:
                boneGroup = armatureObj.pose.bone_groups["CTC Chain Bones"]
            else:
                boneGroup = armatureObj.pose.bone_groups.new(name = "CTC Chain Bones")
            boneGroup.color_set = THEME
        ctcCollection = bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection)
        if ctcCollection != None:
            objList = ctcCollection.all_objects
        else:
            objList = bpy.data.objects
        try:
            ctcBoneList = [obj.constraints["BoneName"].subtarget for obj in objList if obj.get("TYPE",None) == "CTC_NODE"]
        except:
            ctcBoneList = []
        for ctcBone in ctcBoneList:
            if bpy.app.version < (4,0,0):
                poseBone = armatureObj.pose.bones.get(ctcBone,None)
                if poseBone != None:
                    poseBone.bone_group = boneGroup
            else:
                if ctcBone in armatureObj.data.bones:
                    bone = armatureObj.data.bones[ctcBone]
                    bone.color.palette = THEME

#为对象添加限制约束来锁定其位置、旋转和缩放变换
def lockObjTransforms(obj, lockLocation=True, lockRotation=True, lockScale=True):
    if lockLocation:
        constraint = obj.constraints.new(type="LIMIT_LOCATION")
        constraint.use_min_x = True
        constraint.use_min_y = True
        constraint.use_min_z = True

        constraint.use_max_x = True
        constraint.use_max_y = True
        constraint.use_max_z = True
    if lockRotation:
        constraint = obj.constraints.new(type="LIMIT_ROTATION")
        constraint.use_limit_x = True
        constraint.use_limit_y = True
        constraint.use_limit_z = True

    if lockScale:
        constraint = obj.constraints.new(type="LIMIT_SCALE")
        constraint.use_min_x = True
        constraint.use_min_y = True
        constraint.use_min_z = True

        constraint.use_max_x = True
        constraint.use_max_y = True
        constraint.use_max_z = True

        constraint.min_x = 1.0
        constraint.max_x = 1.0
        constraint.min_y = 1.0
        constraint.max_y = 1.0
        constraint.min_z = 1.0
        constraint.max_z = 1.0

#获取指定的CTC集合
#
def findHeaderObj(ctcCollection = None):
    #如果未提供ctcCollection参数，则从CTC TOOLS面板的集合索引框获取CTC集合的名称，并据此查找对应的集合
    if ctcCollection == None:
        if bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection,None) != None:
            ctcCollection = bpy.data.collections[bpy.context.scene.ctc_toolpanel.ctcCollection]
    #如果提供了ctcCollection参数，则获取该集合中的所有对象
    if ctcCollection != None:
        objList = ctcCollection.all_objects
        #遍历该集合中的所有对象，获取其中的CTC Header空物体
        headerList = [obj for obj in objList if obj.get("TYPE",None) == "CTC_HEADER"]
        #如果找到了至少一个CTC Header空物体，则返回其中第一个
        if len(headerList) >= 1:
            return headerList[0]
        #如果未找到任何CTC Header空物体，则返回None
        else:
            return None
    else:
        return None

#检查在给定对象列表中是否存在与基础名称（baseName）匹配的对象名称
#参数：baseName（要检查的基础名称字符串），checkSubString（布尔值，指定是否将baseName作为子字符串进行检查，默认为True），objList（对象列表，默认为None）
def checkNameUsage(baseName,checkSubString = True, objList = None):
    #若未提供对象列表，则获取当前场景中的所有对象
    if objList == None:
        objList = bpy.data.objects
    #若checkSubString为True，则检查baseName是否作为子字符串出现在对象列表中；若为False，则检查baseName是否精确匹配对象列表中某个对象的名称
    if checkSubString:
        return any(baseName in name for name in [obj.name for obj in objList])
    else:
        return baseName in [obj.name for obj in objList]

#检查给定的ctcSettingsID是否在作为某个CTC Settings空物体的ctc_settings.id属性值存在
# def checkctcSettingsIDUsage(ctcSettingsID):
#     idList = [obj.ctc_settings.id for obj in bpy.context.scene.objects if obj.get("TYPE",None) == "CTC_CHAIN"]
#     if ctcSettingsID in idList:
#         return True
#     else:
#         return False