# Hango Gateway Custom Plug-in Use Tutorial

## 一、Requirement

Implement a UA black and white list plug-in. Support console configuration UA blacklist/whitelist.

## 二、Write plug-ins and debug them

### 2.1 The development of rider

Rider is an open source custom plug-in package of the hango team. It dynamically expands custom plug-ins through the combination of rider and envoy's hot-loading capabilities.

（1）2.1.1 Set up the plugins/ua-restriction.lua file under the Rider root to store the plug-in code

Create plugins/ua-restriction.lua and add the following code.

It consists of two parts: plug-in schema configuration and plug-in execution logic configuration; Schema configuration can be divided into base_json_schema global configuration and route_json_schema routing configuration. Global configuration is used to configure the common configuration of the plug-in, such as the global configuration of external authentication services; Routing configuration is the core configuration of the plug-in, and most scenarios only need to write route_json_schema.

The plug-in executes logic and relies on the SDK encapsulated by Rider to develop the corresponding plug-in link. If no User-Agent header exists, then 400 is returned. "User-Agent not found". If no User-Agent header exists, then 400 is returned. Return 403 "Forbidden" if match uA blacklist.

```lua
require("rider")
local envoy = envoy
local get_req_header = envoy.req.get_header
local ipairs = ipairs
local re_find = string.find
local respond = envoy.respond
local logDebug = envoy.logDebug

local uaRestrictionHandler = {}

local BAD_REQUEST = 400
local FORBIDDEN = 403

local MATCH_EMPTY     = 0
local MATCH_WHITELIST = 1
local MATCH_BLACKLIST = 2

local json_validator = require("rider.json_validator")

local base_json_schema = {
    type = 'object',
    properties = {},
}

local route_json_schema = {
    type = 'object',
    properties = {
      allowlist = {
        type = 'array',
        items = {
          type = 'string',
        },
      },
      denylist = {
        type = 'array',
        items = {
          type = 'string',
        },
      },
    },
}
json_validator.register_validator(base_json_schema, route_json_schema)

--- strips whitespace from a string.
local function strip(str)
  if str == nil then
    return ""
  end
  str = tostring(str)
  if #str > 200 then
    return str:gsub("^%s+", ""):reverse():gsub("^%s+", ""):reverse()
  else
    return str:match("^%s*(.-)%s*$")
  end
end

local function get_user_agent()
  return get_req_header("user-agent")
end

local function examine_agent(user_agent, allowlist, denylist)
  user_agent = strip(user_agent)

  if allowlist then
    for _, rule in ipairs(allowlist) do
      logDebug("allowist: compare "..rule.." and "..user_agent)
      if re_find(user_agent, rule) then
        return MATCH_WHITELIST
      end
    end
  end

  if denylist then
    for _, rule in ipairs(denylist) do
      logDebug("denylist: compare "..rule.." and "..user_agent)
      if re_find(user_agent, rule) then
        return MATCH_BLACKLIST
      end
    end
  end

  return MATCH_EMPTY
end

function uaRestrictionHandler:on_request()
  local config = envoy.get_route_config()
  if config == nil then
    return
  end

  logDebug("Checking user-agent");

  local user_agent = get_user_agent()
  if user_agent == nil then
    return respond({[":status"] = BAD_REQUEST}, "user-agent not found")
  end

  local match  = examine_agent(user_agent, config.allowlist, config.denylist)

  if match > 1 then
    logDebug("UA is now allowed: "..user_agent);
    return respond({[":status"] = FORBIDDEN}, "Forbidden")
  end
end

return uaRestrictionHandler

```

### 2.2 The debugging of rider

Update the script/dev/envoy.yaml file to add the corresponding http_filter configuration as follows;

```yaml
- name: proxy.filters.http.rider
    typed_config:
      "@type": type.googleapis.com/proxy.filters.http.rider.v3alpha1.FilterConfig
      plugin:
        vm_config:
          package_path: "/usr/local/lib/rider/?/init.lua;/usr/local/lib/rider/?.lua;"
        code:
          local:
            filename: /usr/local/lib/rider/plugins/ua-restriction.lua
        name: ua-restriction
        config: {}
```

