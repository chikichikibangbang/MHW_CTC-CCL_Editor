#Author: NSA Cloud
import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty
import math

from ..operators.file_ccl import CCLCollisionData
from ..operators.file_ctc import ColAttrFlag, ChaAttrFlag
from ..operators.rw_presets import reloadPresets


def update_NodeNameVis(self, context):
    for obj in bpy.data.objects:
        if obj.get("TYPE",None) == "CTC_NODE":
            obj.show_name = self.showNodeNames
def update_angleLimitConeVis(self, context):
    for obj in bpy.data.objects:
        if obj.get("TYPE",None) == "CTC_NODE_FRAME_HELPER" and not obj.get("isLastNode"):
            obj.hide_viewport = not self.showAngleLimitCones
def update_DrawNodesThroughObjects(self, context):
    for obj in bpy.data.objects:
        if obj.get("TYPE",None) == "CTC_NODE" or obj.get("TYPE",None) == "CTC_NODE_FRAME":
            obj.show_in_front = self.drawNodesThroughObjects
def update_DrawConesThroughObjects(self, context):
    for obj in bpy.data.objects:
        if obj.get("TYPE",None) == "CTC_NODE_FRAME_HELPER":
            obj.show_in_front = self.drawConesThroughObjects
def update_angleLimitSize(self, context):
    for obj in bpy.data.objects:
        if obj.get("TYPE",None) == "CTC_NODE_FRAME":
            obj.empty_display_size = 0.01*self.angleLimitDisplaySize
def update_coneSize(self, context):
    for obj in bpy.data.objects:
        if obj.get("TYPE", None) == "CTC_NODE_FRAME_HELPER":

            xScaleModifier = 1.0
            yScaleModifier = 1.0
            zScaleModifier = 1.0

            # Get ctc node to check settings
            if obj.parent != None and obj.parent.parent != None and obj.parent.parent.get("TYPE") == "CTC_NODE":
                nodeObj = obj.parent.parent
                if nodeObj.ctc_node.AngleMode == "2": #AngleMode_LimitHinge
                    zScaleModifier = .01
                elif nodeObj.ctc_node.AngleMode == "3": #AngleMode_LimitOval
                    zScaleModifier = nodeObj.ctc_node.WidthRate
            obj.scale = (0.001*self.coneDisplaySize * xScaleModifier, 0.001*self.coneDisplaySize * yScaleModifier,
                         0.001*self.coneDisplaySize * zScaleModifier)



def update_AngleLimitMode(self, context):
    obj = self.id_data
    #Get child frame, then get the angle limt cone from frame
    if type(obj).__name__ == "Object":#Check if it's an object to prevent issues with clipboard
        if obj.get("TYPE",None) == "CTC_NODE":
            for child in obj.children:
                if child.get("TYPE",None) == "CTC_NODE_FRAME":
                    for frameChild in child.children:
                        if frameChild.get("TYPE",None) == "CTC_NODE_FRAME_HELPER":
                            #Determine cone scale
                            xScaleModifier = 1.0
                            yScaleModifier = 1.0
                            zScaleModifier = 1.0
                            if obj.ctc_node.AngleMode == "2": #AngleMode_LimitHinge
                                zScaleModifier = .01
                            elif obj.ctc_node.AngleMode == "3": #AngleMode_LimitOval
                                # zScaleModifier = .5
                                zScaleModifier = obj.ctc_node.WidthRate
                            frameChild.scale = (0.001*bpy.context.scene.ctc_toolpanel.coneDisplaySize*xScaleModifier,0.001*bpy.context.scene.ctc_toolpanel.coneDisplaySize*yScaleModifier,0.001*bpy.context.scene.ctc_toolpanel.coneDisplaySize*zScaleModifier)


def update_AngleLimitRad(self, context):
    obj = self.id_data
    # Get child frame, then get the angle limit cone from frame
    if type(obj).__name__ == "Object":  # Check if it's an object to prevent issues with clipboard
        if obj.get("TYPE", None) == "CTC_NODE":
            for child in obj.children:
                if child.get("TYPE", None) == "CTC_NODE_FRAME":
                    for frameChild in child.children:
                        if frameChild.get("TYPE", None) == "CTC_NODE_FRAME_HELPER":

                            if "CTCGeometryNodes" in frameChild.modifiers:
                                modifier = frameChild.modifiers["CTCGeometryNodes"]
                                if bpy.app.version < (4, 0, 0):
                                    modifier["Input_0"] = obj.ctc_node.AngleLimitRadius
                                else:
                                    modifier["Socket_0"] = obj.ctc_node.AngleLimitRadius
                                modifier.node_group.interface_update(context)
                            # print("Set modifier value")
                        # frameChild.data.spOT_ctcsize = obj.ctc_ctcnode.angleLimitRad
def update_NodeRadius(self, context):
    obj = self.id_data
    if type(obj).__name__ == "Object":#Check if it's an object to prevent issues with clipboard
        if obj.ctc_node.boneColRadius != 0:
            obj.empty_display_size = 0.01*obj.ctc_node.boneColRadius# * 100
        else:
            obj.empty_display_size = 0.01

def update_collisionColor(self, context):
    if "CCLCollisionMat" in bpy.data.materials:
        mat = bpy.data.materials["CCLCollisionMat"]
        mat.diffuse_color = self.collisionColor
        mat.node_tree.nodes[0].inputs["Base Color"].default_value = bpy.context.scene.ctc_toolpanel.collisionColor
        mat.node_tree.nodes[0].inputs["Alpha"].default_value = bpy.context.scene.ctc_toolpanel.collisionColor[3]
