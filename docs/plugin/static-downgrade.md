# 静态降级

## 描述

`static-downgrade`插件可匹配指定的请求进行降级，返回指定的响应内容

## 属性

| 名称                                      | 类型       | 必选项 | 范围                                                                                   | 描述           |
|-----------------------------------------|----------|-----|--------------------------------------------------------------------------------------|--------------|
| kind                                    | string   | 是   | static-downgrade                                                                     | 插件类型（值固定）    |
| condition.request.requestSwitch         | boolean  | 是   | -                                                                                    | 是否使用请求进行匹配   |
| condition.request.method                | []string | 否   | GET<br/>POST<br/>PUT<br/>DELETE<br/>OPTIONS<br/>HEAD<br/>TRACE<br/>CONNECT<br/>PATCH | HTTP的请求方法类型  |
| condition.request.path.match_type       | string   | 否   | exact_match<br/>safe_regex_match                                                     | 请求路径匹配方式     |
| condition.request.path.value            | string   | 否   | -                                                                                    | 请求路径匹配内容     |
| condition.request.host.match_type       | string   | 否   | exact_match<br/>safe_regex_match                                                     | 请求域名匹配方式     |
| condition.request.host.value            | string   | 否   | -                                                                                    | 请求域名匹配内容     |
| condition.request.headers[].headerKey   | string   | 否   | -                                                                                    | 请求头匹配名称      |
| condition.request.headers[].match_type  | string   | 否   | exact_match<br/>safe_regex_match                                                     | 请求头匹配匹配方式    |
| condition.request.headers[].value       | string   | 否   | -                                                                                    | 请求头匹配匹配内容    |
| condition.response.code.match_type      | string   | 是   | exact_match<br/>safe_regex_match                                                     | 响应状态码匹配方式    |
| condition.response.code.value           | integer  | 是   | [200, 599]                                                                           | 响应状态码匹配内容    |
| condition.response.headers[].headerKey  | string   | 否   | -                                                                                    | 响应头匹配名称      |
| condition.response.headers[].match_type | string   | 否   | exact_match<br/>safe_regex_match                                                     | 响应头匹配方式      |
| condition.response.headers[].value      | string   | 否   | -                                                                                    | 响应头匹配内容      |
| response.code                           | integer  | 是   | [200, 599]                                                                           | 降级后返回的状态码    |
| response.headers[key]                   | string   | 是   | -                                                                                    | 降级后返回的响应头    |
| response.headers[value]                 | string   | 是   | -                                                                                    | 降级后返回的响应头对应值 |
| response.body                           | string   | 否   | -                                                                                    | 降级后返回的body内容 |


## 前置条件

以下curl命令中存在变量，使用前需要替换为真实环境数据，变量以`{{}}`符号包裹，例如`{{ 网关ID }}`需要根据网关的实际ID进行替换；创建插件命令中`PluginConfiguration`（插件配置）需要根据实际需要进行配置

## 创建

```shell
curl -XPOST -v -H "Content-Type:application/json" -d '{
  "BindingObjectId": {{ 路由ID }},
  "BindingObjectType": "routeRule",
  "GwId": {{ 网关ID }},
  "PluginConfiguration": "{\"condition\":{\"request\":{\"requestSwitch\":true,\"method\":[\"GET\",\"POST\"],\"path\":{\"match_type\":\"exact_match\",\"value\":\"/rootpath/subpath\"},\"headers\":[{\"headerKey\":\"reqHeader\",\"match_type\":\"exact_match\",\"value\":\"reqHeaderValue\"}]},\"response\":{\"code\":{\"match_type\":\"safe_regex_match\",\"value\":\"503\"},\"headers\":[{\"headerKey\":\"rspHeader\",\"match_type\":\"exact_match\",\"value\":\"rspHeaderValue\"}]}},\"kind\":\"static-downgrade\",\"response\":{\"headers\":{\"downgradeHeader\":\"downgradeHeaderValue\"},\"code\":\"200\",\"body\":\"Test Response Context\"}}",
  "PluginType": "static-downgrade"
}' http://{{ hango-portal ip:port }}/gdashboard?Action=BindingPlugin&Version=2019-09-01
```

## 测试

```shell
## 基于如下基本的curl命令，添加插件中配置的请求头、响应头等降级条件，测试是否返回配置的响应内容（响应码、响应头和响应体）
curl -v "http://{{ 网关IP }}/{{ 路由path }}" -H "host:{{ 网关关联域名 }}"

## 例如，插件中配置了降级条件配置了一个响应头为"reqHeader: reqHeaderValue"，则需要构造如下请求进行测试
curl -v "http://{{ 网关IP }}/{{ 路由path }}" -H "host:{{ 网关关联域名 }}" -H "reqHeader:reqHeaderValue"
```

## 删除

```shell
curl -v -H "Content-Type:application/json" http://{{ hango-portal ip:port }}/gdashboard?PluginBindingInfoId={{ 插件ID }}&Action=UnbindingPlugin&Version=2019-09-01
```

## 界面配置方法

[插件界面配置方法引导](plugin-configuring-guide.md)