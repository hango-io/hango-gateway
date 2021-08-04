# Installation

## Installing on Kubernetes

We use helm to install gateway on kubernetes. If you do not have a kubernetes, you can start with [minikube start](https://minikube.sigs.k8s.io/docs/start/)

Kubernetes Version >=1.17

### Install with Helm

1.Install slime-plugin and istio operator

```shell
cd istio-install
./install.sh
```

2.Verifiy slime-plugin and istio alreay running

```shell
$ kubectl -n mesh-operator get pod
NAME                          READY   STATUS    RESTARTS   AGE
slime-boot-66fcdfdc9b-bwwhc   1/1     Running   0          88s

$ kubectl -n istio-operator get pod
NAME                              READY   STATUS    RESTARTS   AGE
istio-operator-685566f48c-d8k9r   1/1     Running   0          88s
```

3.Add Hango Gateway to the list of known chart repositories, as well as prepare the installation namespace:

```shell
helm repo add hango https://github.com/repo/hango/hango-helm
helm repo update
```

4.Install hango gateway with default value use the following commands:

```shell
helm install --namespace hango-system --name hango-gateway ./helm/hango-gateway/ 
```

5.Verify installation

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

6.Un-install

```shell
helm ls --all --short | xargs -L1 helm delete --purge

./istioctl x uninstall --purge
```

## Installing on Docker

Planing...

## Installing on VMs

Planing...
