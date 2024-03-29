# RoadMap

## 介绍

本文可以作为Hango用户和贡献者了解项目方向的参考

## 如何加入RoadMap

* 可以通过issue提Feature的形式与我们进行讨论，如果功能被接受，我们会将对应的issue加入后续的规划
* 如果对我们的规划有计划，可以通过issue进行评论，我们会将对应的issue分配给您

## Hango 迭代版本计划

### v1.3.0（融合网关）
> 已发布

* 支持虚拟网关形态，基于不同功能需求创建不同类型虚拟网关
* 支持纳管预览用户Gateway API，支持多类插件增强

### v1.4.0（模型变更）
> 已发布

* 模型优化，取消服务路由元数据
* 新增域名管理界面，用于集中式管理虚拟网关域名
* 新增TLS证书管理
* 支持单向HTTPS

### v1.5.0（Ingress）
> 已发布

* 支持K8S Ingress流量治理

### v1.6.0（插件市场）
> 已发布

* 支持插件市场能力
* 支持Lua语言自定义插件接入插件市场

### v1.6.1（7层负载功能）
> 已发布

* 支持网关向upstream传客户端IP
* 支持服务温暖上线
* 支持基于Cookie会话保持方式