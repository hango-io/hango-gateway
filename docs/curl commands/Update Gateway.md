#Update Gateway  By CURL Commands

### Update API-Plane and Envoy proxy address. 
curl -v -H "Content-Type:aplication/json" -d '{
  "Gwid":1,
  "ApiPlaneAddr": "http://api-plane-sm.qa-ci.service.163.org",
  "Description": "Hango gateway test.",
  "GatewayConfigInfo": {
    "AuthAddr": "",
    "EnvId": "prod",
    "AuditDatasourceSwitch": "",
    "AuditDbConfig": ""
  },
  "GwAddr": "http://gateway-proxy.qa-ci.service.163.org",
  "GwClusterName": "prod-gateway",
  "GwName": "hango_envoy_gateway",
  "GwType": "envoy",
  "ProjectIds": [
    0,
    1,
    3
  ]
}' http://apigw-gportal-envoy.qa-ci.service.163.org/gdashboard?Action=UpdateGateway&Version=2018-08-09