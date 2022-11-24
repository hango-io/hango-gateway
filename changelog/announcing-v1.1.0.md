### 描述
本次更新是Hango正式版v1.1.0的发布。基于v1.0.0版本集成了eureka、nacos注册中心支持、waf插件、流量染色等特性

### 新功能

- 支持对接eureka和nacos注册中心发现服务
  
  https://github.com/hango-io/portal/pull/9

  https://github.com/hango-io/api-plane/pull/10

- 支持k8s服务流量染色功能

  https://github.com/hango-io/hango-gateway/pull/45

- 支持waf插件

  https://github.com/hango-io/hango-gateway/pull/45


### 工程增强

- Slime模块聚合服务发现功能，CRD支持k8s 1.22+版本
  
  https://github.com/hango-io/hango-gateway/pull/40

- istiod CRD支持k8s 1.22+版本
  
  https://github.com/hango-io/hango-gateway/pull/43

- hango-portal 与 hango-api-plane SpringBoot升级至2.5.14版本

  https://github.com/hango-io/api-plane/pull/11