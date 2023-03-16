# 插件模板配置说明
可以通过修改配置文件控制插件的展示

## 控制插件开关
  在名为hango-api-plane-config的ConfigMap中找到 ```pluginmanager-template.json```配置，该配置是插件的模板来源，可以通过```enable```调整插件的开关。例如：
 ```yaml
 {
  "enable": "true",
  "name": "envoy.filters.http.fault"
}
 ```
名为```envoy.filters.http.fault```的插件将会被开启。
目前支持的插件有如下：
* proxy.filters.http.metadatahub：插件元数据
* envoy.filters.http.fault：百分比限流
* envoy.filters.http.local_ratelimit：本地限流
* proxy.filters.http.iprestriction：IP黑白名单
* proxy.filters.http.ua_restriction：UA黑白名单
* proxy.filters.http.referer_restriction：Restriction黑白名单
* proxy.filters.http.header_restriction：Header黑白名单
* proxy.filters.http.header_rewrite:响应头重写
* proxy.filters.http.staticdowngrade：静态降级
* proxy.filters.http.circuitbreaker：熔断
* proxy.filters.http.waf：Web应用程序防火墙
* proxy.filters.http.rider：lua扩展
## 控制插件显示
  在名为hango-api-plane-config的ConfigMap中找到```plugin-support-config.json```配置，其功能是配置不同类型的虚拟网关所支持的插件列表展示。```display```设置为```false```的插件将不会再前端页面展示。