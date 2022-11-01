# URI黑白名单

## 描述

`uri-restriction`是hango的一款rider插件（用户可基于hango的rider开发手册开发自己的rider插件），该插件可以基于请求的path进行黑白名单限制

## 属性

| 名称               | 类型       | 必选项 | 范围              | 描述          |
|------------------|----------|-----|-----------------|-------------|
| kind             | string   | 是   | uri-restriction | 插件类型（值固定）   |
| type             | string   | 是   | lua             | 插件技术实现（值固定） |
| config.allowlist | []string | 否   | length <= 200   | 白名单path     |
| config.denylist  | []string | 否   | length <= 200   | 黑名单path     |


## 前置条件

以下curl命令中存在变量，使用前需要替换为真实环境数据，变量以`{{}}`符号包裹，例如`{{ 网关ID }}`需要根据网关的实际ID进行替换；创建插件命令中`PluginConfiguration`（插件配置）需要根据实际需要进行配置

## 创建

```shell
curl -XPOST -v -H "Content-Type:application/json" -d '{
  "BindingObjectId": {{ 路由ID }},
  "BindingObjectType": "routeRule",
  "GwId": {{ 网关ID }},
  "PluginConfiguration": "{\"kind\":\"uri-restriction\",\"type\":\"lua\",\"config\":{\"allowlist\":[\"/test/blank\"],\"denylist\":[\"/test/black\"]}}",
  "PluginType": "uri-restriction"
}' http://{{ hango-portal ip:port }}/gdashboard?Action=BindingPlugin&Version=2019-09-01
```

## 测试

```shell
## 修改如下请求的{{ 路由path }}，配置为插件中的黑名单或白名单，观察请求被拦截或放行
curl -v "http://{{ 网关IP }}/{{ 路由path }}" -H "host:{{ 网关关联域名 }}"
```

## 删除

```shell
curl -v -H "Content-Type:application/json" http://{{ hango-portal ip:port }}/gdashboard?PluginBindingInfoId={{ 插件ID }}&Action=UnbindingPlugin&Version=2019-09-01
```

## 界面配置方法

[插件界面配置方法引导](plugin-configuring-guide.md)