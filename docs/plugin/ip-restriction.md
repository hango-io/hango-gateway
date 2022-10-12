# IP黑白名单

## 描述

`ip-restriction`插件可以针对来源于不同User-Agent（用户代理）的请求进行黑名单或白名单限制

## 属性

| 名称   | 类型       | 必选项 | 范围             | 描述                       |
|------|----------|-----|----------------|--------------------------|
| kind | string   | 是   | ip-restriction | 插件类型（值固定）                |
| type | integer  | 是   | [0, 1]         | IP黑白名单策略<br/>0:黑名单；1:白名单 |
| list | []string | 是   | IP格式           | IP值                      |


## 前置条件

以下curl命令中存在变量，使用前需要替换为真实环境数据，变量以`{{}}`符号包裹，例如`{{ 网关ID }}`需要根据网关的实际ID进行替换；创建插件命令中`PluginConfiguration`（插件配置）需要根据实际需要进行配置

## 创建

```shell
curl -XPOST -v -H "Content-Type:application/json" -d '{
  "BindingObjectId": {{ 路由ID }},
  "BindingObjectType": "routeRule",
  "GwId": {{ 网关ID }},
  "PluginConfiguration": "{\"type\":\"0\",\"list\":[\"192.168.2.101\",\"192.168.2.102\"],\"kind\":\"ip-restriction\"}",
  "PluginType": "ip-restriction"
}' http://{{ hango-portal ip:port }}/gdashboard?Action=BindingPlugin&Version=2019-09-01
```

## 测试

```shell
## 基于如下请求，基于不同IP（携带请求头X-Forwarded-For）来源请求网关测试IP黑白名单插件
curl -v "http://{{ 网关IP }}/{{ 路由path }}" -H "host:{{ 网关关联域名 }}"
```

## 删除

```shell
curl -v -H "Content-Type:application/json" http://{{ hango-portal ip:port }}/gdashboard?PluginBindingInfoId={{ 插件ID }}&Action=UnbindingPlugin&Version=2019-09-01
```

## 界面配置方法

[插件界面配置方法引导](plugin-configuring-guide.md)