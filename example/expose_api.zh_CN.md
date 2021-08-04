# Hango 网关路由

通过接口创建服务，路由，同时进行服务和路由发布，便捷使用Hango网关。

## 创建服务

通过创建服务接口，创建服务，例如，创建一个名为hango-test的服务。

```shell
curl "http://hango.io.portal.org/gdashboard/envoy?Action=CreateService&Version=2019-09-01" \
-H 'Content-Type: application/json' \
-d '{
    "ServiceType":"http",
    "ServiceName":"hango-test",
    "ServiceTag":"hango-test",
    "Contacts":"admin"
    }'
```

## 创建路由

通过api创建路由，路由从属于服务；例如创建一个前缀为/hango/unit的路由，hango-route-test。

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

## 发布服务

声明注册类型以及后端应用进行服务发布，例如，在k8s注册中心中发布服务至应用istio-e2e-app.hango-system.svc.cluster.local。

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

## 发布路由

通过声明服务端口进行路由发布，一旦路由发布成功，就可以通过hango网关调用路由。例如，发布路由至服务80端口。

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

## 验证路由

可以通过curl指令验证路由是否成功。

```shell
curl "http://hango.io.proxy/hango/unit" -H "host:istio.com"
```

返回

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

## 下线、删除路由

调用api进行路由下线及删除，例如：

```shell
curl "http://hango.io.portal.org/gdashboard/envoy?Action=DeletePublishedRouteRule&Version=2019-09-01&RouteRuleId={route_id}&GwId={gw_id}"

curl "http://hango.io.portal.org/gdashboard/envoy?Action=DeleteRouteRule&Version=2019-09-01&RouteRuleId={route_id}"
```

## 下线、删除服务

调用api进行服务下线及删除，例如：

```shell
curl "http://hango.io.portal.org/gdashboard/envoy?Action=DeleteServiceProxy&Version=2019-09-01&ServiceId={service_id}&GwId={gw_id}"

curl "http://hango.io.portal.org/gdashboard/envoy?Action=DeleteService&Version=2019-09-01&ServiceId={service_id}"
```
