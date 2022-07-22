HANGO_NAMESPACE=hango-system
HANGO_PORTAL=`kubectl get svc -n $HANGO_NAMESPACE  | grep hango-portal | awk '{print $3}'`
HANGO_API_PLANE=`kubectl get svc -n $HANGO_NAMESPACE  | grep hango-api-plane | awk '{print $3}'`
HANGO_PROXY=`kubectl get svc -n $HANGO_NAMESPACE  | grep hango-proxy | awk '{print $3}'`
result=$(curl -s -w "%{http_code}" -o /dev/null -X POST "http://${HANGO_PORTAL}:80/gdashboard?Action=CreateGateway&Version=2018-08-09" \
-H 'Content-Type: application/json'  \
-H "x-auth-accountId:admin" \
-H "x-auth-tenantId: 1" \
-H "x-auth-projectId: 1" \
-d '{
    "GwName":"hango_envoy_gateway",
    "ApiPlaneAddr":"http://'"$HANGO_API_PLANE"':10880",
    "GwClusterName":"demo-istio",
    "GwAddr":"http://'"$HANGO_PROXY"'",
    "GwType":"envoy",
    "HostList": [
        "istio.com"
    ]
}')