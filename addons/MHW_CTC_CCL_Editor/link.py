import bpy
import webbrowser

class BilibiliWebsite(bpy.types.Operator):
    bl_idname = "ctc.bilibili_website"
    bl_label = "Bilibili"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        webbrowser.open("https://space.bilibili.com/84161516?spm_id_from=333.1007.0.0")
        return {'FINISHED'}


class QQWebsite(bpy.types.Operator):
    bl_idname = "ctc.qq_website"
    bl_label = "QQGroup"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        webbrowser.open("https://qm.qq.com/q/iABxIIl3gs")
        return {'FINISHED'}


class CaimoguWebsite(bpy.types.Operator):
    bl_idname = "ctc.caimogu_website"
    bl_label = "Caimogu"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        webbrowser.open("https://www.caimogu.cc/user/183747.html")
        return {'FINISHED'}

class GithubWebsite(bpy.types.Operator):
    bl_idname = "ctc.github_website"
    bl_label = "Github"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        webbrowser.open("https://github.com/chikichikibangbang/MHW_CTC_CCL_Editor")
        return {'FINISHED'}