def update_coneColor(self, context):
    if "CTCConeMat" in bpy.data.materials:
        mat = bpy.data.materials["CTCConeMat"]
        mat.diffuse_color = self.coneColor
        mat.node_tree.nodes[0].inputs["Base Color"].default_value = bpy.context.scene.ctc_toolpanel.coneColor
        mat.node_tree.nodes[0].inputs["Alpha"].default_value = bpy.context.scene.ctc_toolpanel.coneColor[3]
def update_RelationLinesVis(self, context):
    bpy.context.space_data.overlay.show_relationship_lines = self.showRelationLines
def update_hideLastNodeAngleLimit(self, context):
    for obj in bpy.data.objects:
        if obj.get("TYPE",None) == "CTC_NODE_FRAME_HELPER" and obj.get("isLastNode"):
            obj.hide_viewport = self.hideLastNodeAngleLimit

def update_CollisionNameVis(self, context):
    collisionTypes = [
        "CCL_SPHERE",
        "CCL_CAPSULE_START",
        "CCL_CAPSULE_END"]
    for obj in bpy.data.objects:
        if obj.get("TYPE",None) in collisionTypes:
            obj.show_name = self.showCollisionNames

def update_DrawCollisionsThroughObjects(self, context):
    collisionTypes = [
        "CCL_SPHERE",
        "CCL_CAPSULE",
        ]
    for obj in bpy.data.objects:
        if obj.get("TYPE",None) in collisionTypes:
            obj.show_in_front = self.drawCollisionsThroughObjects

def update_DrawCapsuleHandlesThroughObjects(self, context):
    for obj in bpy.data.objects:
        if obj.get("TYPE",None) == "CCL_CAPSULE_START" or obj.get("TYPE",None) == "CCL_CAPSULE_END":
            obj.show_in_front = self.drawCapsuleHandlesThroughObjects

ColAttrFlag = ColAttrFlag()
def update_CollisionAttrFlagFromInt(self, context):
    if not self.internal_changingFlagValues:
        try:
            ColAttrFlag.asInt32 = self.CollisionAttrFlagValue
            self.internal_changingFlagValues = True
            for field_name, field_type, _ in ColAttrFlag.flagValues._fields_:
                setattr(self,field_name,abs(getattr(ColAttrFlag.flagValues, field_name)))
            self.internal_changingFlagValues = False
        except:
            self.internal_changingFlagValues = False
def update_IntFromCollisionAttrFlag(self, context):
    if not self.internal_changingFlagValues:
        try:
            ColAttrFlag.asInt32 = 0
            for field in ColAttrFlag.flagValues._fields_:
                fieldName = field[0]
                if fieldName in self:
                    setattr(ColAttrFlag.flagValues, fieldName, getattr(self, fieldName))

            self.internal_changingFlagValues = True
            self.CollisionAttrFlagValue = ColAttrFlag.asInt32
            self.internal_changingFlagValues = False
        except:
            self.internal_changingFlagValues = False
ChaAttrFlag = ChaAttrFlag()
def update_ChainAttrFlagFromInt(self, context):
    if not self.internal_changingFlagValues:
        try:
            ChaAttrFlag.asInt32 = self.ChainAttrFlagValue
            self.internal_changingFlagValues = True
            for field_name, field_type, _ in ChaAttrFlag.flagValues._fields_:
                setattr(self,field_name,abs(getattr(ChaAttrFlag.flagValues, field_name)))
            self.internal_changingFlagValues = False
        except:
            self.internal_changingFlagValues = False

def update_IntFromChainAttrFlag(self, context):
    if not self.internal_changingFlagValues:
        try:
            ChaAttrFlag.asInt32 = 0
            for field in ChaAttrFlag.flagValues._fields_:
                fieldName = field[0]
                if fieldName in self:
                    setattr(ChaAttrFlag.flagValues, fieldName, getattr(self, fieldName))

            self.internal_changingFlagValues = True
            self.ChainAttrFlagValue = ChaAttrFlag.asInt32
            self.internal_changingFlagValues = False
        except:
            self.internal_changingFlagValues = False

