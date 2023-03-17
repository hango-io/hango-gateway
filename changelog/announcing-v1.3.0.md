### 描述
本次更新是Hango正式版v1.3.0的发布。基于v1.2.0版本更新了融合网关能力，支持k8s的Gateway API纳管等能力

### 新功能

- [支持虚拟网关形态，基于不同功能需求创建不同类型虚拟网关](https://github.com/hango-io/portal/commit/eb61aa8d097fe59cee407f9e7afe1ca388853c60)

- [支持纳管预览用户Gateway API，支持多类插件增强](https://github.com/hango-io/api-plane/commit/c53574e9dbfc89ae0e4c8f50da366a8de5af9451)


### 工程增强

- [portal模块分为`common-infra`和`envoy-infra`，基于切面形式进行增强回调](https://github.com/hango-io/portal/commit/eb61aa8d097fe59cee407f9e7afe1ca388853c60)