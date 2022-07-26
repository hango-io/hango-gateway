# Expose route to hango

For the purpose of this example, you'll create service and route to e2e. Then, publish service and route to hango gateway.
Use hango gateway route to e2e service.

## Add Service

Hango Gateway exposes hango-gateway-portal to users. You can use hango-gateway-portal api to add a service. For example, add a service which name is hango-test.

```shell
curl "http://hango.io.portal.org/gdashboard/envoy?Action=CreateService&Version=2018-08-09" \
-H 'Content-Type: application/json' \
-d '{
    "ServiceType":"http",
    "ServiceName":"hango-test",
    "ServiceTag":"hango-test",
    "Contacts":"admin"
    }'
```

## Add Route

You can use hango-gateway-portal api to add a route. For example, add a route named hango-route-test, and the uri is prefix: /hango/unit

```shell
curl "http://hango.io.portal.org/gdashboard/envoy?Action=CreateRouteRule&Version=2019-09-01" \
-H 'Content-Type: application/json' \
-d '{
    "RouteRuleName":"hango-route-test",
    "Uri":{
        "Type":"prefix",
        "Value":[
            "/hango/unit"
        ]
    },
    "ServiceId": service_id
   }'
```

## Publish Service

You can use hango-gateway-portal api to publish service. You need to declare registry-center-type and backend application. For example, publish hango-test service to istio-e2e-app.hango-system.svc.cluster.local in kubernetes registry.

```shell
curl "http://hango.io.portal.org/gdashboard/envoy?Action=PublishService&Version=2019-09-01" \
-H 'Content-Type: application/json' \
-d '{
    "GwId": gw_id,
    "ServiceId":service_id,
    "PublishType":"DYNAMIC",
    "BackendService": "istio-e2e-app.hango-system.svc.cluster.local",
    "PublishProtocol":"http",
    "RegistryCenterType":"Kubernetes",
}'
```

## Publish Route

You can use hango-gateway-portal api to publish route to hango gateway. Once publish route, you can call the e2e api through hango gateway. You should declare service port for publishing. For example, publish route with 80 port.

```shell
curl "http://hango.io.portal.org/gdashboard/envoy?Action=PublishRouteRule&Version=2019-09-01" \
-H 'Content-Type: application/json' \
-d '{
    "GwId": gw_id,
    "RouteRuleId": route_id,
    "DestinationServices":[
        {
            "Port":"80",
            "Weight":100,
            "ServiceId":service_id
        }
    ],
}'
```

## Verify the Route

You can use curl to verify the route. For example,

```shell
curl "http://hango.io.proxy/hango/unit" -H "host:istio.com"
```

response

```shell
HTTP/1.1 200 OK
date: Thu, 15 Apr 2021 08:53:20 GMT
content-length: 719
content-type: text/plain; charset=utf-8
x-envoy-upstream-service-time: 0
server: istio-envoy

ServiceVersion=v1
ServicePort=80
Host=istio.com
Method=GET
URL=/hango/unit
Proto=HTTP/1.1
........
```

## Offline and Delete Route

You can use hango-gateway-portal api to offline or delete route. For example,

```shell
curl "http://hango.io.portal.org/gdashboard/envoy?Action=DeletePublishedRouteRule&Version=2019-09-01&RouteRuleId={route_id}&GwId={gw_id}"

curl "http://hango.io.portal.org/gdashboard/envoy?Action=DeleteRouteRule&Version=2019-09-01&RouteRuleId={route_id}"
```

## Offline and Delete Service

You can use hango-gateway-portal api to offline or delete service. For example,

```shell
curl "http://hango.io.portal.org/gdashboard/envoy?Action=DeleteServiceProxy&Version=2019-09-01&ServiceId={service_id}&GwId={gw_id}"

curl "http://hango.io.portal.org/gdashboard/envoy?Action=DeleteService&Version=2018-08-09&ServiceId={service_id}"
```
