./istioctl operator init --watchedNamespaces=hango-system

kubectl create ns hango-system
kubectl create ns mesh-operator

kubectl apply -f https://raw.githubusercontent.com/slime-io/slime/v0.1/install/init/crds.yaml
kubectl apply -f https://raw.githubusercontent.com/slime-io/slime/v0.1/install/init/slime-boot-install.yaml
