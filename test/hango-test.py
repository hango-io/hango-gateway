# -*- coding: utf-8 -*-
import requests
import json
import time
import const
import commands

const.PORTAL = commands.getoutput("kubectl get svc -n hango-system  | grep hango-portal | awk '{print $3}'")
const.APP = "istio-e2e-app.hango-system.svc.cluster.local"
const.GW = commands.getoutput("kubectl get svc -n hango-system  | grep hango-proxy | awk '{print $3}'")

def get_gw():
    url = "http://" + const.PORTAL + \
        "/gdashboard?Action=DescribeGatewayList&Version=2018-08-09"
    r = requests.get(url)
    if(200 == r.status_code):
        gws = json.loads(r.text)["GatewayInfos"]
        gw_id = gws[0].get("GwId")
        return gw_id


def create_service():
    url = "http://" + const.PORTAL + \
        "/gdashboard?Action=CreateService&Version=2018-08-09"
    data = ''' 
   {
      "ServiceType":"http",
      "ServiceName":"hango-test",
      "ServiceTag":"hango-test",
      "Contacts":"admin"
   }
   '''
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=data, headers=headers)
    if(200 == r.status_code):
        print("create service ok")
        service_id = json.loads(r.text)["Result"]
        print('service_id:' + str(service_id))
        return service_id
    else:
        print("create service error")
        print('error info: ' + r.text)


def create_route(service_id):
    url = "http://" + const.PORTAL + \
        "/gdashboard/envoy?Action=CreateRouteRule&Version=2019-09-01"
    data = {
        "RouteRuleName": "hango-route-unit",
        "Uri": {
            "Type": "prefix",
            "Value": [
                "/hango/unit"
            ]
        },
        "Priority": 50,
        "ServiceId": service_id
    }

    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if(201 == r.status_code):
        print("create route ok")
        route_id = json.loads(r.text)["RouteRuleId"]
        print('RouteRuleId:' + str(route_id))
        return route_id
    else:
        print("create route error")
        print('error info: ' + r.text)


def publish_service(service_id, gw_id):
    url = "http://" + const.PORTAL + \
        "/gdashboard/envoy?Action=PublishService&Version=2019-09-01"
    data = {
        "GwId": gw_id,
        "ServiceId": service_id,
        "PublishType": "DYNAMIC",
        "BackendService": const.APP,
        "PublishProtocol": "http",
        "RegistryCenterType": "Kubernetes",
    }

    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if(200 == r.status_code):
        print("publish service ok")
    else:
        print("publish service error")
        print('error info: ' + r.text)


def publish_route(route_id, service_id, gw_id):
    url = "http://" + const.PORTAL + \
        "/gdashboard/envoy?Action=PublishRouteRule&Version=2019-09-01"
    data = {
        "GwId": gw_id,
        "RouteRuleId": route_id,
        "DestinationServices": [
            {
                "Port": "80",
                "Weight": 100,
                "ServiceId": service_id
            }
        ]
    }
#    data = data = {"GwId":1,"EnableState":"enable","Timeout":"60000","DestinationServices":[{"BackendService":"wewef","Weight":100,"ServiceId":1}],"ServiceId":1,"RouteRuleId":22}

    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if(200 == r.status_code):
        print("publish route ok")
    else:
        print("publish route error")
        print('error info: ' + r.text)


def offline_route(route_id, gw_id):
    url = "http://" + const.PORTAL + \
        "/gdashboard/envoy?Action=DeletePublishedRouteRule&Version=2019-09-01"
    PARAMS = {'RouteRuleId': route_id, 'GwId': gw_id}
    r = requests.get(url, params=PARAMS)
    if(200 == r.status_code):
        print("offline route ok")
    else:
        print("offline route error")
        print('error info: ' + r.text)


def offline_service(service_id, gw_id):
    url = "http://" + const.PORTAL + \
        "/gdashboard/envoy?Action=DeleteServiceProxy&Version=2019-09-01"
    PARAMS = {'ServiceId': service_id, 'GwId': gw_id}
    r = requests.get(url, params=PARAMS)
    if(200 == r.status_code):
        print("offline service ok")
    else:
        print("offline service error")
        print('error info: ' + r.text)


def delete_route(route_id):
    url = "http://" + const.PORTAL + \
        "/gdashboard/envoy?Action=DeleteRouteRule&Version=2019-09-01"
    PARAMS = {'RouteRuleId': route_id}
    r = requests.get(url, params=PARAMS)
    if(200 == r.status_code):
        print("delete route ok")
    else:
        print("delete route error")
        print('error info: ' + r.text)


def delete_service(service_id):
    url = "http://" + const.PORTAL + \
        "/gdashboard?Action=DeleteService&Version=2018-08-09"
    PARAMS = {'ServiceId': service_id}
    r = requests.get(url, params=PARAMS)
    if(200 == r.status_code):
        print("delete service ok")
    else:
        print("delete service error")
        print('error info: ' + r.text)


def bind_plugin(rout_id, gw_id, plugin_type, plugin_conf):
    url = "http://" + const.PORTAL + \
        "/gdashboard/envoy?Action=BindingPlugin&Version=2019-09-01"
    data = {
        "BindingObjectId": rout_id,
        "BindingObjectType": "routeRule",
        "GwId": gw_id,
        "PluginConfiguration": plugin_conf,
        "PluginType": plugin_type
    }

    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if(200 == r.status_code):
        print("bingding plugin  " + plugin_type + "  -------------ok")


def invoke_gw(add_headers=None):
    url = "http://" + const.GW + "/hango/unit"
    HEADERS = {'host': 'istio.com'}
    if add_headers is not None:
        HEADERS = HEADERS.copy()
        HEADERS.update(add_headers)
    r = requests.get(url, headers=HEADERS)
    return r.status_code


gw_id = get_gw()

service_id = create_service()
route_id = create_route(service_id)
publish_service(service_id, gw_id)
publish_route(route_id, service_id, gw_id)

# 首次调用，sleep 5s, 配置加载
time.sleep(5)
if(200 == invoke_gw()):
    print("invode_gw OK---------------/hango/unit")

# ip 黑白名单测试
ip_res = "{\"type\":\"0\",\"list\":[\"127.0.0.1\"],\"kind\":\"ip-restriction\"}"
bind_plugin(route_id, gw_id, "ip-restriction", ip_res)
ip_local = {'x-hango-real-ip': '127.0.0.1'}
time.sleep(2)
if(403 == invoke_gw(ip_local)):
    print("invode_gw ip-restriction plugin ok---------------ip-restriction")

# 本地限流测试，local-limiting
local_limit = "{\"limit_by_list\":[{\"headers\":[],\"minute\":5}],\"kind\":\"local-limiting\",\"name\":\"local-limiting\"}"
bind_plugin(route_id, gw_id, "local-limiting", local_limit)

for i in range(50):
    if(429 == invoke_gw()):
        print("invode_gw local-limit plugin ok---------------local-limit")
        break

# UA黑白名单，ua-restriction
ua_restriction = "{\"kind\":\"ua-restriction\",\"type\":\"lua\",\"config\":{\"allowlist\":[],\"denylist\":[\"bot\"]}}"
bind_plugin(route_id, gw_id, "ua-restriction", ua_restriction)
time.sleep(2)
ua_local = {'User-Agent': 'bot'}
if(403 == invoke_gw(ua_local)):
    print("invode_gw ua-restriction plugin ok---------------ua-restriction")

offline_route(route_id, gw_id)
offline_service(service_id, gw_id)
delete_route(route_id)
delete_service(service_id)
