# 安装

## 前置条件

目前版本支持基于Kubernetes进行安装，如果没有Kubernetes环境，可以采用[minikube](https://minikube.sigs.k8s.io/docs/start/) 进行安装。对于Kubernetes的版本，我们要求版本至少是1.17 版本。

### Helm 安装

1、安装slime-plugin 和 istio operator
默认提供系统os支持为linux

```shell
cd istio-install
./install.sh
```

如果用户使用其他os，可以通过以下命令，下载平台相关的istioctl即可。

```shell
curl -L https://istio.io/downloadIstio | sh -
```

2、验证slime和istio operator的运行状态，确保STATUS显示为Running状态

```shell
$ kubectl -n mesh-operator get pod
NAME                          READY   STATUS    RESTARTS   AGE
slime-boot-66fcdfdc9b-bwwhc   1/1     Running   0          88s

$ kubectl -n istio-operator get pod
NAME                              READY   STATUS    RESTARTS   AGE
istio-operator-685566f48c-d8k9r   1/1     Running   0          88s
```

3、安装hango gateway

提供通过helm方式安装hango gateway, 你需要首先安装[Helm](https://helm.sh/zh/docs/intro/install/), 如果已安装helm，直接通过helm install进行安装即可。

```shell
进入hango/install目录执行
helm install --namespace hango-system --name hango-gateway ./helm/hango-gateway/ 
```

如果你的Helm版本是3.x，执行
```shell
进入hango/install目录执行
helm install --namespace hango-system hango-gateway ./helm/hango-gateway/ 
```

4、确认hango网关运行状态

```shell
$ kubectl get pods -n hango-system
NAME                               READY   STATUS    RESTARTS   AGE
gateway-proxy-7756966795-bd8qp     1/1     Running   0          61s
hango-api-plane-5b58699494-8ngwv   1/1     Running   0          61s
hango-portal-8df74744b-mf6lr       1/1     Running   0          43s
hango-ui-d68d97c97-tp2zf           1/1     Running   0          61s
istio-e2e-app-6b954b4bb5-mmf87     1/1     Running   0          61s
istiod-68dd858bff-qs695            1/1     Running   0          56s
plugin-cb485b49b-c9nrt             1/1     Running   0          59s
```

5、卸载hango网关

```shell
helm ls --all --short | xargs -L1 helm delete --purge

./istioctl x uninstall --purge
```
