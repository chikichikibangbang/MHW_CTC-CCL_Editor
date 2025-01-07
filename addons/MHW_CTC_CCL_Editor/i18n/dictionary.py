from MHW_CTC_CCL_Editor.common.i18n.dictionary import preprocess_dictionary

dictionary = {
    "zh_CN": {
        ("*", "Example Addon Side Bar Panel"): "示例插件面板",
        ("*", "Example Functions"): "示例功能",
        ("*", "ExampleAddon"): "示例插件",
        ("*", "Resource Folder"): "资源文件夹",
        ("*", "Int Config"): "整数参数",
        # This is not a standard way to define a translation, but it is still supported with preprocess_dictionary.
        "Boolean Config": "布尔参数",
        ("*", "Add-on Preferences View"): "插件设置面板",
        ("Operator", "ExampleOperator"): "示例操作",





        #CTC Header Settings面板
        ("*", "Note: The header settings here will affect all chains."): "注意：此处的标头设置会影响所有的物理链。",


        # ("*", "Attribute Flags"): "属性标识",
        ("*", "Determine certain movement properties of the chain."
              "\nIt is actually a binary, and the maximum bit may be 8 bits from testing."
              "\nThe most common value is 64 (mostly seen on armor), followed by 80 (mostly seen on pendants)."
              "\n80 seems to make the chain move more violently than 64, you can refer to the fluttering pendant."
              "\nThe main difference lies in the fifth and seventh bits of binary, and it is unclear what these bits mean"): "决定物理链的某些运动属性."
                                                                                                                    "\n实际为二进制，经测试最大位可能为8位."
                                                                                                                    "\n最常见的是64（多在防具上看到），其次是80（多在吊坠上看到）."
                                                                                                                    "\n80相比64似乎会使链的运动更为剧烈，可以参考会飘动的吊坠."
                                                                                                                    "\n主要区别在于二进制的第5位和第7位，尚不清楚这些位具体表示的含义",
        # ("*", "Set Attribute Flag"): "设定属性标识",
        ("*", "Set header attribute flag value from a list of known values"): "从已知数值的列表中设置属性标识",

        # ("*", "Step Time"): "时间步长",
        ("*", "The time interval between each update of the simulation by the physics engine."
              "\nSetting the step time to 0.16666 seconds means that the physics engine updates 60 times per second, which matches a frame rate of 60FPS."
              "\nPlease don't change this value"): "物理引擎每次更新模拟之间的时间间隔.\n将时间步长设置为1/60秒，意味着物理引擎每秒会进行60次更新，这与60FPS的帧率相匹配.\n请不要修改此值",

        # ("*", "Gravity Scaling"): "重力比例",
        ("*", "Multiple of the gravity applied to the chain, Usually 1."
              "\nWhen the value is negative, the direction of gravity reverses."
              "\nWhen the value is 0, there is no gravity"): "链受到重力的倍数，通常为1.\n当值为负数时，重力方向会反转.\n当值为0时，则无重力",

        # ("*", "Global Damping"): "整体阻尼",
        ("*", "The greater the damping, the greater the resistance, and the slower and more difficult the movement of the chain."
              "\nThe smaller the damping, the smaller the resistance, and the faster and more flexible the movement of the chain."
              "\nNormally the damping is 0 or 0.1, shouldn't be set to too high."
              "\nA negative value will cause the chain to gain additional energy and move automatically"): "阻尼越大，阻力越大，链的运动越缓慢和困难.\n阻尼越小，阻力越小，链的运动越迅速和灵活.\n阻尼通常为0或0.1，不应设为过高的值.\n值为负时，会使链获取额外的能量，从而自动运动",

        # ("*", "Global TransForce Coef"): "整体反作用力系数",
        ("*", "When the value is 1, the trans force is equal to the acting force. This is the usual value."
              "\nWhen the value is greater than 1, the trans force will be greater than the acting force. And the higher the value, the more intense the chain moves."
              "\nWhen the value is less than 1, the trans force will be less than the acting force. And the smaller the value, the weaker the chain moves."
              "\nWhen the value is negative, the trans force and acting force will reverse, causing the chain that was originally moving backward to move forward"): "当值为1时，反作用力等于作用力. 这是通常设定的数值."
                     "\n当值大于1时，反作用力会大于作用力. 并且数值越大，链的运动幅度越剧烈."
                     "\n当值小于1时，反作用力会小于作用力. 并且数值越小，链的运动幅度越微弱."
                     "\n当值为负时，反作用力和作用力会反向，会导致原本向后运动的链变为向前运动",

        # ("*", "Spring Scaling"): "弹性比例",
        ("*", "Multiple of chain elasticity, Usually 1."
              "\nSetting it to a negative value is not recommended, which will lead to some unstable physical behavior"): "链弹性的倍数，通常为1.\n不建议设为负数，会导致一些不稳定的物理行为",

        # ("*", "Wind Scale"): "风力范围平均值",
        # ("*", "Wind Scale Min"): "风力范围最小值",
        # ("*", "Wind Scale Max"): "风力范围最大值",
        ("*", "The magnitude of the wind force exposed to the chain is divided into average (median), minimum and maximum."
              "\nThe sizes of these three parameters should be determined by default according to the rule of \"WindScaleMax>=WindScale>=WindScaleMin\"."
              "\nJudging from the traversed CTC files, it seems that there is a relationship of \"WindScale=(WindScaleMin+WindScaleMax)/2\", which may be simply an average value"): "风力范围,分为平均值(中间值),最小值和最大值.\n这三个参数的大小应默认按照\"最大值>=平均值>=最小值\"的规则来取值.\n从遍历过的CTC文件来看,似乎有着\"平均值=(最小值+最大值)/2\"的固定关系,可能单纯是平均值",

        # ("*", "Wind Scale Weight"): "风力范围权重",



        #CTC Chain Settings面板

        # ("*", "Collision AttrFlag Settings"): "碰撞属性标志设置",
        # ("*", "Collision AttrFlag"): "碰撞属性标志",
        ("*", "Accounting value of all flags.\nChanging this value will change all flags at the same time"): "所有标志位的合算数值.\n更改此数值将同步更改所有标志位",
        # ("*", "CollisionSelfEnable"): "与其他链发生碰撞",
        ("*", "Whether the chain is allowed to collide with other chains"): "是否允许链与其他链发生碰撞",
        # ("*", "CollisionModelEnable"): "与ccl发生碰撞",
        ("*", "Whether the chain is allowed to collide with ccl file"): "是否允许链与与ccl文件发生碰撞",
        # ("*", "CollisionVGroundEnable"): "与地面发生碰撞",
        ("*", "Whether the chain is allowed to collide with the ground"): "是否允许链与地面发生碰撞",





        # ("*", "unkn AttrFlag1"): "未知属性标志1",
        ("*", "Actually binary. Common values are 0, 1, 17, 32. More testing is needed."
              "\nTaking 1 for the 1 bits seems to make the chain harder (or recovers faster) than taking 0."
              "\nTaking 1 for the 2 bits will force the chain to stretch, like a spring"): "未知标志,实际为二进制.常见取值有0,1,17,32.还需更多测试."
                                                                                           "\n第一位取1相比取0,链似乎会更硬一些(或者说恢复原状更快)."
                                                                                           "\n第二位取1相比取0,链会被强制拉伸,像一根弹簧一样",
        # ("*", "unkn AttrFlag2"): "未知属性标志2",
        ("*", "Actually binary, Usually the value is 0, rarely the value is 1"): "未知标志,实际为二进制,通常取值为0,很少为1",

        # ("*", "Gravity"): "重力",
        ("*", "Usually only need to change the Y axis gravity."
              "\nWhen the value is negative, the direction of gravity reverses.When the value is 0, there is no gravity."
              "\nGravityScaling with the Header part can be viewed as a product, so when both values are negative, the actual direction of gravity is still downward"): "通常只需要调整y轴方向的重力即可."
                                                                                                                                                                        "\n当值为负数时,重力方向会反转.当值为0时,则无重力."
                                                                                                                                                                        "\n与Header部分的重力比例可以看做乘积关系,所以当二者值都为负时，实际的重力方向仍然是向下的",



        # ("*", "Damping"): "阻尼",

        # ("*", "TransForce Coef"): "反作用力系数",
        ("*", "If \"Global TransForce Coef\" is 1, it usually should be set to a value less than 1 here."
              "\nWhen the value is 1, the trans force is equal to the acting force. This is the usual value."
              "\nWhen the value is greater than 1, the trans force will be greater than the acting force. And the higher the value, the more intense the chain moves."
              "\nWhen the value is less than 1, the trans force will be less than the acting force. And the smaller the value, the weaker the chain moves."
              "\nWhen the value is negative, the trans force and acting force will reverse, causing the chain that was originally moving backward to move forward"): "若\"整体反作用力系数\"为1，则此处通常应设为小于1的数值."
                     "\n当值为1时，反作用力等于作用力. 这是通常设定的数值."
                     "\n当值大于1时，反作用力会大于作用力. 并且数值越大，链的运动幅度越剧烈."
                     "\n当值小于1时，反作用力会小于作用力. 并且数值越小，链的运动幅度越微弱."
                     "\n当值为负时，反作用力和作用力会反向，会导致原本向后运动的链变为向前运动",

        # ("*", "Spring Coef"): "弹性系数",
        ("*", "If \"SpringScaling\" is 1, it usually should be set to a value less than 1 here, even less than 0.1."
              "\nThe greater the value, the harder the chain and the less the deformation."
              "\nThe smaller the value, the softer the chain and the greater the deformation."
              "\nSetting it to a negative value is not recommended, which will lead to some unstable physical behavior"): "若\"弹性比例\"为1，则此处通常应设为小于1的数值，甚至小于0.1."
                                                                                                                          "\n值越大，则链越硬，相应的形变越小."
                                                                                                                          "\n值越小，则链越软，相应的形变越大."
                                                                                                                          "\n不建议设为负数，会导致一些不稳定的物理行为",



        #CTC Node Settings面板

        # ("*", "Angle Mode"): "角度模式",
        ("*", "Node will rotate in any direction"): "节点将向任意方向旋转",
        ("*", "Rotation of node will be limited to a cone"): "节点的旋转将被限制在一个圆锥体内",
        ("*", "Rotation of node will be limited to rotation only along the z-axis"): "节点的旋转将被限制为只绕Z轴旋转",
        ("*", "Rotation of node will be limited to an oval cone"): "节点的旋转将被限制在一个椭圆锥体内",


        # ("*", "Collision Shape"): "碰撞形状",
        ("*", "No Collision"): "无碰撞体",
        ("*", "The shape of collision is a sphere"): "碰撞体形状为球体",
        ("*", "The shape of collision is a capsule"): "碰撞体形状为胶囊",


        # ("*", "Collision Radius"): "碰撞半径",
        # ("*", "Collision Radius"): "碰撞半径",

        # ("*", "Angle Limit Radius"): "角度限制半径",
        ("*", "The amount the node is allowed to rotate from it's angle limit direction."
              "\nIt is actually in radian, representing the top angle of a cone."
              "\nThe bottom radius of the cone is used here to represent the top angle, which is incorrect but sufficient to represent the actual size"): "允许节点在其角度限制方向上旋转的量.\n实际为弧度制，表示圆锥体的顶角.\n此处使用圆锥体的底面半径代为表示顶角，虽然不正确但足够表示实际的大小",



        # ("*", "Width Rate"): "宽度比率",
        ("*", "Rate of width to length of oval at the bottom of cone."
              "\nEffective only when Angle Mode is Oval."
              "\nWhen the value is 0, Oval has the same effect as Hinge",): "角度限制圆锥体底部椭圆的宽度相较于长度的比例.\n只在角度模式为Oval时才生效.\n当值为0时，Oval的效果几乎和Hinge相同",



        # ("*", "Elastic Coef"): "弹性系数",
        ("*", "Note that the elastic coef here is different from the spring coef of chain."
              "\nThe smaller the elastic coef, the easier the node is to be stretched."
              "\nThe larger the elastic coef, the more likely the node will be to maintain its original length."
              "\nChanging this value is not recommended，usually 1, which means that the node always maintains its original length"): "注意此处的弹性系数与链设置中的弹性系数不一样.\n弹性系数越小，节点越容易被拉长.\n弹性系数越大，节点越倾向于保持原本的长度.\n不建议修改此值，通常为1，即节点总是保持原本的长度",










    }
}

dictionary = preprocess_dictionary(dictionary)

dictionary["zh_HANS"] = dictionary["zh_CN"]