class CTCToolPanelPG(bpy.types.PropertyGroup):

    def getCTCChainPresets(self, context):
        return reloadPresets("CTCChain")

    def getCTCNodePresets(self, context):
        return reloadPresets("CTCNode")

    # def getCCLCollisionPresets(self, context):
    #     return reloadPresets("CCLCollision")

    CTCChainPresets: EnumProperty(
        name="",
        description="",
        items=getCTCChainPresets
    )
    CTCNodePresets: EnumProperty(
        name="",
        description="",
        items=getCTCNodePresets
    )
    # CCLCollisionPresets: EnumProperty(
    #     name="",
    #     description="",
    #     items=getCCLCollisionPresets
    # )
    applyPresetToChildNodes: BoolProperty(
        name="Apply to Child Nodes",
        description="Apply ctc node preset to all nodes that are a child of the selected node",
        default=False
    )
    #对应CTC Tools面板的Active CTC Collection索引框
    ctcCollection: StringProperty(
        name="",
        description="Set the collection containing the ctc file to edit."
                    "\nHint: ctc collections are orange."
                    "\nYou can create a new ctc collection by pressing the \"Create CTC Header\" button."
                    "\nThe ccl collision created will also be included in the collection",

    )
    #对应姿态模式下CTC Tools面板的创建链按钮
    ChainFromBoneLabelName: StringProperty(
        name="ChainFromBoneLabelName",
        default="Create CTC Chain From Bone",
    )
    #是否显示链节点名称
    showNodeNames: BoolProperty(
        name="Show Node Names",
        description="Show Node Names in 3D View",
        default=True,
        update=update_NodeNameVis
    )
    #是否前置显示链节点对象
    drawNodesThroughObjects: BoolProperty(
        name="Draw Nodes Through Objects",
        description="Make all ctc node and frame objects render through any objects in front of them",
        default=True,
        update=update_DrawNodesThroughObjects
    )
    #是否显示角度限制锥体
    showAngleLimitCones: BoolProperty(
        name="Show Cones",
        description="Show Angle Limit Cones in 3D View",
        default=True,
        update=update_angleLimitConeVis
    )
    #是否前置显示角度限制锥体
    drawConesThroughObjects: BoolProperty(
        name="Draw Cones Through Objects",
        description="Make all angle limit cones render through any objects in front of them",
        default=True,
        update=update_DrawConesThroughObjects
    )
    #角度限制轴的显示尺寸
    angleLimitDisplaySize: FloatProperty(
        name="Angle Limit Size",
        description="Set the display size of node angle limits",
        default=4.0,
        soft_min=0.0,
        #soft_max=.4,
        #precision=3,
        step=10,
        update=update_angleLimitSize
    )
    #角度限制锥体显示尺寸
    coneDisplaySize: FloatProperty(
        name="Cone Size",
        description="Set the display size of node angle limit cones",
        default=5.0,
        soft_min=0.0,
        #soft_max=.2,
        #precision=3,
        step=10,
        update=update_coneSize
    )
    #碰撞体颜色
    collisionColor: bpy.props.FloatVectorProperty(
        name="Collision Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.003, 0.426, 0.8, 0.3),
        update=update_collisionColor
    )
    #角度限制锥体的颜色
    coneColor: bpy.props.FloatVectorProperty(
        name="Angle Limit Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.8, 0.6, 0.0, 0.4),
        update=update_coneColor
    )
    #显示关系线
    showRelationLines: BoolProperty(
        name="Show Relation Lines",
        description="Show dotted lines indicating object parents.\nNote that this affects all objects, not just ctc objects",
        default=True,
        update=update_RelationLinesVis,
    )
    #隐藏尾骨的角度限制锥体
    hideLastNodeAngleLimit: BoolProperty(
        name="Hide Last Node Cone",
        description="Hide the last ctc node's angle limit cone.\nThis is because the last node is typically unused and has a dummy rotation value",
        default=True,
        update=update_hideLastNodeAngleLimit,
    )
    #是否显示碰撞体名称
    showCollisionNames: BoolProperty(
        name="Show Collision Names",
        description="Show CCL Collision Names in 3D View",
        default=True,
        update=update_CollisionNameVis
    )
    #是否前置显示碰撞体
    drawCollisionsThroughObjects: BoolProperty(
        name="Draw Collisions Through Objects",
        description="Make all ccl collision objects render through any objects in front of them",
        default=True,
        update=update_DrawCollisionsThroughObjects
    )
    drawCapsuleHandlesThroughObjects: BoolProperty(
        name="Draw Handles Through Objects",
        description="Make all capsule handle objects render through any objects in front of them",
        default=True,
        update=update_DrawCapsuleHandlesThroughObjects
    )

