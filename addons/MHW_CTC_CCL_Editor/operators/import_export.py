import bpy
import os
from bpy_extras.io_utils import ExportHelper,ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty,PointerProperty
from bpy.types import Operator, OperatorFileListElement,AddonPreferences

from MHW_CTC_CCL_Editor.addons.MHW_CTC_CCL_Editor.operators.ctc_function import importCTCFile, exportCTCFile, importCCLFile, exportCCLFile


class ImportMHWCTC(bpy.types.Operator, ImportHelper):
    bl_idname = "ctc.import_mhw_ctc"
    bl_label = "Import MHW CTC"
    bl_description = "Import MHW CTC Files.\nNOTE: Before importing ctc, make sure that at least one mod3 armature exists in the current scene"
    bl_options = {'PRESET', "REGISTER", "UNDO"}
    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )
    directory: StringProperty(
        subtype='DIR_PATH',
    )
    loadccl: BoolProperty(
        name="Load CCL File",
        description="When importing ctc file, also import ccl file with the same file name under current path",
        default=True)
    filename_ext = ".ctc"
    filter_glob: StringProperty(default="*.ctc", options={'HIDDEN'})
    targetArmature: StringProperty(
        name="",
        description="The armature to attach ctc objects to.\nNOTE: If some bones that are used by the ctc file are missing on the armature, corresponding ctc nodes using those bones won't be imported",
        default="")
    mergeChain: StringProperty(
        name="",
        description="Merges the imported ctc objects with an existing ctc collection",
        default="")

    def invoke(self, context, event):
        armature = None
        if bpy.data.armatures.get(self.targetArmature, None) == None:
            try:  # Pick selected armature if one is selected
                if armature == None and bpy.context.active_object != None and bpy.context.active_object.type == "ARMATURE":
                    armature = bpy.context.active_object
            except:
                pass
            if armature == None:
                for obj in bpy.context.scene.objects:
                    if obj.type == "ARMATURE":
                        armature = obj

            if armature != None:
                self.targetArmature = armature.data.name

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "loadccl")
        layout.label(text="Target Armature:")
        layout.prop_search(self, "targetArmature", bpy.data, "armatures")
        layout.label(text="Merge With CTC Collection:")
        layout.prop_search(self, "mergeChain", bpy.data, "collections", icon="COLLECTION_COLOR_02")


    def execute(self, context):
        options = {"targetArmature": self.targetArmature, "mergeChain": self.mergeChain, "loadccl": self.loadccl}
        success = importCTCFile(self.filepath, options)
        if success:
            self.report({"INFO"}, "Successfully imported MHW CTC.")
            return {"FINISHED"}
        else:
            self.report({"INFO"}, "Failed to import MHW CTC. Make sure the corresponding mod3 file is imported.")
            return {"CANCELLED"}



class ExportMHWCTC(bpy.types.Operator, ExportHelper):
    bl_idname = "ctc.export_mhw_ctc"
    bl_label = "Export MHW CTC"
    bl_description = "Export MHW CTC Files"
    bl_options = {'PRESET', "REGISTER", "UNDO"}
    filename_ext = ".ctc"
    targetCollection: StringProperty(
        name="",
        description="Set the ctc collection to be exported",
        default="")
    exportccl: BoolProperty(
        name="Export CCL File",
        description="When exporting ctc file, also export ccl file with the same file name into current path",
        default=True)
    filter_glob: StringProperty(default="*.ctc*", options={'HIDDEN'})

    def invoke(self, context, event):
        if bpy.data.collections.get(self.targetCollection, None) == None:
            if bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection):
                self.targetCollection = bpy.context.scene.ctc_toolpanel.ctcCollection
                if ".ctc" in self.targetCollection:
                    self.filepath = self.targetCollection.split(".ctc")[0] + ".ctc"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "exportccl")
        layout.label(text="CTC Collection:")
        layout.prop_search(self, "targetCollection", bpy.data, "collections", icon="COLLECTION_COLOR_02")

    def execute(self, context):
        options = {"targetCollection": self.targetCollection, "exportccl": self.exportccl}
        success = exportCTCFile(self.filepath, options)
        if success:
            self.report({"INFO"}, "Successfully exported MHW CTC.")
        else:
            self.report({"INFO"}, "MHW CTC export failed. See Window > Toggle System Console for details.")
        return {"FINISHED"}


