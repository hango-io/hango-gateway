# 安装Hango

## 前置条件

目前版本支持基于Kubernetes进行安装，如果没有Kubernetes环境，可以采用[minikube](https://minikube.sigs.k8s.io/docs/start/) 进行安装。对于Kubernetes的版本，我们要求版本至少是1.17 版本。

### Helm 安装

1、安装slime-plugin 和 istio operator

```shell
cd istio-install
./install.sh
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

3、获取hango网关helm chart安装包

```shell
helm repo add hango https://github.com/repo/hango/hango-helm
helm repo update
```

4、安装hango gateway

```shell
helm install --namespace hango-system --name hango-gateway ./helm/hango-gateway/ 
```

5、确认hango网关运行状态

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

6、卸载hango网关

```shell
helm ls --all --short | xargs -L1 helm delete --purge

./istioctl x uninstall --purge
```
