# Referer黑白名单

## 描述

`referer-restriction`插件可以基于请头头Referer来针对来源的请求进行黑名单或白名单限制

## 属性

| 名称                | 类型      | 必选项 | 范围                                                | 描述                       |
|-------------------|---------|-----|---------------------------------------------------|--------------------------|
| kind              | string  | 是   | referer-restriction                                   | 插件类型（值固定）                |
| type              | integer | 是   | [0, 1]                                            | Referer黑白名单策略<br/>0:黑名单；1:白名单 |
| list[].match_type | string  | 是   | exact_match<br/>prefix_match<br/>safe_regex_match | Referer黑白名单策略                 |
| list[].value      | string  | 是   | length <= 200                                     | Referer值              |


## 前置条件

以下curl命令中存在变量，使用前需要替换为真实环境数据，变量以`{{}}`符号包裹，例如`{{ 网关ID }}`需要根据网关的实际ID进行替换；创建插件命令中`PluginConfiguration`（插件配置）需要根据实际需要进行配置

## 创建

```shell
curl -XPOST -v -H "Content-Type:application/json" -d '{
  "BindingObjectId": {{ 路由ID }},
  "BindingObjectType": "routeRule",
  "GwId": {{ 网关ID }},
  "PluginConfiguration": "{\"type\":\"0\",\"list\":[{\"match_type\":\"exact_match\",\"value\":[\"deny\"]}],\"kind\":\"referer-restriction\"}",
  "PluginType": "referer-restriction"
}' http://{{ hango-portal ip:port }}/gdashboard?Action=BindingPlugin&Version=2019-09-01
```

## 测试

```shell
## 修改如下请求的Referer参数，与插件配置的Referer值一致，测试黑白名单效果
curl -v "http://{{ 网关IP }}/{{ 路由path }}" -H "host:{{ 网关关联域名 }}" -H "Referer:xxx"
```

## 删除

```shell
curl -v -H "Content-Type:application/json" http://{{ hango-portal ip:port }}/gdashboard?PluginBindingInfoId={{ 插件ID }}&Action=UnbindingPlugin&Version=2019-09-01
```

## 界面配置方法

[插件界面配置方法引导](plugin-configuring-guide.md)