Add the corresponding Route configuration, as follows;

```yaml
typed_per_filter_config:
  proxy.filters.http.rider:
    "@type": type.googleapis.com/proxy.filters.http.rider.v3alpha1.RouteFilterConfig
    plugins:
      # Plugin config here applies to the Route
      - name: ua-restriction
        config:
          denylist:
          - bot
```

Execute './scripts/dev/local-up.sh 'to start hango-gateway and a simple HTTP service.

`curl -v http://localhost:8000/anything -H 'User-Agent:bot'`

![image-20210416173118827](../images/rider_ok.png)

response: `403 Foebidden`

### 2.3 The development of console schem

Developing the corresponding plug-in schema, the plug-in can be exposed to the gateway console for easy user configuration.

Expose the corresponding UA-restriction plug-in to the Hango console by writing a JSON schema.

According to the requirements, the development of UA-restriction front-end schema is as follows;

```json
{
  "formatter": {
    "kind": "ua-restriction",
    "type": "lua",
    "config": {
      "allowlist": "&allowlist",
      "denylist": "&denylist"
    }
  },
  "layouts": [
    {
      "key": "allowlist",
      "alias": "白名单",
      "help": "User-Agent matches the whitelist first, and releases it directly after hitting",
      "type": "multi_input",
      "rules": [
      ]
    },
    {
      "key": "denylist",
      "alias": "黑名单",
      "help": "User-Agent matches the whitelist first, if it fails to hit, it will continue to match the blacklist, and if hit, it will be banned directly",
      "type": "multi_input",
      "rules": [
      ]
    }
  ]
}
```

## 三、Integrate plug-ins into Hango

### 3.1 Integrate plug-in to hango-envoy

（1）In the rider directory, execute

```yaml
kubectl create configmap hango-rider-plugin --from-file=plugins/ -n hango-system
```

（2）Wait for about 10 seconds, and load the corresponding plugins into hango-gateway

### 3.2 Integrate plug-in to api-palne

（1）Clarify the level of the plugin

The hango gateway custom plug-in supports two levels: the global level and the routing level; the global level is the entire gateway level, and the effective order is the priority routing level plug-in to take effect.

The global configuration entry is: [Plugin Management] -> [Add Global Plug-in]. After configuring a global plug-in, all routes of the gateway are effective.

The routing level configuration entry is: [Released information] -> [Released routing] -> [Plugins] -> [Add global plugins]. After configuring a route-level plug-in, it will only take effect for the current route.

（2）Update the plugin-config.json in the api-plane project /plugin/route directory to add the corresponding plug-in declaration

```json
{
    "name": "ua-restriction",
    "displayName": "UA黑白名单", 
    "schema": "plugin/route/ua-restriction.json",
    "description": "UA黑白名单插件",
    "processor": "AggregateGatewayPluginProcessor",
    "author": "system",
    "createTime": "1572537600000",
    "updateTime": "1572537600000",
    "pluginScope": "global,routeRule",   
    "instructionForUse": "UA黑白名单插件",
    "categoryKey": "security",  
    "categoryName": "安全"
```

(3) Add the ua-detection.json schema file in the /plugin/route directory

```json
---ua-restriction.json
{
  "formatter": {
    "kind": "ua-restriction",
    "type": "lua",
    "config": {
      "allowlist": "&allowlist",
      "denylist": "&denylist"
    }
  },
  "layouts": [
    {
      "key": "allowlist",
      "alias": "白名单",
      "help": "User-Agent matches the whitelist first, and releases directly after the hit, and supports regular",
      "type": "multi_input",
      "rules": [
      ]
    },
    {
      "key": "denylist",
      "alias": "黑名单",
      "help": "User-Agent matches the whitelist first, if no hits, continue to match the blacklist, directly banned after hits, support regular",
      "type": "multi_input",
      "rules": [
      ]
    }
  ]
}
```

(4) Execute the following instructions to generate the corresponding plug-in configmap.

```shell
kubectl create configmap hango-plugin --from-file=plugin/route/ -n hango-system
```

(5) Wait for about 10s, after the configmap is loaded successfully, you can use the custom plug-in.
