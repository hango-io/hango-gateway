# 静态降级

## 描述

`static-downgrade`插件可匹配指定的请求进行降级，返回指定的响应内容

## 属性

| 名称                   | 类型     | 必选项 | 默认值  | 描述           |
|----------------------|--------|-----|------|--------------|
| 静态降级条件/请求/是否使用请求进行匹配 | switch | 是   | 否    | 是否使用请求进行匹配   |
| - 静态降级条件/请求/请求方法     | select | 否   | -    | HTTP的请求方法类型  |
| - 静态降级条件/请求/请求路径/匹配方法  | select | 是   | 精确匹配 | 请求路径匹配方式     |
| - 静态降级条件/请求/请求路径/取值    | string | 否   | -    | 请求路径匹配内容     |
| - 静态降级条件/请求/域名/匹配方式    | select | 是   | 精确匹配 | 请求域名匹配方式     |
| - 静态降级条件/请求/域名/取值      | string | 否   | -    | 请求域名匹配内容     |
| - 静态降级条件/请求/请求头/请求头    | string | 否   | -    | 请求头匹配名称      |
| - 静态降级条件/请求/请求头/匹配方式   | select | 是   | 精确匹配 | 请求头匹配匹配方式    |
| - 静态降级条件/请求/请求头/取值     | string | 否   | -    | 请求头匹配匹配内容    |
| 静态降级条件/响应/状态码/匹配方式   | select | 是   | 精确匹配 | 响应状态码匹配方式    |
| 静态降级条件/响应/状态码/取值     | string | 是   | -    | 响应状态码匹配内容    |
| 静态降级条件/响应/响应头/响应头    | string | 否   | -    | 响应头匹配名称      |
| 静态降级条件/响应/响应头/匹配方式   | select | 是   | 精确匹配 | 响应头匹配方式      |
| 静态降级条件/响应/响应头/取值     | string | 否   | -    | 响应头匹配内容      |
| 降级后响应内容/响应状态码        | number | 是   | 200  | 降级后返回的状态码    |
| 降级后响应内容/响应头          | string | 是   | -    | 降级后返回的响应头    |
| 降级后响应内容/响应头值         | string | 是   | -    | 降级后返回的响应头对应值 |
| 降级后响应内容/请求响应内容       | string | 是   | -    | 降级后返回的body内容 |


## 前置条件

以下curl命令中存在变量，使用前需要替换为真实环境数据，变量以`{{}}`符号包裹，例如`{{ 网关ID }}`需要根据网关的实际ID进行替换；创建插件命令中`PluginConfiguration`（插件配置）需要根据实际需要进行配置

## 创建

```shell
curl -XPOST -v -H "Content-Type:application/json" -d '{
  "BindingObjectId": {{ 路由ID }},
  "BindingObjectType": "routeRule",
  "GwId": {{ 网关ID }},
  "PluginConfiguration": "{\"condition\":{\"request\":{\"requestSwitch\":true,\"method\":[\"GET\",\"POST\"],\"path\":{\"match_type\":\"exact_match\",\"value\":\"/rootpath/subpath\"},\"host\":{\"match_type\":\"exact_match\"},\"headers\":[{\"headerKey\":\"reqHeader\",\"match_type\":\"exact_match\",\"value\":\"reqHeaderValue\"}]},\"response\":{\"code\":{\"match_type\":\"safe_regex_match\",\"value\":\"503\"},\"headers\":[{\"headerKey\":\"rspHeader\",\"match_type\":\"exact_match\",\"value\":\"rspHeaderValue\"}]}},\"kind\":\"static-downgrade\",\"response\":{\"headers\":{\"downgradeHeader\":\"downgradeHeaderValue\"},\"code\":\"200\",\"body\":\"Test Response Context\"}}",
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