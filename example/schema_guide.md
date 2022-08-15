# 结构

```json
{
  "version": "版本",
  "inject": {}, // 需要在最终特殊注入的参数，不会展示
  "formatter": { // 重定义最终参数字段，不定义时候，按照layouts结构返回
  },
  "layouts": [
    {
      "key": "后端接口 key",
      "alias": "前端字段显示的 label",
      "help": "label 旁边的 ❓ hover 提示",
      "type": "支持的类型", // 下表详细提供
      "default": "默认值",
      "options": [ // 可选字段，支持 string 或 object
        "普通字符串",
        { // or Object
          "text": "前端展示的文字",
          "value": "后端映射的值"
        }
      ],
      "layouts": [
        ... // 嵌套循环字段
      ],

      // 以下功能为增强型功能
      "rules": [ // 规则校验参数，支持 string
        "Required" // 必须填写
      ],
      "disabled": false, // 是否禁用
      "visible": { // 条件显示
        [key]: "等于某个值时起作用"
      },
      "invisible": { // 条件隐藏
        [key]: "等于某个值时起作用"
      },

      // 以下为保留字段
      "role": "角色",
      "style": {}, // 自定义样式，暂不支持
    }
  ]
}
```

# 配置

## 特殊参数

| 字段      | 类型   | 备注                                             | 默认值 |
| --------- | ------ | ------------------------------------------------ | ------ |
| inject    | Object | 需要在最终特殊注入的参数，不会展示               | N      |
| version   | String | 版本控制预留字段                                 | N      |
| formatter | Object | 格式化提交结果，如果配置了，则覆盖原 schema 格式 | N      |
|           |        |                                                  |        |

## 基本参数