class ImportMHWCCL(bpy.types.Operator, ImportHelper):
    bl_idname = "ctc.import_mhw_ccl"
    bl_label = "Import MHW CCL"
    bl_description = "Import MHW CCL Files.\nNOTE: Before importing ccl, make sure that at least one mod3 armature and ctc collection exists in the current scene, otherwise the button cannot be triggered"
    bl_options = {'PRESET', "REGISTER", "UNDO"}
    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )
    directory: StringProperty(
        subtype='DIR_PATH',
    )
    filename_ext = ".ccl"
    filter_glob: StringProperty(default="*.ccl", options={'HIDDEN'})
    targetArmature: StringProperty(
        name="",
        description="The armature to attach ccl objects to.\nNOTE: If some bones that are used by the ccl file are missing on the armature, corresponding ccl nodes using those bones won't be imported",
        default="")
    mergeChain: StringProperty(
        name="",
        description="Merges the imported ccl objects with an existing ccl collection",
        default="")

    @classmethod
    def poll(self, context):
        return bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection, None) is not None

    def invoke(self, context, event):
        armature = None
        if bpy.data.armatures.get(self.targetArmature, None) == None:
            try:  # Pick selected armature if one is selected
                if armature == None and bpy.context.active_object != None and bpy.context.active_object.type == "ARMATURE":
                    armature = bpy.context.active_object
            except:
                pass
            if armature == None:
                for obj in bpy.context.scene.objects:
                    if obj.type == "ARMATURE":
                        armature = obj

            if armature != None:
                self.targetArmature = armature.data.name

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Target Armature:")
        layout.prop_search(self, "targetArmature", bpy.data, "armatures")
        layout.label(text="Merge With CTC Collection:")
        layout.prop_search(self, "mergeChain", bpy.data, "collections", icon="COLLECTION_COLOR_02")

    def execute(self, context):
        options = {"targetArmature": self.targetArmature, "mergeChain": self.mergeChain}
        success = importCCLFile(self.filepath, options)
        if success:
            self.report({"INFO"}, "Successfully imported MHW CCL.")
            return {"FINISHED"}
        else:
            self.report({"INFO"}, "Failed to import MHW CCL. Make sure the corresponding mod3 file and ctc file are both imported.")
            return {"CANCELLED"}


class ExportMHWCCL(bpy.types.Operator, ExportHelper):
    bl_idname = "ctc.export_mhw_ccl"
    bl_label = "Export MHW CCL"
    bl_description = "Export MHW CCL Files"
    bl_options = {'PRESET', "REGISTER", "UNDO"}
    filename_ext = ".ccl"
    targetCollection: StringProperty(
        name="",
        description="Set the ccl collection to be exported",
        default="")
    filter_glob: StringProperty(default="*.ccl*", options={'HIDDEN'})

    def invoke(self, context, event):
        if bpy.data.collections.get(self.targetCollection, None) == None:
            if bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection):
                self.targetCollection = bpy.context.scene.ctc_toolpanel.ctcCollection
                if ".ctc" in self.targetCollection:
                    self.filepath = self.targetCollection.split(".ctc")[0] + ".ccl"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="CTC Collection:")
        layout.prop_search(self, "targetCollection", bpy.data, "collections", icon="COLLECTION_COLOR_02")

    def execute(self, context):
        options = {"targetCollection": self.targetCollection}
        success = exportCCLFile(self.filepath, options)
        if success:
            self.report({"INFO"}, "Successfully exported MHW CCL.")
        else:
            self.report({"INFO"}, "MHW CCL export failed. See Window > Toggle System Console for details.")
        return {"FINISHED"}



