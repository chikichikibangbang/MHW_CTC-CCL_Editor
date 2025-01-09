![MHWCTCCCLEditorTitle](https://github.com/user-attachments/assets/4254e640-cc60-4c0b-ab03-f2e59975712e)

This addon allows for importing, editing and exporting **ctc** & **ccl** files in **Monster Hunter World**.

This addon is a modified version based on NSACloud's RE Chain Editor.  

![Blender Preview1](https://github.com/user-attachments/assets/b8656635-cb54-4d55-b921-db5ae2be02ab)
![Blender Preview2](https://github.com/user-attachments/assets/20d699cf-ee8e-49ac-9231-7a6a069cdf85)

## Features
 - Allows for importing, editing and exporting MHW ctc & ccl files.
 - Can create new ctc & ccl files entirely within Blender.
 - Presets of chain configurations can be saved and shared.
 - TO DO
     - 添加更多预设
     - 添加按预设碰撞体创建CCL对象的功能
     - 修复存在ctc对象时无法成功导出mod3模型的问题

## Change Log

### V1 - 1/9/2025

* Second test release.
* Complete Chinese translation.
* Fixed an issue where addon installation failed due to direct download of source code.
* Fixed the issue of automatic update module errors.
 
### V1 - 1/7/2025

* First test release.

## Requirements
* [Blender 2.93 or higher](https://www.blender.org/download/)
* [Easier Mod3 Importer Exporter](https://github.com/chikichikibangbang/Easier_Mod3_Importer_Exporter)

## Installation
Download the addon by clicking Code > Download Zip.

In Blender, go to Edit > Preferences > Addons, then click "Install" in the top right.

Navigate to the downloaded zip file for this addon and click "Install Addon". The addon should then be usable.

To update this addon, navigate to Preferences > Add-ons > MHW CTC&CCL Editor and press the "Check for update" button.

## Usage Guide

To be added.

**TL;DR Usage Guide**

1. Import a mod3 model and add bones to be used as physics bones to the armature.
2. (Optional) Press "Rename&Transfer Bones" to rename and convert bones to mod3 format.
3. Create a ctc header, then switch to pose mode, select the start bone of a chain and press "Create Chain From Bone" for each chain. 
4. (Optional) Add ccl collisions to bones by selecting one or two bones and pressing "Create Collision From Bone".
5. Configure ctc & ccl objects in the Object properties tab, or apply presets.
6. Adjust the ctc node XYZ angle limits if necessary.
7. Export from File > Export > CTC & CCL

 ## Credits
[Monster Hunter Modding Discord](https://discord.gg/gJwMdhK)
- [NSACloud](https://github.com/NSACloud) - Perfect RE Chain Editor! 
- [AsteriskAmpersand](https://github.com/AsteriskAmpersand) - Original MHW CTC Editor
- [CG Cookie](https://github.com/CGCookie) - Addon updater module
- [xzhuah](https://github.com/xzhuah) - BlenderAddonPackageTool

 ## 一些中文内容
 * B站id：不太亮的诸葛亮
 * 怪猎mod作者交流群：640945651
 