#对应CTC Header空物体的自定义属性
class CTCHeaderPG(bpy.types.PropertyGroup):
    #完
    AttributeFlags: IntProperty(
        name="Attribute Flags",
        description="Determine certain movement properties of the chain."
                    "\nIt is actually a binary, and the maximum bit may be 8 bits from testing."
                    "\nThe most common value is 64 (mostly seen on armor), followed by 80 (mostly seen on pendants)."
                    "\n80 seems to make the chain move more violently than 64, you can refer to the fluttering pendant."
                    "\nThe main difference lies in the fifth and seventh bits of binary, and it is unclear what these bits mean",
        default=64,
    )
    #完
    StepTime: FloatProperty(
        name="Step Time",
        description="The time interval between each update of the simulation by the physics engine."
                    "\nSetting the step time to 0.16666 seconds means that the physics engine updates 60 times per second, which matches a frame rate of 60FPS."
                    "\nPlease don't change this value",
        default=1/60,
    )
    #完
    GravityScaling: FloatProperty(
        name="Gravity Scaling",
        description="Multiple of the gravity applied to the chain, Usually 1."
                    "\nWhen the value is negative, the direction of gravity reverses."
                    "\nWhen the value is 0, there is no gravity",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    #完
    GlobalDamping: FloatProperty(
        name="Global Damping",
        description="The greater the damping, the greater the resistance, and the slower and more difficult the movement of the chain."
                    "\nThe smaller the damping, the smaller the resistance, and the faster and more flexible the movement of the chain."
                    "\nNormally the damping is 0 or 0.1, shouldn't be set to too high."
                    "\nA negative value will cause the chain to gain additional energy and move automatically",
        default=0.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    #完
    GlobalTransForceCoef: FloatProperty(
        name="Global TransForce Coef",
        description="When the value is 1, the trans force is equal to the acting force. This is the usual value."
                    "\nWhen the value is greater than 1, the trans force will be greater than the acting force. And the higher the value, the more intense the chain moves."
                    "\nWhen the value is less than 1, the trans force will be less than the acting force. And the smaller the value, the weaker the chain moves."
                    "\nWhen the value is negative, the trans force and acting force will reverse, causing the chain that was originally moving backward to move forward",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    #完
    SpringScaling: FloatProperty(
        name="Spring Scaling",
        description="Multiple of chain elasticity, Usually 1.\nSetting it to a negative value is not recommended, which will lead to some unstable physical behavior",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    #完
    WindScale: FloatProperty(
        name="Wind Scale",
        description="The magnitude of the wind force exposed to the chain is divided into average (median), minimum and maximum."
                    "\nThe sizes of these three parameters should be determined by default according to the rule of \"WindScaleMax>=WindScale>=WindScaleMin\"."
                    "\nJudging from the traversed CTC files, it seems that there is a relationship of \"WindScale=(WindScaleMin+WindScaleMax)/2\", which may be simply an average value",
        default=0.6,
    )
    #完
    WindScaleMin: FloatProperty(
        name="Wind Scale Min",
        description="The magnitude of the wind force exposed to the chain is divided into average (median), minimum and maximum."
                    "\nThe sizes of these three parameters should be determined by default according to the rule of \"WindScaleMax>=WindScale>=WindScaleMin\"."
                    "\nJudging from the traversed CTC files, it seems that there is a relationship of \"WindScale=(WindScaleMin+WindScaleMax)/2\", which may be simply an average value",
        default=0.3,
    )
    #完
    WindScaleMax: FloatProperty(
        name="Wind Scale Max",
        description="The magnitude of the wind force exposed to the chain is divided into average (median), minimum and maximum."
                    "\nThe sizes of these three parameters should be determined by default according to the rule of \"WindScaleMax>=WindScale>=WindScaleMin\"."
                    "\nJudging from the traversed CTC files, it seems that there is a relationship of \"WindScale=(WindScaleMin+WindScaleMax)/2\", which may be simply an average value",
        default=1.0,
    )
    #完
    WindScaleWeight: bpy.props.FloatVectorProperty(
        name="Wind Scale Weight",
        description="Represents the wind weight (proportion) of each wind section, and the sum of the three values equals 1.",
        size=3,
        default=(0.2, 0.7, 0.1),
        soft_min=0.0,
        soft_max=1.0,
    )

#获取CTC Header数据
def getCTCHeader(ctcHeaderData,targetObject):
    targetObject.ctc_header.AttributeFlags = ctcHeaderData.AttributeFlags
    targetObject.ctc_header.StepTime = ctcHeaderData.StepTime

    targetObject.ctc_header.GravityScaling = ctcHeaderData.GravityScaling
    targetObject.ctc_header.GlobalDamping = ctcHeaderData.GlobalDamping
    targetObject.ctc_header.GlobalTransForceCoef = ctcHeaderData.GlobalTransForceCoef
    targetObject.ctc_header.SpringScaling = ctcHeaderData.SpringScaling

    targetObject.ctc_header.WindScale = ctcHeaderData.WindScale
    targetObject.ctc_header.WindScaleMin = ctcHeaderData.WindScaleMin
    targetObject.ctc_header.WindScaleMax = ctcHeaderData.WindScaleMax

    targetObject.ctc_header.WindScaleWeight[0] = ctcHeaderData.WindScaleWeight0
    targetObject.ctc_header.WindScaleWeight[1] = ctcHeaderData.WindScaleWeight1
    targetObject.ctc_header.WindScaleWeight[2] = ctcHeaderData.WindScaleWeight2

#设置CTC Header数据
def setCTCHeaderData(ctcHeaderData,targetObject):
    ctcHeaderData.AttributeFlags = int(targetObject.ctc_header.AttributeFlags)
    ctcHeaderData.StepTime = float(targetObject.ctc_header.StepTime)

    ctcHeaderData.GravityScaling = float(targetObject.ctc_header.GravityScaling)
    ctcHeaderData.GlobalDamping = float(targetObject.ctc_header.GlobalDamping)
    ctcHeaderData.GlobalTransForceCoef = float(targetObject.ctc_header.GlobalTransForceCoef)
    ctcHeaderData.SpringScaling = float(targetObject.ctc_header.SpringScaling)

    ctcHeaderData.WindScale = float(targetObject.ctc_header.WindScale)
    ctcHeaderData.WindScaleMin = float(targetObject.ctc_header.WindScaleMin)
    ctcHeaderData.WindScaleMax = float(targetObject.ctc_header.WindScaleMax)

    ctcHeaderData.WindScaleWeight0 = float(targetObject.ctc_header.WindScaleWeight[0])
    ctcHeaderData.WindScaleWeight1 = float(targetObject.ctc_header.WindScaleWeight[1])
    ctcHeaderData.WindScaleWeight2 = float(targetObject.ctc_header.WindScaleWeight[2])


#对应CTC Settings空物体的自定义属性
class CTCSettingsPG(bpy.types.PropertyGroup):

    #完
    internal_changingFlagValues: BoolProperty(
        name="Change Flag Values",
        description="This value is inaccessible by the user, it is used to determine whether the user changed a value or an update function did so that an infinite loop doesn't happen",
        default=False,
    )
    #完
    CollisionAttrFlagValue: IntProperty(
        name="Collision AttrFlag",
        description="Accounting value of all flags.\nChanging this value will change all flags at the same time",
        default=4,
        update=update_CollisionAttrFlagFromInt
    )
    #完
    CollisionFlags_None: BoolProperty(
        name="CollisionFlags_None",
        description="",
        default=False,
        update=update_IntFromCollisionAttrFlag
    )
    #完
    CollisionSelfEnable: BoolProperty(
        name="CollisionSelfEnable",
        description="Whether the chain is allowed to collide with other chains",
        default=False,
        update=update_IntFromCollisionAttrFlag
    )
    #完
    CollisionModelEnable: BoolProperty(
        name="CollisionModelEnable",
        description="Whether the chain is allowed to collide with ccl file",
        default=True,
        update=update_IntFromCollisionAttrFlag
    )
    #完
    CollisionVGroundEnable: BoolProperty(
        name="CollisionVGroundEnable",
        description="Whether the chain is allowed to collide with the ground",
        default=False,
        update=update_IntFromCollisionAttrFlag
    )
    #完
    ChainAttrFlagValue: IntProperty(
        name="Chain AttrFlag",
        description="Accounting value of all flags.\nChanging this value will change all flags at the same time",
        default=39,
        update=update_ChainAttrFlagFromInt
    )
    #完
    AngleLimitEnable: BoolProperty(
        name="AngleLimitEnable",
        description="Whether to enable angle limit.\nUsually recommended to enable it, otherwise angle limit will be invalid",
        default=True,
        update=update_IntFromChainAttrFlag
    )
    #完
    AngleLimitRestitutionEnable: BoolProperty(
        name="AngleLimitRestitutionEnable",
        description="Whether to enable angle limit restitution",
        default=True,
        update=update_IntFromChainAttrFlag
    )
    #完
    EndRotConstraintEnable: BoolProperty(
        name="EndRotConstraintEnable",
        description="Whether to enable the rotation of end node (uncertain)",
        default=True,
        update=update_IntFromChainAttrFlag
    )
    #完
    TransAnimationEnable: BoolProperty(
        name="TransAnimationEnable",
        description="Whether to enable trans animation.\nAfter activating, the chain will stagnate in a motion stop posture, but the specific meaning is unclear",
        default=False,
        update=update_IntFromChainAttrFlag
    )
    #完
    AngleFreeEnable: BoolProperty(
        name="AngleFreeEnable",
        description="Whether to enable angle free",
        default=False,
        update=update_IntFromChainAttrFlag
    )
    #完
    StretchBothEnable: BoolProperty(
        name="StretchBothEnable",
        description="Whether to enable stretch (uncertain).\nDepends on the mass and elasticity of the nodes",
        default=True,
        update=update_IntFromChainAttrFlag
    )
    #完
    PartBlendEnable: BoolProperty(
        name="PartBlendEnable",
        description="Whether to enable part blend.\nAfter activating, the chain seems to squeeze towards the center, but the specific meaning is unclear",
        default=False,
        update=update_IntFromChainAttrFlag
    )
    #完
    unknAttrFlag1: IntProperty(
        name="unkn AttrFlag1",
        description="Actually binary. Common values are 0, 1, 17, 32. More testing is needed."
                    "\nTaking 1 for the 1 bits seems to make the chain harder (or recovers faster) than taking 0."
                    "\nTaking 1 for the 2 bits will force the chain to stretch, like a spring",
        default=0,
    )
    #完
    unknAttrFlag2: IntProperty(
        name="unkn AttrFlag2",
        description="Actually binary, Usually the value is 0, rarely the value is 1",
        default=0,
    )
    #完
    ColAttribute: IntProperty(
        name="Collider Attribute",
        description="Usually the value is -1",
        default=-1,
    )
    #完
    ColGroup: IntProperty(
        name="Collider Group",
        description="Usually the value is 1",
        default=1,
    )
    #完
    ColType: IntProperty(
        name="Collider Type",
        description="Usually the value is 1",
        default=1,
    )
    #完
    Gravity: FloatVectorProperty(
        name="Gravity",
        description="Usually only need to change the Y axis gravity."
                    "\nWhen the value is negative, the direction of gravity reverses.When the value is 0, there is no gravity."
                    "\nGravityScaling with the Header part can be viewed as a product, so when both values are negative, the actual direction of gravity is still downward",
        default=(0.0, -980.0, 0.0),
        subtype="XYZ"
    )
    #完
    Damping: FloatProperty(
        name="Damping",
        description="The greater the damping, the greater the resistance, and the slower and more difficult the movement of the chain."
                    "\nThe smaller the damping, the smaller the resistance, and the faster and more flexible the movement of the chain."
                    "\nNormally the damping is 0 or 0.1, shouldn't be set to too high."
                    "\nA negative value will cause the chain to gain additional energy and move automatically",
        default=0.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    #完
    TransForceCoef: FloatProperty(
        name="TransForce Coef",
        description="If \"Global TransForce Coef\" is 1, it usually should be set to a value less than 1 here."
                    "\nWhen the value is 1, the trans force is equal to the acting force. This is the usual value."
                    "\nWhen the value is greater than 1, the trans force will be greater than the acting force. And the higher the value, the more intense the chain moves."
                    "\nWhen the value is less than 1, the trans force will be less than the acting force. And the smaller the value, the weaker the chain moves."
                    "\nWhen the value is negative, the trans force and acting force will reverse, causing the chain that was originally moving backward to move forward",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    #完
    SpringCoef: FloatProperty(
        name="Spring Coef",
        description="If \"SpringScaling\" is 1, it usually should be set to a value less than 1 here, even less than 0.1."
                    "\nThe greater the value, the harder the chain and the less the deformation."
                    "\nThe smaller the value, the softer the chain and the greater the deformation."
                    "\nSetting it to a negative value is not recommended, which will lead to some unstable physical behavior",
        default=0.01,
        soft_min=0.0,
        soft_max=1.0,
    )
    #完
    LimitForce: FloatProperty(
        name="Limit Force",
        description="Usually the value is 100",
        default=100.0,
    )
    #完
    FrictionCoef: FloatProperty(
        name="Friction Coef",
        description="Usually the value is 0",
        default=0.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    #完
    ReflectCoef: FloatProperty(
        name="Reflect Coef",
        description="Usually the value is 0.1",
        default=0.1,
        soft_min=0.0,
        soft_max=1.0,
    )
    #完
    WindRate: FloatProperty(
        name="Wind Rate",
        description="",
        default=0.1,
        soft_min=0.0,
        soft_max=1.0,
    )
    #完
    WindLimit: IntProperty(
        name="Wind Limit",
        description="There is a hidden variable in memory called \"UseWindLimit\"."
                    "\nWhen the value here is a negative integer, UseWindLimit = 50."
                    "\nWhen the value here is a positive integer, UseWindLimit = WindLimit."
                    "\nOnly seen taking 10 in a few ctc files, so you can just default to -1",
        default=-1,
    )

def getctcSettings(ctcSettingsData, targetObject):
    targetObject.ctc_settings.CollisionAttrFlagValue = ctcSettingsData.CollisionAttrFlag.asInt32
    targetObject.ctc_settings.ChainAttrFlagValue = ctcSettingsData.ChainAttrFlag.asInt32
    targetObject.ctc_settings.unknAttrFlag1 = ctcSettingsData.unknAttrFlag1
    targetObject.ctc_settings.unknAttrFlag2 = ctcSettingsData.unknAttrFlag2

    targetObject.ctc_settings.ColAttribute = ctcSettingsData.ColAttribute
    targetObject.ctc_settings.ColGroup = ctcSettingsData.ColGroup
    targetObject.ctc_settings.ColType = ctcSettingsData.ColType

    targetObject.ctc_settings.Gravity[0] = ctcSettingsData.xGravity
    targetObject.ctc_settings.Gravity[1] = ctcSettingsData.yGravity
    targetObject.ctc_settings.Gravity[2] = ctcSettingsData.zGravity

    targetObject.ctc_settings.Damping = ctcSettingsData.Damping
    targetObject.ctc_settings.TransForceCoef = ctcSettingsData.TransForceCoef
    targetObject.ctc_settings.SpringCoef = ctcSettingsData.SpringCoef

    targetObject.ctc_settings.LimitForce = ctcSettingsData.LimitForce
    targetObject.ctc_settings.FrictionCoef = ctcSettingsData.FrictionCoef
    targetObject.ctc_settings.ReflectCoef = ctcSettingsData.ReflectCoef

    targetObject.ctc_settings.WindRate = ctcSettingsData.WindRate
    targetObject.ctc_settings.WindLimit = ctcSettingsData.WindLimit


def setctcSettingsData(ctcSettingsData,targetObject):
    ctcSettingsData.CollisionAttrFlag.asInt32 = targetObject.ctc_settings.CollisionAttrFlagValue
    ctcSettingsData.ChainAttrFlag.asInt32 = targetObject.ctc_settings.ChainAttrFlagValue
    ctcSettingsData.unknAttrFlag1 = targetObject.ctc_settings.unknAttrFlag1
    ctcSettingsData.unknAttrFlag2 = targetObject.ctc_settings.unknAttrFlag2

    ctcSettingsData.ColAttribute = targetObject.ctc_settings.ColAttribute
    ctcSettingsData.ColGroup = targetObject.ctc_settings.ColGroup
    ctcSettingsData.ColType  = targetObject.ctc_settings.ColType


    ctcSettingsData.xGravity = targetObject.ctc_settings.Gravity[0]
    ctcSettingsData.yGravity = targetObject.ctc_settings.Gravity[1]
    ctcSettingsData.zGravity = targetObject.ctc_settings.Gravity[2]

    ctcSettingsData.Damping = targetObject.ctc_settings.Damping
    ctcSettingsData.TransForceCoef = targetObject.ctc_settings.TransForceCoef
    ctcSettingsData.SpringCoef = targetObject.ctc_settings.SpringCoef

    ctcSettingsData.LimitForce = targetObject.ctc_settings.LimitForce
    ctcSettingsData.FrictionCoef = targetObject.ctc_settings.FrictionCoef
    ctcSettingsData.ReflectCoef = targetObject.ctc_settings.ReflectCoef

    ctcSettingsData.WindRate = targetObject.ctc_settings.WindRate
    ctcSettingsData.WindLimit = targetObject.ctc_settings.WindLimit


#对应CTC Node空物体的自定义属性
class CTCNodePG(bpy.types.PropertyGroup):
    #完
    unknByte1: bpy.props.IntProperty(
        name="unkn Byte1",
        description="Unknown flag, which may actually be binary, default to 0",
        default=0,
    )
    #完
    unknByte2: bpy.props.IntProperty(
        name="unkn Byte2",
        description="Unknown flag, which may actually be binary or boolean.\nTaking 1 may make the node more compact than taking 0 (uncertain).\nThe default is 0",
        default=0,
    )
    #完
    AngleMode: bpy.props.EnumProperty(
        name="Angle Mode",
        description="",
        items=[("0", "AngleMode_Free", "Node will rotate in any direction"),
               ("1", "AngleMode_LimitCone", "Rotation of node will be limited to a cone"),
               ("2", "AngleMode_LimitHinge", "Rotation of node will be limited to rotation only along the z-axis"),
               ("3", "AngleMode_LimitOval", "Rotation of node will be limited to an oval cone"),
               ],
        update=update_AngleLimitMode,
        default=1,
    )
    #完
    CollisionShape: bpy.props.EnumProperty(
        name="Collision Shape",
        description="",
        items=[("0", "CollisionShape_None", "No Collision"),
               ("1", "CollisionShape_Sphere", "The shape of collision is a sphere"),
               ("2", "CollisionShape_Capsule", "The shape of collision is a capsule"),
               ],
        default=1,
    )
    #完
    unknownEnum: bpy.props.EnumProperty(
        name="unkn Enum",
        description="Unknown enumeration, usually 1, but rarely used 0 and 2.\nNormally, you can default to 1",
        items=[("0", "unknEnum_0", ""),
               ("1", "unknEnum_1", ""),
               ("2", "unknEnum_2", ""),
               ],
        default=1,
    )
    #完
    boneColRadius: FloatProperty(
        name="Collision Radius",
        description="",
        default=0.0,
        step=10,
        soft_min=0.0,
        update=update_NodeRadius,
    )
    #完
    AngleLimitRadius: FloatProperty(
        name="Angle Limit Radius",
        description="The amount the node is allowed to rotate from it's angle limit direction."
                    "\nIt is actually in radian, representing the top angle of a cone."
                    "\nThe bottom radius of the cone is used here to represent the top angle, which is incorrect but sufficient to represent the actual size",
        default=math.pi/4,
        step=100,
        soft_min=0.0,
        soft_max=180.0,
        subtype="ANGLE",
        update=update_AngleLimitRad,
    )
    #完
    WidthRate: FloatProperty(
        name="Width Rate",
        description="Rate of width to length of oval at the bottom of cone."
                    "\nEffective only when Angle Mode is Oval."
                    "\nWhen the value is 0, Oval has the same effect as Hinge",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
        update=update_AngleLimitMode,
    )
    #完
    Mass: FloatProperty(
        name="Mass",
        description="Most ctc files default to 1, a few will have values greater than 1 or even around 10, and some will have values less than 1.\nIt is not clear how this parameter works",
        default=1.0,
        soft_min=0.0,
    )
    #完
    ElasticCoef: FloatProperty(
        name="Elastic Coef",
        description="Note that the elastic coef here is different from the spring coef of chain."
                    "\nThe smaller the elastic coef, the easier the node is to be stretched."
                    "\nThe larger the elastic coef, the more likely the node will be to maintain its original length."
                    "\nChanging this value is not recommended，usually 1, which means that the node always maintains its original length",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
    )

def getCTCNode(ctcNodeData,targetObject):

    targetObject.ctc_node.unknByte1 = ctcNodeData.unknByte1
    targetObject.ctc_node.unknByte2 = ctcNodeData.unknByte2
    targetObject.ctc_node.AngleMode = str(ctcNodeData.AngleMode)
    targetObject.ctc_node.CollisionShape = str(ctcNodeData.CollisionShape)
    targetObject.ctc_node.unknownEnum = str(ctcNodeData.unknownEnum)

    targetObject.ctc_node.boneColRadius = ctcNodeData.boneColRadius
    targetObject.ctc_node.AngleLimitRadius = ctcNodeData.AngleLimitRadius
    targetObject.ctc_node.WidthRate = ctcNodeData.WidthRate
    targetObject.ctc_node.Mass = ctcNodeData.Mass
    targetObject.ctc_node.ElasticCoef = ctcNodeData.ElasticCoef

def setCTCNodeData(ctcNodeData,targetObject):

    ctcNodeData.unknByte1 = targetObject.ctc_node.unknByte1
    ctcNodeData.unknByte2 = targetObject.ctc_node.unknByte2
    ctcNodeData.AngleMode = int(targetObject.ctc_node.AngleMode)
    ctcNodeData.CollisionShape = int(targetObject.ctc_node.CollisionShape)
    ctcNodeData.unknownEnum = int(targetObject.ctc_node.unknownEnum)

    ctcNodeData.boneColRadius = targetObject.ctc_node.boneColRadius
    ctcNodeData.AngleLimitRadius = targetObject.ctc_node.AngleLimitRadius
    ctcNodeData.WidthRate = targetObject.ctc_node.WidthRate
    ctcNodeData.Mass = targetObject.ctc_node.Mass
    ctcNodeData.ElasticCoef = targetObject.ctc_node.ElasticCoef

    if targetObject.parent.get("TYPE", None) == "CTC_CHAIN":
        ctcNodeData.isParent = 1
    else:
        ctcNodeData.isParent = 0

    for child in targetObject.children:
        if child.get("TYPE", None) == "CTC_NODE_FRAME":
            frame = child
    frame_matrix_normalized = frame.matrix_local.normalized()
    ctcNodeData.row1_0 = round(frame_matrix_normalized[0][0],6)
    ctcNodeData.row1_1 = round(frame_matrix_normalized[0][1],6)
    ctcNodeData.row1_2 = round(frame_matrix_normalized[0][2],6)
    ctcNodeData.row1_3 = round(frame_matrix_normalized[0][3],6)

    ctcNodeData.row2_0 = round(frame_matrix_normalized[1][0],6)
    ctcNodeData.row2_1 = round(frame_matrix_normalized[1][1],6)
    ctcNodeData.row2_2 = round(frame_matrix_normalized[1][2],6)
    ctcNodeData.row2_3 = round(frame_matrix_normalized[1][3],6)

    ctcNodeData.row3_0 = round(frame_matrix_normalized[2][0],6)
    ctcNodeData.row3_1 = round(frame_matrix_normalized[2][1],6)
    ctcNodeData.row3_2 = round(frame_matrix_normalized[2][2],6)
    ctcNodeData.row3_3 = round(frame_matrix_normalized[2][3],6)

    ctcNodeData.row4_0 = round(frame_matrix_normalized[3][0],6)
    ctcNodeData.row4_1 = round(frame_matrix_normalized[3][1],6)
    ctcNodeData.row4_2 = round(frame_matrix_normalized[3][2],6)
    ctcNodeData.row4_3 = round(frame_matrix_normalized[3][3],6)


    boneName = targetObject.constraints["BoneName"].subtarget
    boneID = int(boneName.split("_")[-1])
    ctcNodeData.boneFunctionID = boneID



def update_CollisionOffset(self, context):
    obj = self.id_data
    if obj.get("TYPE",None) != "CCL_CAPSULE":
        obj.location = 0.01*obj.ccl_collision.StartColOffset# * 100
    else:
        for child in obj.children:
            if child.get("TYPE",None) == "CCL_CAPSULE_START":
                child.location = 0.01*obj.ccl_collision.StartColOffset# * 100

def update_EndCollisionOffset(self, context):
    obj = self.id_data
    if obj.get("TYPE",None) != "CCL_CAPSULE" and obj.get("TYPE",None) != "CCL_SPHERE":
        obj.location = 0.01*obj.ccl_collision.EndColOffset# * 100
    else:
        for child in obj.children:
            if child.get("TYPE",None) == "CCL_CAPSULE_END":
                child.location = 0.01*obj.ccl_collision.EndColOffset# * 100

def update_CollisionRadius(self, context):
    obj = self.id_data
    if type(obj).__name__ == "Object":  # Check if it's an object to prevent issues with clipboard
        if obj.get("TYPE", None) != "CCL_CAPSULE":
            obj.scale = [0.01*obj.ccl_collision.ColRadius] * 3
        else:
            for child in obj.children:
                if child.get("TYPE", None) == "CCL_CAPSULE_START" or child.get("TYPE", None) == "CCL_CAPSULE_END":
                        child.scale = [0.01*obj.ccl_collision.ColRadius] * 3


class CCLPG(bpy.types.PropertyGroup):
    #完
    StartColOffset: FloatVectorProperty(
        name="Head Offset",
        description="Set position of the head collision object",
        step=10,
        subtype="XYZ",
        update=update_CollisionOffset
    )
    #完
    EndColOffset: FloatVectorProperty(
        name="Tail Offset",
        description="Set position of the tail collision object",
        step=10,
        subtype="XYZ",
        update=update_EndCollisionOffset
    )
    #完
    ColRadius: FloatProperty(
        name="Collision Radius",
        description="",
        default=0.00,
        step=10,
        soft_min=0.00,
        update=update_CollisionRadius,
    )
    # ColRadius: FloatProperty(
    #     name="Collision Radius",
    #     description="Radius",
    #     default=0.00,
    #     step=.1,
    #     soft_min=0.00,
    #     update=update_CollisionRadius,
    # )

def getCCLCollision(CCLCollisionData,targetObject):
    targetObject.ccl_collision.ColRadius = CCLCollisionData.ColRadius
    targetObject.ccl_collision.StartColOffset[0] = CCLCollisionData.startPosX
    targetObject.ccl_collision.StartColOffset[1] = CCLCollisionData.startPosY
    targetObject.ccl_collision.StartColOffset[2] = CCLCollisionData.startPosZ
    targetObject.ccl_collision.EndColOffset[0] = CCLCollisionData.endPosX
    targetObject.ccl_collision.EndColOffset[1] = CCLCollisionData.endPosY
    targetObject.ccl_collision.EndColOffset[2] = CCLCollisionData.endPosZ

def setCCLCollisionData(CCLCollisionData,targetObject):
    CCLCollisionData.ColRadius = 100*targetObject.scale[0]

    CCLCollisionData.startPosX = 100*targetObject.location[0]
    CCLCollisionData.startPosY = 100*targetObject.location[1]
    CCLCollisionData.startPosZ = 100*targetObject.location[2]

    CCLCollisionData.endPosX = 100*targetObject.ccl_collision.EndColOffset[0]
    CCLCollisionData.endPosY = 100*targetObject.ccl_collision.EndColOffset[1]
    CCLCollisionData.endPosZ = 100*targetObject.ccl_collision.EndColOffset[2]

    if targetObject.get("TYPE", None) != "CCL_CAPSULE":
        boneName = targetObject.constraints["BoneName"].subtarget
        boneID = int(boneName.split("_")[-1])
        CCLCollisionData.startboneID = boneID
        CCLCollisionData.endboneID = boneID
        CCLCollisionData.ColShape = 0
        targetObject.ccl_collision.StartColOffset = 100*targetObject.location
        targetObject.ccl_collision.ColRadius = 100*targetObject.scale[0]
    else:
        CCLCollisionData.ColShape = 1
        startCapsule = None
        endCapsule = None
        for child in targetObject.children:
            if child.get("TYPE", None) == "CCL_CAPSULE_START":
                startCapsule = child
            elif child.get("TYPE", None) == "CCL_CAPSULE_END":
                endCapsule = child

        if startCapsule != None:
            CCLCollisionData.ColRadius = 100*startCapsule.scale[0]
            boneName = startCapsule.constraints["BoneName"].subtarget
            boneID = int(boneName.split("_")[-1])
            CCLCollisionData.startboneID = boneID

            CCLCollisionData.startPosX = 100*startCapsule.location[0]
            CCLCollisionData.startPosY = 100*startCapsule.location[1]
            CCLCollisionData.startPosZ = 100*startCapsule.location[2]

            targetObject.ccl_collision.StartColOffset = 100*startCapsule.location
            targetObject.ccl_collision.ColRadius = 100*startCapsule.scale[0]
        if endCapsule != None:
            boneName = endCapsule.constraints["BoneName"].subtarget
            boneID = int(boneName.split("_")[-1])
            CCLCollisionData.endboneID = boneID

            CCLCollisionData.endPosX = 100*endCapsule.location[0]
            CCLCollisionData.endPosY = 100*endCapsule.location[1]
            CCLCollisionData.endPosZ = 100*endCapsule.location[2]

            targetObject.ccl_collision.EndColOffset = 100*endCapsule.location
        else:
            CCLCollisionData.endPosX = 0.0
            CCLCollisionData.endPosY = 0.0
            CCLCollisionData.endPosZ = 0.0
            CCLCollisionData.endboneID = CCLCollisionData.startboneID



class CTCClipboardPG(bpy.types.PropertyGroup):
    ctc_type: StringProperty(default="NONE", options={'HIDDEN'})
    ctc_type_name: StringProperty(default="None", options={'HIDDEN'})
    ctc_header : PointerProperty(type=CTCHeaderPG)
    ctc_settings : PointerProperty(type=CTCSettingsPG)
    ctc_node : PointerProperty(type=CTCNodePG)
    ccl_collision : PointerProperty(type=CCLPG)
    frameOrientation: FloatVectorProperty(
        name = "Frame Orientation",
        size = 3,
        subtype = "XYZ"
        )