| 字段                | 类型                     | 备注                                                     | 默认值 |
| ------------------- | ------------------------ | -------------------------------------------------------- | ------ |
| layouts             | Array`<Object>`          | 布局，_嵌套循环字段_（数组嵌套时，需要配合`type=array`） | Y      |
| key                 | String                   | 后端接口 key                                             | Y      |
| alias               | String                   | 前端字段显示的 label                                     | Y      |
| help                | String                   | label 旁边的 ❓ hover 提示                                | N      |
| description         | String                   | 描述提示信息                                         | N      |
| placeholder         | String                   | 输入框内提示信息                                         | N      |
| [type](#Type)       | String                   | 支持的类型，参考表 [Type](#Type)                         | Y      |
| default             |                          | 字段默认值。（返回值必要时，请填写）                     | N      |
| [options](#Options) | Array`<String | Object>` | 根据不同`type` 进行配合使用，参考表 [Options](#Options)  | N      |
|                     |                          |                                                          |        |
|                     |                          |                                                          |        |

### Type

| 字段         | 备注                                              |
| ------------ | ------------------------------------------------- |
| text         | 文本格式                                          |
| input        | 输入框                                            |
| string       | 同 `input`                                        |
| multi_input  | 多值输入框，返回数组                              |
| multi_string | 同 `multi_input`                                  |
| number       | 数字输入框                                        |
| select       | 下拉选择框，需配合 `options` 参数                 |
| array        | 同 `select`                                       |
| multi_select | 下拉多选择框，需配合 `options` 参数               |
| multi_array  | 同 `multi_select`                                 |
| radio        | 单选组，需配合 `options` 参数                     |
| checkbox     | 多选组，需配合 `options` 参数                     |
| switch       | Boolean 值切换                                    |
| boolean      | 同 `switch`                                       |
| json         | json格式文本输入                                       |
|              |                                                   |
| button       | 按钮（保留字段，暂不支持），需配合 `options` 参数 |
|              |                                                   |

### Options

| 字段     | 备注               |
| -------- | ------------------ |
| text     | 前端展示的文字     |
| value    | 后端映射的值       |
| disabled | 是否禁用当前选项   |
|          |                    |
| color    | 保留字段，暂不支持 |
| event    | 保留字段，暂不支持 |
|          |                    |

## 增强参数

| 字段      | 类型              | 备注                             | 是否必需 |
| --------- | ----------------- | -------------------------------- | -------- |
| rules     | Array`<String>`   | 校验规则，参考表 [Rules](#Rules) | N        |
| disabled  | Boolean           | 是否禁用                         | N        |
| visible   | Boolean \| Object | 条件显示                         | N        |
| invisible | Boolean \| Object | 条件隐藏                         | N        |
|           |                   |                                  |          |

### Rules

`rules` 中，未在下表中声明的内置规则，都是按照正则表达式进行解析。

| 字段           | 备注                                   |
| -------------- | -------------------------------------- |
| Required       | 必须填写                               |
| Number         | 有效的正整数                           |
| Name           | 由字母、中文、数字、下划线或中划线组成 |
| MaxLength(200) | 最大长度 200 位                        |
| MinLength(100) | 最小长度 100 位                        |
| MaxNumber(999) | 最大数字 999                           |
| MinNumber(1)   | 最小数字 1                             |
| Unique         | 数组类型时，可检测是否重复                            |
| ArrayMaxLength(10)   | 数组类型时，最大 10 组                             |
| ArrayMinLength(1)   | 数组类型时，最小 1 组                            |
|                |                                        |

### 自定义正则

```js
            "rules": [
                "Required",
                {
                    "pattern": "^\\d+$",
                    "flags": "", // 正则表达式修饰符:  i	执行对大小写不敏感的匹配。g	执行全局匹配（查找所有匹配而非在找到第一个匹配后停止）。m	执行多行匹配。
                    "message": "自定义提示，必须是数字",
                }
            ]
```

正则表达式修饰符:

![image.png](http://pfp.ps.netease.com/kmspvt/file/612df4966158bc85425e8523ViyrJGmZ01?sign=Qj8Ok88lN_diq8__i5hXOlxYlXc=&expire=1660574063)

## 保留参数

| 字段  | 类型   | 备注                               | 是否必需 |
| ----- | ------ | ---------------------------------- | -------- |
| role  | String | 内置角色行为（保留字段，暂不支持） | N        |
| style | Object | 保留字段，暂不支持                 | N        |
|       |        |                                    |          |
|       |        |                                    |          |
|       |        |                                    |          |



## 特殊字段解释

### inject

`inject` 参数是用来定义一些特殊的不再前端展示的内容，最终会合并到主结构体一起提交。

例如：

schema 定义如下

```json
{
    "layouts": [
        {
            "key": "a",
            "alias": "a",
            "layouts": [
                {
                    "key": "b",
                    "alias": "b",
                    "type": "input",
                }
            ]
        },
        {
            "key": "c",
            "alias": "c",
            "type": "input",
        }
    ]
}
```

正常返回时的结构为：

```json
{
    "a": {
        "b": "",
    },
    "c": "",
}
````

如果我们定义了 `inject` 参数，如：

```json
{
    "inject": {
        "kind": "abc",
        "a": {
            "d": "ddd",
        }
    },
    "layouts": [
        ...
    ]
}
```

则返回的最终结果将是如下：

```json
{
    "kind": "abc",
    "a": {
        "b": "",
        "d": "ddd",
    },
    "c": "",
}
```

### formatter

`formatter` 更强大的自定义返回结构体，最总格式将按照 `formatter` 定义的结构进行重构，如下：

例如：

schema 定义如下

```json
{
    "layouts": [
        {
            "key": "a",
            "alias": "a",
            "layouts": [
                {
                    "key": "b",
                    "alias": "b",
                    "type": "input",
                }
            ]
        },
        {
            "key": "c",
            "alias": "c",
            "type": "input",
        }
    ]
}
```

正常返回时的结构为：

```json
{
    "a": {
        "b": "bbb",
    },
    "c": "ccc",
}
````

如果我们定义了 `formatter` 参数（其中 `+` 为内置连接符号），如：

    连接符号为：+
    取值为：&， key和value都要 & 开头取值，否则为字符串
    @号开头的 value 数组，会拉平为 map。数组种必须要有 { key: '', value: '' } 两个字段'

**注意**： 如果使用了上述的符号，请把原 layouts 定义字段结构映射到 formatter 的原始位置上。否则更新取值无法实现！

```json
{
    "formatter": {
        "Result": "&a.b+c"
    },
    "layouts": [
        ...
    ]
}
```

则返回的最终结果将是如下：

```json
{
    "Result": "bbbccc",
}
```


# 例子 (可不看)

```json
{
    "inject": {
        "name": "ianus-rate-limiting",
        "kind": "ianus-rate-limiting",
        "limit_by_list": {
            "kind": "abc"
        }
    },
    "layouts": [{
            "key": "type_text",
            "description": "text 类型的 Demo",
            "default": "我是文本",
            "alias": "text",
            "type": "text"
        },
        {
            "key": "type_switch",
            "description": "switch 类型的 Demo",
            "alias": "switch",
            "type": "switch"
        },
        {
            "key": "type_input",
            "description": "input 类型的 Demo",
            "alias": "input",
            "type": "input"
        },
        {
            "key": "type_multi_input",
            "description": "multi_input 类型的 Demo",
            "alias": "multi_input",
            "type": "multi_input"
        },
        {
            "key": "type_number",
            "description": "number 类型的 Demo",
            "alias": "number",
            "type": "number"
        },
        {
            "key": "type_select",
            "description": "select 类型的 Demo",
            "alias": "select",
            "type": "select",
            "options": ["A", "B"]
        },
        {
            "key": "type_multi_select",
            "description": "multi_select 类型的 Demo",
            "alias": "multi_select",
            "type": "multi_select",
            "options": ["A", "B"]
        },
        {
            "key": "type_radio",
            "description": "radio 类型的 Demo",
            "alias": "radio",
            "type": "radio",
            "options": ["A", "B"]
        },
        {
            "key": "type_checkbox",
            "description": "checkbox 类型的 Demo",
            "alias": "checkbox",
            "type": "checkbox",
            "options": ["A", "B"]
        },
        {
            "key": "type_json",
            "description": "json 类型的 Demo",
            "alias": "json",
            "type": "json",
            "default": { "info": "我是默认值" }
        },
        {
            "key": "limit_by_list",
            "help": "1.频率限制是指限制带同一标识请求在给定时间段内可处理的次数;\n2.user-开头的是指用户在某维度的参数, 不以user-开头的是指下游服务器的参数;\n3.使用user-xxx参数的前提是\"请求转换插件\"已经将xxx参数转换为user-xxx.;\n4.当前版本计数方式限制为local, 所以实际频控限制=配置的限制*集群节点数量",
            "alias": "复杂类型",
            "type": "array",
            "layouts": [{
                    "key": "identifier_extractor",
                    "help": "用于计算请求标识，以供计数使用;例如，Ip, Header[User-Agent]",
                    "alias": "标识提取策略",
                    "type": "string"
                },
                {
                    "key": "pre_condition",
                    "help": "满足前置条件的请求才会进入频控流程. 左变量为identifier_extractor提取的值",
                    "alias": "频控前置条件",
                    "type": "array",
                    "layouts": [{
                            "key": "right_value",
                            "alias": "right_value",
                            "type": "string"
                        },
                        {
                            "key": "operator",
                            "alias": "operator",
                            "type": "select",
                            "default": "=",
                            "options": ["≈", "!≈", "=", "!="]
                        }
                    ]
                },
                {
                    "key": "key",
                    "alias": "KEY",
                    "type": "input"
                },
                {
                    "key": "value",
                    "alias": "VALUE",
                    "type": "input"
                },
                {
                    "key": "day",
                    "alias": "每天请求数",
                    "type": "number"
                },
                {
                    "key": "minute",
                    "alias": "每分钟请求数",
                    "type": "number"
                },
                {
                    "key": "second",
                    "alias": "每秒请求数",
                    "type": "number"
                },
                {
                    "key": "limit_by_list",
                    "help": "1.频率限制是指限制带同一标识请求在给定时间段内可处理的次数;\n2.user-开头的是指用户在某维度的参数, 不以user-开头的是指下游服务器的参数;\n3.使用user-xxx参数的前提是\"请求转换插件\"已经将xxx参数转换为user-xxx.;\n4.当前版本计数方式限制为local, 所以实际频控限制=配置的限制*集群节点数量",
                    "alias": "限制标识列表3",
                    "layouts": [{
                            "visible": {
                                "true": ["this", "month"]
                            },
                            "key": "identifier_extractor",
                            "help": "用于计算请求标识，以供计数使用;例如，Ip, Header[User-Agent]",
                            "alias": "标识提取策略",
                            "type": "string"
                        },
                        {
                            "key": "month",
                            "alias": "每月请求数",
                            "type": "switch"
                        },
                        {
                            "key": "hour",
                            "alias": "每小时请求数",
                            "type": "number"
                        }
                    ]
                }
            ]
        },
        {
            "key": "rules",
            "description": "rules 校验的 Demo, 必须填写，且只能输入数字",
            "alias": "rules",
            "type": "input",
            "rules": [
                "Required",
                "^\\d+$"
            ]
        }
    ]
}
```
