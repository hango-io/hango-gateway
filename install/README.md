# Installation

## Installing on Kubernetes

We use helm to install gateway on kubernetes. If you do not have a kubernetes, you can start with [minikube start](https://minikube.sigs.k8s.io/docs/start/)

Kubernetes Version >=1.17

### Install with Shell

1. Go to the "hango-gateway/install" directory. The directory structure tree is as follows
```xml
install
install
├─common
├─crds
├─helm
├─init-hango
├─install.sh
├─check.sh
└─uninstall.sh
```
2. You will see three scripts for install (install.sh), check status (check.sh), and uninstall (uninstall.sh) respectively. You can directly execute the command

Note: Make sure you have sufficient permissions before executing the script
```shell
sh install.sh
```
3. After the script is executed, run the following command to verify the running status of the Hango gateway
```shell
sh check.sh
```
The normal running status is as follows. If the container is not ready now, wait for a while and check it again
```shell
[install-check][14:50:49]
========= pods in namespace[hango-system] show below =========
NAME                               READY   STATUS    RESTARTS   AGE
gateway-proxy-55887cb579-mv9xh     1/1     Running   0          87s
hango-api-plane-6c4554cfc4-ndnx5   1/1     Running   0          101s
hango-portal-597bb489d6-45b2r      1/1     Running   0          101s
hango-ui-75458cc7dc-b4x6b          1/1     Running   0          101s
istio-e2e-app-85bb49bf75-t7slt     1/1     Running   0          101s
hango-istiod-697b5c4456-67l92      1/1     Running   0          95s
slime-75fcb44f68-w9x4x             1/1     Running   0          94s
```

### The other way to install Hango gateway
1. Please configure K8S resources of Hango gateway by referring to the script content

### Uninstall with Shell
1. Go to "hango-gateway/install" directory
2. Run the script to uninstall hango gateway

Note: Make sure you have sufficient permissions before executing the script
```shell
sh uninstall.sh
```
3. After the script is executed, run the following command to check the running status of the Hango gateway
```shell
sh check.sh
```
After the uninstallation is complete, the namespaces and all containers under them will be deleted. If k8s resources still exist, you can try uninstall.sh script again or manually delete the resources
```shell
[install-check][14:56:29]
========= pods in namespace[hango-system] show below =========
No resources found in hango-system namespace.
```

## Installing on Docker

Planing...

## Installing on VMs

Planing...
