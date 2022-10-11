# 百分比限流

## 描述

`percent-limit`插件可以对网关流量基于百分比粒度进行限流

## 属性

| 名称            | 类型      | 必选项 | 范围            | 描述         |
|---------------|---------|-----|---------------|------------|
| kind          | string  | 是   | percent-limit | 插件类型（值固定）  |
| limit_percent | integer | 是   | [0, 100]      | 允许通过流量的百分比 |


## 前置条件

以下curl命令中存在变量，使用前需要替换为真实环境数据，变量以`{{}}`符号包裹，例如`{{ 网关ID }}`需要根据网关的实际ID进行替换；创建插件命令中`PluginConfiguration`（插件配置）需要根据实际需要进行配置

## 创建

```shell
curl -XPOST -v -H "Content-Type:application/json" -d '{
  "BindingObjectId": {{ 路由ID }},
  "BindingObjectType": "routeRule",
  "GwId": {{ 网关ID }},
  "PluginConfiguration": "{\"limit_percent\":\"50\",\"kind\":\"percent-limit\"}",
  "PluginType": "percent-limit"
}' http://{{ hango-portal ip:port }}/gdashboard?Action=BindingPlugin&Version=2019-09-01
```

## 测试

```shell
## 通过脚本多次调用以下curl命令，测试网关百分比限流效果
curl -v "http://{{ 网关IP }}/{{ 路由path }}" -H "host:{{ 网关关联域名 }}"
```

## 删除

```shell
curl -v -H "Content-Type:application/json" http://{{ hango-portal ip:port }}/gdashboard?PluginBindingInfoId={{ 插件ID }}&Action=UnbindingPlugin&Version=2019-09-01
```

## 界面配置方法

[插件界面配置方法引导](plugin-configuring-guide.md)