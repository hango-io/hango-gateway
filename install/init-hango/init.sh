curl -X POST 'http://{{portal addr}}:{{portal port}}/gdashboard/envoy?Action=CreateGateway&Version=2019-09-01' \
 -H 'Content-Type: application/json'  \
-d '{
    "GwName":"hango_envoy_gateway",
    "ApiPlaneAddr":"http://{{api_plane addr}}:{{api_plane port}}",
    "Description":"this is des",
    "GwClusterName":"demo-istio",
    "GwAddr":"http://{{gateway_proxy addr}}",
    "GwType":"envoy",
    "HostList": [
        "istio.com"
       ]
}'
