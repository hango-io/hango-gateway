# 本地限流

## 描述

`local-limiting`插件可以实现基于网关实例级别的多维度流量

## 属性

| 名称                                   | 类型      | 必选项 | 范围                                                | 描述             |
|--------------------------------------|---------|-----|---------------------------------------------------|----------------|
| kind                                 | string  | 是   | local-limiting                                    | 插件类型（值固定）      |
| limit_by_list[].headers[].headerKey  | string  | 否   | length <= 200                                     | 限流匹配Header名    |
| limit_by_list[].headers[].match_type | string  | 是   | exact_match<br/>prefix_match<br/>safe_regex_match | 限流请求Header匹配方式 |
| limit_by_list[].headers[].value      | string  | 是   | length <= 200                                     | 限流匹配Header值    |
| limit_by_list[].day                  | integer | 是   | \> 0                                              | 天维度允许通过的请求数量   |
| limit_by_list[].hour                 | integer | 是   | \> 0                                              | 时维度允许通过的请求数量   |
| limit_by_list[].minute               | integer | 是   | \> 0                                              | 分维度允许通过的请求数量   |
| limit_by_list[].second               | integer | 是   | \> 0                                              | 秒维度允许通过的请求数量   |

## 前置条件

以下curl命令中存在变量，使用前需要替换为真实环境数据，变量以`{{}}`符号包裹，例如`{{ 网关ID }}`需要根据网关的实际ID进行替换；创建插件命令中`PluginConfiguration`（插件配置）需要根据实际需要进行配置

## 创建

```shell
curl -XPOST -v -H "Content-Type:application/json" -d '{
  "BindingObjectId": {{ 路由ID }},
  "BindingObjectType": "routeRule",
  "GwId": {{ 网关ID }},
  "PluginConfiguration": "{\"limit_by_list\":[{\"headers\":[{\"headerKey\":\"limitHeader\",\"match_type\":\"exact_match\",\"value\":\"limitHeaderValue\"}],\"day\":4321,\"hour\":321,\"minute\":21,\"second\":1}],\"kind\":\"local-limiting\",\"name\":\"local-limiting\"}",
  "PluginType": "local-limiting"
}' http://{{ hango-portal ip:port }}/gdashboard?Action=BindingPlugin&Version=2019-09-01
```

## 测试

```shell
## 如下命令展示了用命令调用3次请求的案例，可修改for中的请求次数，进行限流次数测试；可以为请求添加header进行限流请头求匹配测试
for((i=0;i<3;i++));do curl -v "http://{{ 网关IP }}/{{ 路由path }}" -H "host:{{ 网关关联域名 }}" -H "blackHeader:blackHeaderValue";done
```

## 删除

```shell
curl -v -H "Content-Type:application/json" http://{{ hango-portal ip:port }}/gdashboard?PluginBindingInfoId={{ 插件ID }}&Action=UnbindingPlugin&Version=2019-09-01
```

## 界面配置方法

[插件界面配置方法引导](plugin-configuring-guide.md)