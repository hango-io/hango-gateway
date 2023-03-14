#!/bin/bash

HANGO_NAMESPACE=hango-system

function init_hango(){
  HANGO_PORTAL=`kubectl get svc -n $HANGO_NAMESPACE  | grep hango-portal | awk '{print $3}'`
  HANGO_API_PLANE=`kubectl get svc -n $HANGO_NAMESPACE  | grep hango-api-plane | awk '{print $3}'`
  HANGO_PROXY=`kubectl get svc -n $HANGO_NAMESPACE  | grep hango-proxy | awk '{print $3}'`
  GW_CLUSTER_NAME="hango-demo-gateway"
  result=$(curl -s -w "%{http_code}" -o /dev/null -X POST "http://${HANGO_PORTAL}:80/gdashboard?Action=CreateGateway&Version=2022-10-30" \
  -H 'Content-Type: application/json'  \
  -H "x-auth-accountId:admin" \
  -H "x-auth-tenantId: 1" \
  -H "x-auth-projectId: 1" \
  -d '{
        "Name":"hango_envoy_gateway",
        "EnvId":"1",
        "SvcType":"NodePort",
        "SvcName":"gateway-proxy",
        "Type":"envoy",
        "ConfAddr":"http://'"$HANGO_API_PLANE"':10880",
        "Description":"Hango网关",
        "GwClusterName":'\"${GW_CLUSTER_NAME}\"'
    }')
  if [[ $result -eq 200 ]]; then
      echo "Init hango success."
  else
      echo -e "\033[31mInit error\033[0m, init_hango can be run independently \n"
      echo -e "============================== Common mistakes ==============================\n"
      echo -e "1.The same gateway has been created, please go to the hango-console to check"
      echo -e "2.hango-portal is unhealthy, please check the hango-portal pod status"
      exit 1
  fi
}

# start init hango
init_hango