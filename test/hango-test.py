# -*- coding: utf-8 -*-
import requests
import json
import time
import const
import commands
import sys

# 等待测试适配网关新模型版本 v1.4.0
print("Please wait for the test future online...")
sys.exit()

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


def describe_plugin_id(route_id, gw_id, plugin_type):
    url = "http://" + const.PORTAL + \
        "/gdashboard/envoy?Action=DescribeBindingPlugins&Version=2019-09-01"
    PARAMS = {'BindingObjectId': route_id, 'GwId': gw_id, 'BindingObjectType':'routeRule'} 
    r = requests.get(url, params=PARAMS)
    if(200 == r.status_code):
        pls = json.loads(r.text)["PluginBindingList"]
        for pl in pls:
            if pl.get("PluginType") == plugin_type:
                return pl.get("PluginBindingInfoId")

def offline_plugin(plugin_binding_id, plugin_type):
    url = "http://" + const.PORTAL + \
        "/gdashboard/envoy?Action=UnbindingPlugin&Version=2019-09-01"
    PARAMS = {'PluginBindingInfoId': plugin_binding_id}
    r = requests.get(url, params=PARAMS)
    if(200 == r.status_code):
        print("offline plugin " + plugin_type +" ok")

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


def invoke_gw(add_headers=None, add_params=None):
    url = "http://" + const.GW + "/hango/unit"
    HEADERS = {'host': 'istio.com'}
    PARAMS = {}
    if add_headers is not None:
        HEADERS = HEADERS.copy()
        HEADERS.update(add_headers)
    if add_params is not None:
        PARAMS.update(add_params)
    r = requests.get(url, headers=HEADERS, params=PARAMS)
    return r.status_code

def invoke_gw_return_h(add_headers=None):
    url = "http://" + const.GW + "/hango/unit"
    HEADERS = {'host': 'istio.com'}
    if add_headers is not None:
        HEADERS = HEADERS.copy()
        HEADERS.update(add_headers)
    r = requests.get(url, headers=HEADERS)
    return r.headers


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

# offline locallimit
offline_plugin(describe_plugin_id(route_id, gw_id, "local-limiting"), "local-limiting")
time.sleep(2)

# UA黑白名单，ua-restriction
ua_restriction = "{\"type\": \"0\",\"list\": [{\"match_type\": \"exact_match\",\"value\": [\"bot\"]}],\"kind\": \"ua-restriction\"}"
bind_plugin(route_id, gw_id, "ua-restriction", ua_restriction)
time.sleep(2)
ua_local = {'User-Agent': 'bot'}
if(403 == invoke_gw(ua_local)):
    print("invode_gw ua-restriction plugin ok---------------ua-restriction")

# URI黑白名单，uri-restriction
uri_restriction = "{\"kind\":\"uri-restriction\",\"type\":\"lua\",\"config\":{\"allowlist\":[],\"denylist\":[\"d1\"]}}"
bind_plugin(route_id, gw_id, "uri-restriction", uri_restriction)
time.sleep(2)
uri_params = {'d': 'd1'}
if(403 == invoke_gw(None, uri_params)):
    print("invode_gw uri-restriction plugin ok---------------uri-restriction")

# Header黑白名单，header-restriction
header_restriction = "{\"type\":\"0\",\"list\":[{\"header\":\"header_test\",\"match_type\":\"exact_match\",\"value\":[\"black\"]}],\"kind\":\"header-restriction\"}"
bind_plugin(route_id, gw_id, "header-restriction", header_restriction)
time.sleep(2)
header_local = {'header_test': 'black'}
if(403 == invoke_gw(header_local)):
    print("invode_gw header-restriction plugin ok---------------header-restriction")

# 百分比限流测试，percent-limit
percent_limit = "{\"limit_percent\":50,\"kind\":\"percent-limit\",\"name\":\"percent-limit\"}"
bind_plugin(route_id, gw_id, "percent-limit", percent_limit)

for i in range(50):
    if(429 == invoke_gw()):
        print("invode_gw percent-limit plugin ok---------------percent-limit")
        break

# offline percentlimit
offline_plugin(describe_plugin_id(route_id, gw_id, "percent-limit"), "percent-limit")
time.sleep(2)


# 本地缓存插件， local-cache
local_cache = "{\"condition\":{\"request\":{\"requestSwitch\":false},\"response\":{\"responseSwitch\":true,\"code\":{\"match_type\":\"exact_match\",\"value\":\"200\"},\"headers\":[]}},\"ttl\":{\"local\":{\"default\":\"30000\",\"custom\":[]}},\"kind\":\"local-cache\",\"keyMaker\":{\"excludeHost\":false,\"ignoreCase\":true,\"queryString\":[],\"headers\":[]}}"
bind_plugin(route_id, gw_id, "local-cache", local_cache)
time.sleep(2)
for i in range(50):
    r_headers = invoke_gw_return_h()
    if "HIT" == r_headers.get("x-cache-status"):
        print("invode_gw local-cache plugin ok---------------local-cache")
        break

offline_route(route_id, gw_id)
offline_service(service_id, gw_id)
delete_route(route_id)
delete_service(service_id)

