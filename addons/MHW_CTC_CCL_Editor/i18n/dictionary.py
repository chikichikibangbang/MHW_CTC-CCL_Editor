from ....common.i18n.dictionary import preprocess_dictionary

dictionary = {
    "zh_CN": {
        # ("*", "Example Addon Side Bar Panel"): "示例插件面板",
        # ("*", "Example Functions"): "示例功能",
        # ("*", "ExampleAddon"): "示例插件",
        # ("*", "Resource Folder"): "资源文件夹",
        # ("*", "Int Config"): "整数参数",
        # # This is not a standard way to define a translation, but it is still supported with preprocess_dictionary.
        # "Boolean Config": "布尔参数",
        # ("*", "Add-on Preferences View"): "插件设置面板",
        # ("Operator", "ExampleOperator"): "示例操作",

        #
        # #update
        # ("*", "Updater Settings"): "更新设置",
        # ("*", "Auto-check for Update"): "自动检查更新",
        # ("*", "If enabled, auto-check for updates using an interval"): "如果启用，按照一定时间间隔自动检查更新",
        # ("*", "Months"): "月",
        # ("*", "Number of months between checking for updates"): "每次检查更新之间的月数",
        # ("*", "Days"): "日",
        # ("*", "Number of days between checking for updates"): "每次检查更新之间的天数",
        # ("*", "Hours"): "小时",
        # ("*", "Number of hours between checking for updates"): "每次检查更新之间的小时数",
        # ("*", "Minutes"): "分钟",
        # ("*", "Number of minutes between checking for updates"): "每次检查更新之间的分钟数",
        #
        # ("*", "Interval between checks"): "检查时间间隔",
        #
        # ("*", "Updater module error"): "更新模块错误",


        #AddonOperators
        ("Operator", "Create CTC Header"): "创建CTC标头",
        ("*", "Create a ctc header object.\nNote that all ctc objects must be parented to this.\nA new ctc collection will be created"): "创建一个ctc标头对象.\n注意所有ctc对象必须以此为父级.\n同时会创建一个新的ctc集合",
        ("*", "CTC Name"): "CTC名称",
        ("*", "The name of the newly created ctc collection.\nUse the same name as the ctc file"): "新创建ctc集合的名称.\n该名称会同时作为ctc文件的名称",
        ("*", "Created new CTC collection."): "已创建新的CTC集合.",
        ("*", "Invalid CTC collection name."): "无效的CTC集合名称",

        ("Operator", "Switch to Pose Mode"): "转换至姿态模式",
        ("*", "Switch to Pose Mode to add new ctc chains and ccl collisions"): "转换至姿态模式，以添加新的ctc链组和ccl碰撞",

        ("Operator", "Switch to Object Mode"): "转换至物体模式",
        ("*", "Switch to Object Mode to configure ctc chains and ccl collisions"): "转换至物体模式，以配置ctc链组或ccl碰撞",

        ("Operator", "Create CTC Chain From Bone"): "创建CTC链组",
        ("*", "Create new ctc chain objects starting from the selected bone and ending at the last child bone.\nBones in a chain must be named with bonefunction_xxx.\nNote that a chain cannot be branching"): "创建新的ctc链组对象，该链组以当前选中的骨骼为链首，以最后一个子级骨骼为链尾."
                                                                                                                                                                                                     "\n链组中的骨骼必须以bonefunction_xxx格式命名.\n注意一条链不能含有分支",
        ("*", "Select only the chain start bone."): "请只选中链的头骨.",
        ("*", "A chain must have at least 2 bones."): "一条链必须包含至少2个骨骼.",
        ("*", "Current chain has some bones that are not named with bonefunction_xxx, please check the name of the bones."): "当前链中含有一些名称不符合bonefunction_xxx格式的骨骼，请检查骨骼名称.",
        ("*", "Cannot have branching bones in a chain."): "一条链不能含有分支.",
        ("*", "Created CTC chain from bone."): "已创建新的CTC链组.",
        ("*", "No CTC chain was created because the active CTC collection is not set."): "因为还没有设置当前激活的CTC集合，所以未创建新的CTC链组.",

        ("Operator", "Create CCL Collision From Bone"): "创建CCL碰撞",
        ("*", "Create new ccl collision object from selected bone(s).\nSelect one bone to create a sphere or two bones to create a capsule.\nPlease select bones other than physical bones"): "从选中骨骼创建ccl碰撞对象.\n选中一个骨骼以创建单球体碰撞，选中两个骨骼以创建胶囊碰撞.\n请选择物理骨骼之外的骨骼",
        ("*", "Select one bone to create a sphere or two bones to create a capsule."): "选中一个骨骼以创建单球体碰撞，选中两个骨骼以创建胶囊碰撞.",
        ("*", "Created CCL collision from bone."): "已创建新的CCL碰撞.",
        ("*", "No CCL collision was created because the active CTC collection is not set."): "因为还没有设置当前激活的CTC集合，所以未创建新的CCL碰撞.",

        ("Operator", "Copy"): "复制",
        ("*", "Copy properties from a ctc object"): "复制一个ctc对象的属性",
        ("*", "CTC Header"): "CTC标头",
        ("*", "CTC Chain"): "CTC链组",
        ("*", "CTC Node"): "CTC节点",
        ("*", "Angle Limit Orientation"): "角度限制方向",
        ("*", "A ctc object must be selected."): "必须选中一个ctc对象.",
        ("*", "Copied properties of CTC Header object to clipboard."): "已将CTC标头的属性复制到剪贴板中.",
        ("*", "Copied properties of CTC Chain object to clipboard."): "已将CTC链组的属性复制到剪贴板中.",
        ("*", "Copied properties of CTC Node object to clipboard."): "已将CTC节点的属性复制到剪贴板中.",
        ("*", "Copied properties of Angle Limit Orientation object to clipboard."): "已将角度限制方向的属性复制到剪贴板中.",

        ("Operator", "Paste"): "粘贴",
        ("*", "Paste properties from a ctc object to selected objects.\nThe type of a ctc object must be the same as the object copied from"): "向选中的ctc对象粘贴之前复制的属性.\nctc对象的类型必须和之前复制的对象类型一致",
        ("*", "Pasted properties of CTC Header object from clipboard."): "已从剪贴板粘贴CTC标头的属性.",
        ("*", "Pasted properties of CTC Chain object from clipboard."): "已从剪贴板粘贴CTC链组的属性.",
        ("*", "Pasted properties of CTC Node object from clipboard."): "已从剪贴板粘贴CTC节点的属性.",
        ("*", "Pasted properties of Angle Limit Orientation object from clipboard."): "已从剪贴板粘贴角度限制方向的属性.",
        ("*", "The contents stored in the clipboard can't be applied to the selected object."): "存储在剪贴板中的内容无法应用于所选对象.",


        ("Operator", "Hide Non Nodes"): "隐藏非节点对象",
        ("*", "Hide all objects that aren't ctc nodes to make selecting and configuring them easier."
              "\nPress the \"Unhide All\" button to unhide"): "隐藏所有非ctc节点的对象，以方便选中和配置它们.\n按“全部取消隐藏”按钮以取消隐藏",
        ("*", "Hid all non ctc node objects."): "已隐藏所有非ctc节点的对象.",

        ("Operator", "Hide Non Collisions"): "隐藏非碰撞对象",
        ("*", "Hide all objects that aren't ccl collisions to make selecting and configuring them easier."
              "\nPress the \"Unhide All\" button to unhide"): "隐藏所有非ccl碰撞的对象，以方便选中和配置它们.\n按“全部取消隐藏”按钮以取消隐藏",
        ("*", "Hid all non ccl collision objects."): "已隐藏所有非ccl碰撞的对象.",

        ("Operator", "Hide Non Angle Limits"): "隐藏非角度限制对象",
        ("*", "Hide all objects that aren't angle limits to make selecting and configuring them easier."
              "\nPress the \"Unhide All\" button to unhide"): "隐藏所有非角度限制的对象，以方便选中和配置它们.\n按“全部取消隐藏”按钮以取消隐藏",
        ("*", "Hid all non angle limit objects."): "已隐藏所有非角度限制的对象.",

        ("Operator", "Unhide All"): "全部取消隐藏",
        ("*", "Unhide all objects hidden with above buttons"): "取消隐藏全部被上述按钮隐藏的对象",
        ("*", "Unhid all objects."): "已取消隐藏全部对象.",

        ("Operator", "Align Angle Limit Direction"): "校准角度限制方向",
        ("*", "Aligns angle limit direction with the next node in the chain."
              "\nNote that additional adjustments may be required for the angle limit to work properly."
              "\nYou can select specific ctc chain objects to align"): "将角度限制方向校准为朝向链中的下一个节点.\n请注意，可能需要进行额外调整才能使角度限制正常工作.\n您可以选择特定的ctc链组对象进行校准",
        ("*", "Aligned angle limit directions."): "已校准角度限制方向.",
        ("*", "No chains found in selection or collection."): "在选中或集合中未发现链组对象.",

        ("Operator", "Apply Angle Limit Ramp"): "应用角度限制坡度",
        ("*", "Apply an increasing angle limit radius on each ctc node as it gets further away."
              "\nA ctc chain must be selected. If multiple ctc chains are selected, it will be applied to all of them"): "对链组中的每个ctc节点应用一个逐渐增加的角度限制弧度.\n必须选择一个ctc链组.如果选择了多个ctc链组，那么也将全部应用于它们",
        ("*", "Applied angle limit ramp to selected ctc chains."): "已对选中的ctc链组应用角度限制坡度.",
        ("*", "ctc chains must be selected to apply an angle limit ramp."): "必须选中ctc链组以应用角度限制坡度.",

        ("Operator", "Rename&Transfer Bones"): "重命名并转化骨骼",
        ("*", "Rename and transfer all bones that are a child of the selected bone."
              "\nThe bones cannot be branching.\nSee settings on the right for detailed operation items"): "重命名并转化当前选中骨骼的所有子级骨骼.\n链中的骨骼不能含有分支.\n在右侧设置中查看具体操作项",
        ("*", "Select only the chain start bone."): "请只选中链的头骨.",
        ("*", "A chain must have at least 2 bones."): "一条链必须包含至少2个骨骼.",
        ("*", "Cannot have branching bones in a chain."): "一条链不能含有分支.",
        ("*", "Renamed and Transfered chain bones."): "已重命名并转化链中的骨骼.",
        ("*", "Note: There are some IDs outside 150~200!"): "注意：当前存在超过150~200范围的骨骼ID！",
        # ("*", "number of unused ID (150~200): "): "未使用ID数量(150~200)：",
        ("*", "unused ID (150~200): "): "未使用ID (150~200)：",
        ("*", "Start Bone ID"): "头骨ID",
        ("*", "Current chain will be sorted backwards and renamed with the ID entered"): "当前链将按输入的ID值向后排序并重新命名",

        ("*", "Add Mod3 Bone Properties"): "添加MOD3骨骼属性",
        ("*", "Add mod3 bone properties to normal bones"): "给一般骨骼添加mod3骨骼属性",

        ("*", "Bone Vertical Alignment"): "骨骼竖直校准",
        ("*", "Align bones in a vertical and upward direction"): "将骨骼校准为竖直向上的方向",

        ("Operator", "Transfer Bone Settings"): "转化骨骼设置",
        ("*", "Settings for detailed operation items"): "设置转化骨骼的具体操作项",

        ("Operator", "Set Attribute Flag"): "设置属性标志",
        # ("*", "Set header attribute flag value from a list of known values"): "从已知数值的列表中设置属性标识",

        ("Operator", "Save Selected As Preset"): "保存为预设",
        ("*", "Save selected ctc&ccl object as a preset for easy reuse and sharing."
              "\nPresets can be accessed using the \"Open Preset Folder\" button"): "将选中的ctc或ccl对象保存为预设，以便于重复使用和分享.\n可以使用“打开预设文件夹”按钮访问预设文件",
        ("*", "Saved preset."): "已保存预设.",

        ("Operator", "Open Preset Folder"): "打开预设文件夹",
        ("*", "Open the preset folder in File Explorer"): "在文件资源管理器中打开预设文件夹",

        ("Operator", "Apply CTC Chain Preset"): "应用CTC链组预设",
        ("*", "Apply preset to selected ctc chain objects"): "给选中的ctc链组对象应用预设",
        ("*", "Applied ctc chain preset."): "已应用CTC链组预设.",
        ("*", "Must select a ctc chain in order to apply the preset to it."): "必须选择一个CTC链组对象以应用预设.",

        ("Operator", "Apply CTC Node Preset"): "应用CTC节点预设",
        ("*", "Apply preset to selected ctc node objects.\nNote that frame orientations are not changed by presets"): "给选中的ctc节点对象应用预设.\n注意角度限制方向不会被预设更改",
        ("*", "Applied ctc node preset."): "已应用CTC节点预设.",
        ("*", "Must select a ctc node in order to apply the preset to it."): "必须选择一个CTC节点对象以应用预设.",


        #ctc_function

        ("*", "More than one armature was found in the scene. Select an armature before importing the ctc file."): "当前场景中存在不止一个骨架.请在导入ctc文件之前选择一个骨架.",
        ("*", "No armature in scene. The armature from the mod3 file must be present in order to import the ctc file."): "当前场景中没有骨架.来自mod3模型的骨架必须存在才能导入ctc文件.",
        ("*", "More than one armature was found in the scene. Select an armature before importing the ccl file."): "当前场景中存在不止一个骨架.请在导入ccl文件之前选择一个骨架.",
        ("*", "No armature in scene. The armature from the mod3 file must be present in order to import the ccl file."): "当前场景中没有骨架.来自mod3模型的骨架必须存在才能导入ccl文件.",
        ("*", "Successfully exported MHW CCL."): "成功导出MHW CCL.",

        #import_export

        ("Operator", "Import MHW CTC"): "导入MHW CTC",
        ("*", "Import MHW CTC Files.\nNOTE: Before importing ctc, make sure that at least one mod3 armature exists in the current scene"): "导入MHW CTC文件.\n注意：在导入ctc之前，确保当前场景中存在至少一个mod3模型的骨架",
        ("*", "Load CCL File"): "同时导入CCL文件",
        ("*", "When importing ctc file, also import ccl file with the same file name under current path"): "导入ctc文件时，同时导入当前路径下具有相同文件名的ccl文件",
        ("*", "The armature to attach ctc objects to."
              "\nNOTE: If some bones that are used by the ctc file are missing on the armature, corresponding ctc nodes using those bones won't be imported"): "要附加ctc对象的骨架."
                                                                                                                                                               "\n注意：如果骨架上缺少ctc文件使用的某些骨骼，则不会导入这些骨骼对应的ctc节点",

        ("*", "Merges the imported ctc objects with an existing ctc collection"): "将导入的ctc对象并入现有的ctc集合中",
        ("*", "Target Armature:"): "目标骨架:",
        ("*", "Merge With CTC Collection:"): "并入CTC集合:",
        ("*", "CTC Collection:"): "CTC集合:",

        ("*", "Successfully imported MHW CTC."): "成功导入MHW CTC.",
        ("*", "Failed to import MHW CTC. Make sure the corresponding mod3 file is imported."): "导入MHW CTC失败.确保已导入对应的mod3模型.",

        ("Operator", "Export MHW CTC"): "导出MHW CTC",
        ("*", "Export MHW CTC Files"): "导出MHW CTC文件",
        ("*", "Set the ctc collection to be exported"): "设定要导出的ctc集合",
        ("*", "Export CCL File"): "同时导出CCL文件",
        ("*", "When exporting ctc file, also export ccl file with the same file name into current path"): "导出ctc文件时，同时导出具有相同文件名的ccl文件至当前路径下",
        ("*", "Successfully exported MHW CTC."): "成功导出MHW CTC.",

        ("Operator", "Import MHW CCL"): "导入MHW CCL",
        ("*", "Import MHW CCL Files."
              "\nNOTE: Before importing ccl, make sure that at least one mod3 armature and ctc collection exists in the current scene, otherwise the button cannot be triggered"): "导入MHW CCL文件.\n注意：在导入ccl之前，确保当前场景中存在至少一个mod3模型的骨架，否则该按钮不能触发",
        ("*", "The armature to attach ccl objects to.\n"
              "NOTE: If some bones that are used by the ccl file are missing on the armature, corresponding ccl nodes using those bones won't be imported"): "要附加ccl对象的骨架."
                                                                                                                                                             "\n注意：如果骨架上缺少ccl文件使用的某些骨骼，则不会导入这些骨骼对应的ccl碰撞",
        ("*", "Merges the imported ccl objects with an existing ctc collection"): "将导入的ccl对象并入现有的ctc集合中",

        ("*", "Successfully imported MHW CCL."): "成功导入MHW CCL.",
        ("*", "Failed to import MHW CCL. Make sure the corresponding mod3 file and ctc file are both imported."): "导入MHW CCL失败.确保已导入对应的mod3模型和ctc文件.",

        ("Operator", "Export MHW CCL"): "导出MHW CCL",
        ("*", "Export MHW CCL Files"): "导出MHW CCL文件",
        ("*", "Successfully exported MHW CCL."): "成功导出MHW CCL.",

        #rw_presets

        ("*", "Selected object can not be made into a preset."): "所选对象不能被保存为预设.",
        ("*", "Invalid preset file name."): "无效的预设文件名.",
        ("*", "A ctc object must be selected when saving a preset."): "必须选中一个ctc对象来保存预设.",
        ("*", "Preset type does not match selected object."): "预设类型不匹配所选对象.",
        ("*", "Preset type is not supported."): "预设类型不支持.",


        #AddonPanels
        ("*", "Import & Export"): "导入 & 导出",
        ("Operator", "Import CTC"): "导入 CTC",
        ("Operator", "Export CTC"): "导出 CTC",
        ("Operator", "Import CCL"): "导入 CCL",
        ("Operator", "Export CCL"): "导出 CCL",

        ("*", "CTC & CCL Tools"): "CTC & CCL工具",
        ("*", "Active CTC Collection"): "当前CTC集合",

        ("*", "Create new chains in Pose Mode."): "在姿态模式创建新的链组和碰撞.",
        ("*", "Configure chains in Object Mode."): "在物体模式配置链组和碰撞.",


        ("*", "Clipboard"): "剪贴板",
        ("*", "Copy CTC&CCL Object Properties"): "复制CTC或CCL对象的属性",
        ("*", "Clipboard Contents:"): "剪贴板内容:",



        ("*", "Presets"): "预设",
        ("*", "CTC Chain Preset"): "CTC链组预设",
        ("*", "CTC Node Preset"): "CTC节点预设",

        ("*", "Visibility"): "可见性",
        ("*", "Angle Limit Settings"): "角度限制设置",
        ("*", "Color Settings"): "颜色设置",

        ("*", "Credits"): "贡献者名单",
        ("*", "Modified by:"): "作者:",
        ("*", "Korone"): "诸葛不太亮",
        ("*", "Special thanks:"): "特别感谢:",

        ("Operator", "Bilibili"): "B站",
        ("Operator", "QQGroup"): "QQ群",
        ("Operator", "Caimogu"): "踩蘑菇mod论坛",



        #ctc_properties
        #CTCToolPanelPG
        ("*", "Apply to Child Nodes"): "同时应用到子级节点",
        ("*", "Apply ctc node preset to all nodes that are a child of the selected node"): "将ctc节点预设应用于所选节点的所有子级节点",

        ("*", "Set the collection containing the ctc file to edit."
              "\nHint: ctc collections are orange."
              "\nYou can create a new ctc collection by pressing the \"Create CTC Header\" button."
              "\nThe ccl collision created will also be included in the collection"): "设置包含要编辑的ctc文件的集合."
                                                                                      "\n提示：ctc集合是橙色的."
                                                                                      "\n您可以按“创建CTC标头”按钮创建新的ctc集合."
                                                                                      "\nccl碰撞也将包含在该集合中",

        ("*", "Show Node Names"): "显示节点名称",
        ("*", "Show Node Names in 3D View"): "在3D视图中显示节点名称",

        ("*", "Draw Nodes Through Objects"): "在前面显示节点",
        ("*", "Make all ctc node and frame objects render through any objects in front of them"): "使所有ctc节点和框架对象显示在任意对象前面",

        ("*", "Show Cones"): "显示圆锥体",
        ("*", "Show Angle Limit Cones in 3D View"): "在3D视图中显示角度限制圆锥体",

        ("*", "Draw Cones Through Objects"): "在前面显示圆锥体",
        ("*", "Make all angle limit cones render through any objects in front of them"): "使所有角度限制圆锥体显示在任意对象前面",

        ("*", "Angle Limit Size"): "角度限制大小",
        ("*", "Set the display size of node angle limits"): "设置角度限制坐标轴显示的大小",

        ("*", "Cone Size"): "圆锥体大小",
        ("*", "Set the display size of node angle limit cones"): "设置角度限制圆锥体显示的大小",

        ("*", "Collision Color"): "碰撞体颜色",
        ("*", "Angle Limit Color"): "圆锥体颜色",

        ("*", "Show Relation Lines"): "显示关系线",
        ("*", "Show dotted lines indicating object parents."
              "\nNote that this affects all objects, not just ctc objects"): "显示指示对象父级结构的虚线.\n请注意，这会影响所有对象，而不仅仅是ctc对象",

        ("*", "Hide Last Node Cone"): "隐藏尾节点的圆锥体",
        ("*", "Hide the last ctc node's angle limit cone.\nThis is because the last node is typically unused and has a dummy rotation value"): "隐藏最后一个ctc节点的角度限制圆锥体.\n这是因为最后一个节点通常未使用且具有默认的矩阵值",

        ("*", "Show Collision Names"): "显示碰撞体名称",
        ("*", "Show CCL Collision Names in 3D View"): "在3D视图中显示碰撞体名称",

        ("*", "Draw Collisions Through Objects"): "在前面显示碰撞体",
        ("*", "Make all ccl collision objects render through any objects in front of them"): "使所有ccl碰撞显示在任意对象前面",


        #CTCHeaderPG
        ("*", "CTC Header Settings"): "CTC标头设置",
        ("*", "Note: The header settings here will affect all chains."): "注意：此处的标头设置会影响所有的物理链.",


        ("*", "Attribute Flags"): "属性标志",
        ("*", "Determine certain movement properties of the chain."
              "\nIt is actually a binary, and the maximum bit may be 8 bits from testing."
              "\nThe most common value is 64 (mostly seen on armor), followed by 80 (mostly seen on pendants)."
              "\n80 seems to make the chain move more violently than 64, you can refer to the fluttering pendant."
              "\nThe main difference lies in the fifth and seventh bits of binary, and it is unclear what these bits mean"): "决定物理链的某些运动属性."
                                                                                                                    "\n实际为二进制，经测试最大位可能为8位."
                                                                                                                    "\n最常见的是64（多在防具上看到），其次是80（多在吊坠上看到）."
                                                                                                                    "\n80相比64似乎会使链的运动更为剧烈，可以参考会飘动的吊坠."
                                                                                                                    "\n主要区别在于二进制的第5位和第7位，尚不清楚这些位具体表示的含义",
        ("*", "Set Attribute Flag"): "设定属性标志",
        ("*", "Set header attribute flag value from a list of known values"): "从已知数值的列表中设置属性标识",

        ("*", "Step Time"): "时间步长",
        ("*", "The time interval between each update of the simulation by the physics engine."
              "\nSetting the step time to 0.16666 seconds means that the physics engine updates 60 times per second, which matches a frame rate of 60FPS."
              "\nPlease don't change this value"): "物理引擎每次更新模拟之间的时间间隔.\n将时间步长设置为1/60秒，意味着物理引擎每秒会进行60次更新，这与60FPS的帧率相匹配.\n请不要修改此值",

        ("*", "Gravity Scaling"): "重力比例",
        ("*", "Multiple of the gravity applied to the chain, Usually 1."
              "\nWhen the value is negative, the direction of gravity reverses."
              "\nWhen the value is 0, there is no gravity"): "链受到重力的倍数，通常为1.\n当值为负数时，重力方向会反转.\n当值为0时，则无重力",

        ("*", "Global Damping"): "整体阻尼",
        ("*", "The greater the damping, the greater the resistance, and the slower and more difficult the movement of the chain."
              "\nThe smaller the damping, the smaller the resistance, and the faster and more flexible the movement of the chain."
              "\nNormally the damping is 0 or 0.1, shouldn't be set to too high."
              "\nA negative value will cause the chain to gain additional energy and move automatically"): "阻尼越大，阻力越大，链的运动越缓慢和困难.\n阻尼越小，阻力越小，链的运动越迅速和灵活.\n阻尼通常为0或0.1，不应设为过高的值.\n值为负时，会使链获取额外的能量，从而自动运动",

        ("*", "Global TransForce Coef"): "整体反作用力系数",
        ("*", "When the value is 1, the trans force is equal to the acting force. This is the usual value."
              "\nWhen the value is greater than 1, the trans force will be greater than the acting force. And the higher the value, the more intense the chain moves."
              "\nWhen the value is less than 1, the trans force will be less than the acting force. And the smaller the value, the weaker the chain moves."
              "\nWhen the value is negative, the trans force and acting force will reverse, causing the chain that was originally moving backward to move forward"): "当值为1时，反作用力等于作用力. 这是通常设定的数值."
                     "\n当值大于1时，反作用力会大于作用力. 并且数值越大，链的运动幅度越剧烈."
                     "\n当值小于1时，反作用力会小于作用力. 并且数值越小，链的运动幅度越微弱."
                     "\n当值为负时，反作用力和作用力会反向，会导致原本向后运动的链变为向前运动",

        ("*", "Spring Scaling"): "弹性比例",
        ("*", "Multiple of chain elasticity, Usually 1."
              "\nSetting it to a negative value is not recommended, which will lead to some unstable physical behavior"): "链弹性的倍数，通常为1.\n不建议设为负数，会导致一些不稳定的物理行为",

        ("*", "Wind Scale"): "风力范围平均值",
        ("*", "Wind Scale Min"): "风力范围最小值",
        ("*", "Wind Scale Max"): "风力范围最大值",
        ("*", "The magnitude of the wind force exposed to the chain is divided into average (median), minimum and maximum."
              "\nThe sizes of these three parameters should be determined by default according to the rule of \"WindScaleMax>=WindScale>=WindScaleMin\"."
              "\nJudging from the traversed CTC files, it seems that there is a relationship of \"WindScale=(WindScaleMin+WindScaleMax)/2\", which may be simply an average value"): "风力范围,分为平均值(中间值),最小值和最大值.\n这三个参数的大小应默认按照\"最大值>=平均值>=最小值\"的规则来取值.\n从遍历过的CTC文件来看,似乎有着\"平均值=(最小值+最大值)/2\"的固定关系,可能单纯是平均值",

        ("*", "Wind Scale Weight"): "风力范围权重",
        ("*", "Represents the wind weight (proportion) of each wind section, and the sum of the three values equals 1."): "表示各段风力权重(占比)，三者总和等于1",


        #CTCSettingsPG
        ("*", "CTC Chain Settings"): "CTC链组设置",

        ("*", "Collision AttrFlag Settings"): "碰撞属性标志设置",
        ("*", "Collision AttrFlag"): "碰撞属性标志",
        ("*", "Accounting value of all flags.\nChanging this value will change all flags at the same time"): "所有标志位的合算数值.\n更改此数值将同步更改所有标志位",
        ("*", "CollisionSelfEnable"): "与其他链发生碰撞",
        ("*", "Whether the chain is allowed to collide with other chains"): "是否允许链与其他链发生碰撞",
        ("*", "CollisionModelEnable"): "与ccl发生碰撞",
        ("*", "Whether the chain is allowed to collide with ccl file"): "是否允许链与与ccl文件发生碰撞",
        ("*", "CollisionVGroundEnable"): "与地面发生碰撞",
        ("*", "Whether the chain is allowed to collide with the ground"): "是否允许链与地面发生碰撞",

        ("*", "Chain AttrFlag Settings"): "链属性标志设置",
        ("*", "Chain AttrFlag"): "链属性标志",
        ("*", "AngleLimitEnable"): "启用角度限制",
        ("*", "Whether to enable angle limit.\nUsually recommended to enable it, otherwise angle limit will be invalid"): "是否启用角度限制.\n通常建议启用，否则角度限制将会无效",
        ("*", "AngleLimitRestitutionEnable"): "启用角度限制恢复",
        ("*", "Whether to enable angle limit restitution"): "是否启用角度限制恢复",
        ("*", "EndRotConstraintEnable"): "启用尾节点旋转约束",
        ("*", "Whether to enable the rotation of end node (uncertain)"): "是否启用尾节点的旋转约束（不确定）",
        ("*", "TransAnimationEnable"): "启用反动画",
        ("*", "Whether to enable trans animation.\nAfter activating, the chain will stagnate in a motion stop posture, but the specific meaning is unclear"): "是否启用反动画.\n启用后链会停滞在运动停止的姿态,尚不清楚具体含义",
        ("*", "AngleFreeEnable"): "启用自由角度",
        ("*", "Whether to enable angle free"): "是否启用自由角度",
        ("*", "StretchBothEnable"): "启用链骨伸缩",
        ("*", "Whether to enable stretch (uncertain).\nDepends on the mass and elasticity of the nodes"): "是否启用链骨伸缩（不确定）.\n取决于节点的质量和弹性",
        ("*", "PartBlendEnable"): "启用部分混合",
        ("*", "Whether to enable part blend.\nAfter activating, the chain seems to squeeze towards the center, but the specific meaning is unclear"): "是否启用部分混合.\n启用后链似乎会向中心挤压，尚不清楚具体含义",

        ("*", "unkn AttrFlag1"): "未知属性标志1",
        ("*", "Actually binary. Common values are 0, 1, 17, 32. More testing is needed."
              "\nTaking 1 for the 1 bits seems to make the chain harder (or recovers faster) than taking 0."
              "\nTaking 1 for the 2 bits will force the chain to stretch, like a spring"): "未知标志,实际为二进制.常见取值有0,1,17,32.还需更多测试."
                                                                                           "\n第一位取1相比取0,链似乎会更硬一些(或者说恢复原状更快)."
                                                                                           "\n第二位取1相比取0,链会被强制拉伸,像一根弹簧一样",
        ("*", "unkn AttrFlag2"): "未知属性标志2",
        ("*", "Actually binary, Usually the value is 0, rarely the value is 1"): "未知标志,实际为二进制,通常取值为0,很少为1",

        ("*", "Other Chain Settings"): "其他链设置",

        ("*", "Collider Attribute"): "碰撞属性",
        ("*", "Usually the value is -1"): "值通常为-1",
        ("*", "Collider Group"): "碰撞组",
        ("*", "Usually the value is 1"): "值通常为1",
        ("*", "Collider Type"): "碰撞类型",


        ("*", "Gravity"): "重力",
        ("*", "Usually only need to change the Y axis gravity."
              "\nWhen the value is negative, the direction of gravity reverses.When the value is 0, there is no gravity."
              "\nGravityScaling with the Header part can be viewed as a product, so when both values are negative, the actual direction of gravity is still downward"): "通常只需要调整y轴方向的重力即可."
                                                                                                                                                                        "\n当值为负数时,重力方向会反转.当值为0时,则无重力."
                                                                                                                                                                        "\n与Header部分的重力比例可以看做乘积关系,所以当二者值都为负时，实际的重力方向仍然是向下的",


        ("*", "Damping"): "阻尼",

        ("*", "TransForce Coef"): "反作用力系数",
        ("*", "If \"Global TransForce Coef\" is 1, it usually should be set to a value less than 1 here."
              "\nWhen the value is 1, the trans force is equal to the acting force. This is the usual value."
              "\nWhen the value is greater than 1, the trans force will be greater than the acting force. And the higher the value, the more intense the chain moves."
              "\nWhen the value is less than 1, the trans force will be less than the acting force. And the smaller the value, the weaker the chain moves."
              "\nWhen the value is negative, the trans force and acting force will reverse, causing the chain that was originally moving backward to move forward"): "若\"整体反作用力系数\"为1，则此处通常应设为小于1的数值."
                     "\n当值为1时，反作用力等于作用力. 这是通常设定的数值."
                     "\n当值大于1时，反作用力会大于作用力. 并且数值越大，链的运动幅度越剧烈."
                     "\n当值小于1时，反作用力会小于作用力. 并且数值越小，链的运动幅度越微弱."
                     "\n当值为负时，反作用力和作用力会反向，会导致原本向后运动的链变为向前运动",

        ("*", "Spring Coef"): "弹性系数",
        ("*", "If \"SpringScaling\" is 1, it usually should be set to a value less than 1 here, even less than 0.1."
              "\nThe greater the value, the harder the chain and the less the deformation."
              "\nThe smaller the value, the softer the chain and the greater the deformation."
              "\nSetting it to a negative value is not recommended, which will lead to some unstable physical behavior"): "若\"弹性比例\"为1，则此处通常应设为小于1的数值，甚至小于0.1."
                                                                                                                          "\n值越大，则链越硬，相应的形变越小."
                                                                                                                          "\n值越小，则链越软，相应的形变越大."
                                                                                                                          "\n不建议设为负数，会导致一些不稳定的物理行为",


        ("*", "Limit Force"): "限制力",
        ("*", "Usually the value is 100"): "值通常为100",
        ("*", "Friction Coef"): "摩擦系数",
        ("*", "Usually the value is 0"): "值通常为0",
        ("*", "Reflect Coef"): "反弹系数",
        ("*", "Usually the value is 0.1"): "值通常为0.1",

        ("*", "Wind Rate"): "风力比例",

        ("*", "Wind Limit"): "风力极限",
        ("*", "There is a hidden variable in memory called \"UseWindLimit\"."
              "\nWhen the value here is a negative integer, UseWindLimit = 50."
              "\nWhen the value here is a positive integer, UseWindLimit = WindLimit."
              "\nOnly seen taking 10 in a few ctc files, so you can just default to -1"): "在内存中有一个隐藏变量为UseWindLimit."
                                                                                           "\n当此处数值为负整数时,UseWindLimit值恒为50."
                                                                                           "\n当此处数值为正整数时,UseWindLimit=风力极限."
                                                                                           "\n只在零星几个CTC文件中看到过取10,总之平时默认-1即可",


        #CTCNodePG
        ("*", "CTC Node Settings"): "CTC节点设置",

        ("*", "unkn Byte1"): "未知字节1",
        ("*", "Unknown flag, which may actually be binary, default to 0"): "未知标志,实际可能为二进制.\n取0以外值的CTC文件可能没有,所以基本上不用管,默认0即可",
        ("*", "unkn Byte2"): "未知字节2",
        ("*", "Unknown flag, which may actually be binary or boolean."
              "\nTaking 1 may make the node more compact than taking 0 (uncertain).\nThe default is 0"): "未知标志,实际可能为二进制或布尔值.\n取1相比取0可能会让节点更紧致一些(不确定).\n默认0即可",

        ("*", "Angle Mode"): "角度模式",
        ("*", "Node will rotate in any direction"): "节点将向任意方向旋转",
        ("*", "Rotation of node will be limited to a cone"): "节点的旋转将被限制在一个圆锥体内",
        ("*", "Rotation of node will be limited to rotation only along the z-axis"): "节点的旋转将被限制为只绕Z轴旋转",
        ("*", "Rotation of node will be limited to an oval cone"): "节点的旋转将被限制在一个椭圆锥体内",


        ("*", "Collision Shape"): "碰撞形状",
        ("*", "No Collision"): "无碰撞体",
        ("*", "The shape of collision is a sphere"): "碰撞体形状为球体",
        ("*", "The shape of collision is a capsule"): "碰撞体形状为胶囊",

        ("*", "unkn Enum"): "未知枚举值",
        ("*", "Unknown enumeration, usually 1, but rarely used 0 and 2.\nNormally, you can default to 1"): "未知枚举值,通常为1,很少会用到0和2,平时默认1即可.\n",


        ("*", "Collision Radius"): "碰撞半径",
        ("*", "Collision Radius"): "碰撞半径",

        ("*", "Angle Limit Radius"): "角度限制半径",
        ("*", "The amount the node is allowed to rotate from it's angle limit direction."
              "\nIt is actually in radian, representing the top angle of a cone."
              "\nThe bottom radius of the cone is used here to represent the top angle, which is incorrect but sufficient to represent the actual size"): "允许节点在其角度限制方向上旋转的量.\n实际为弧度制，表示圆锥体的顶角.\n此处使用圆锥体的底面半径代为表示顶角，虽然不正确但足够表示实际的大小",



        ("*", "Width Rate"): "宽度比率",
        ("*", "Rate of width to length of oval at the bottom of cone."
              "\nEffective only when Angle Mode is Oval."
              "\nWhen the value is 0, Oval has the same effect as Hinge",): "角度限制圆锥体底部椭圆的宽度相较于长度的比例.\n只在角度模式为Oval时才生效.\n当值为0时，Oval的效果几乎和Hinge相同",

        ("*", "Mass"): "质量",
        ("*", "Most ctc files default to 1, a few will have values greater than 1 or even around 10, and some will have values less than 1."
              "\nIt is not clear how this parameter works"): "节点质量,大部分ctc文件都是默认1,少部分取值会大于1甚至到10左右,还有一部分取值会小于1.\n目前不是很清楚该参数如何作用",

        ("*", "Elastic Coef"): "弹性系数",
        ("*", "Note that the elastic coef here is different from the spring coef of chain."
              "\nThe smaller the elastic coef, the easier the node is to be stretched."
              "\nThe larger the elastic coef, the more likely the node will be to maintain its original length."
              "\nChanging this value is not recommended，usually 1, which means that the node always maintains its original length"): "注意此处的弹性系数与链设置中的弹性系数不一样.\n弹性系数越小，节点越容易被拉长.\n弹性系数越大，节点越倾向于保持原本的长度.\n不建议修改此值，通常为1，即节点总是保持原本的长度",


        #CCLPG
        ("*", "CCL Collision Settings"): "CCL碰撞设置",

        ("*", "Head Offset"): "头部位置",
        ("*", "Set position of the head collision object"): "设置碰撞体头部对象的位置",

        ("*", "Tail Offset"): "尾部位置",
        ("*", "Set position of the tail collision object"): "设置碰撞体尾部对象的位置",




    }
}

dictionary = preprocess_dictionary(dictionary)

dictionary["zh_HANS"] = dictionary["zh_CN"]
