# 响应头部重写

## 描述

`response-header-rewrite`插件对请求的响应头进行变更，包括新增、删除和修改操作

## 属性

| 名称       | 类型     | 必选项 | 默认值   | 描述           |
|----------|--------|-----|-------|--------------|
| Header名称 | string | 是   | -     | 需要操作的响应头名称   |
| 修改类型     | select | 是   | 创建或追加 | 对响应的的操作类型    |
| 取值       | string | 是   | -     | 对于响应头新增或修改的值 |


## 前置条件

以下curl命令中存在变量，使用前需要替换为真实环境数据，变量以`{{}}`符号包裹，例如`{{ 网关ID }}`需要根据网关的实际ID进行替换；创建插件命令中`PluginConfiguration`（插件配置）需要根据实际需要进行配置

## 创建

```shell
curl -XPOST -v -H "Content-Type:application/json" -d '{
  "BindingObjectId": {{ 路由ID }},
  "BindingObjectType": "routeRule",
  "GwId": {{ 网关ID }},
  "PluginConfiguration": "{\"headerKey\":[\"headerKey\": \"testHeader\",\"operation\": \"update\",\"headerValue\": \"testHeaderValue\"]}",
  "PluginType": "response-header-rewrite"
}' http://{{ hango-portal ip:port }}/gdashboard?Action=BindingPlugin&Version=2019-09-01
```

## 测试

```shell
## 基于如下基础curl命令，根据后端服务要求将请求具体化，观察响应中的头变化是否符合插件配置的预期（响应头是否新增、被修改或删除）
curl -v "http://{{ 网关IP }}/{{ 路由path }}" -H "host:{{ 网关关联域名 }}"
```

## 删除

```shell
curl -v -H "Content-Type:application/json" http://{{ hango-portal ip:port }}/gdashboard?PluginBindingInfoId={{ 插件ID }}&Action=UnbindingPlugin&Version=2019-09-01
```

## 界面配置方法

[插件界面配置方法引导](plugin-configuring-guide.md)