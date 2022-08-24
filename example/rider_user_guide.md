# Hango Gateway Custom Plug-in Use Tutorial

## 一、Requirement

Implement an uri black and white list plug-in. Support console configuration uri blacklist/whitelist.

## 二、Write plug-ins and debug them

### 2.1 The development of rider

Rider is an open source custom plug-in package of the hango team. It dynamically expands custom plug-ins through the combination of rider and envoy's hot-loading capabilities.

（1）2.1.1 Set up the plugins/uri-restriction.lua file under the Rider root to store the plug-in code

Create plugins/uri-restriction.lua and add the following code.

It consists of two parts: plug-in schema configuration and plug-in execution logic configuration; Schema configuration can be divided into base_json_schema global configuration and route_json_schema routing configuration. Global configuration is used to configure the common configuration of the plug-in, such as the global configuration of external authentication services; Routing configuration is the core configuration of the plug-in, and most scenarios only need to write route_json_schema.

The plug-in executes logic and relies on the SDK encapsulated by Rider to develop the corresponding plug-in link. If the characters in the request URI match the black-and-white list rule, the request is allowed. If the characters in the request URI do not match the black-and-white list rule and match the black-and-white list rule, the 403 error code and the corresponding "Forbidden" is returned

```lua
--[[
V2 Rider version was introduced;
Compared with V1, v2 divides request and response into header and body parts to improve plugin performance in different scenarios
-- ]] 
require('rider.v2')

-- Defining local variables
local envoy = envoy
local request = envoy.req
local respond = envoy.respond

-- Define local constants
local NO_MATCH = 0
local MATCH_WHITELIST = 1
local MATCH_BLACKLIST = 2
local BAD_REQUEST = 400
local FORBIDDEN = 403

local uriRestrictionHandler = {}

uriRestrictionHandler.version = 'v2'

local json_validator = require('rider.json_validator')

-- Define the global configuration
local base_json_schema = {
    type = 'object',
    properties = {}
}

-- Define the route configuration
local route_json_schema = {
    type = 'object',
    properties = {
        allowlist = {
            type = 'array',
            items = {
                type = 'string'
            }
        },
        denylist = {
            type = 'array',
            items = {
                type = 'string'
            }
        }
    }
}

json_validator.register_validator(base_json_schema, route_json_schema)

-- Define the local validation URI white-and-black list method
local function checkUriPath(uriPath, allowlist, denylist)
    if allowlist then
        for _, rule in ipairs(allowlist) do
            envoy.logDebug('allowist: compare ' .. rule .. ' and ' .. uriPath)
            if string.find(uriPath, rule) then
                return MATCH_WHITELIST
            end
        end
    end

    if denylist then
        for _, rule in ipairs(denylist) do
            envoy.logDebug('denylist: compare ' .. rule .. ' and ' .. uriPath)
            if string.find(uriPath, rule) then
                return MATCH_BLACKLIST
            end
        end
    end

    return NO_MATCH
end

-- Define the header stage handler for the request
function uriRestrictionHandler:on_request_header()
    local uriPath = request.get_header(':path')
    local config = envoy.get_route_config()

    envoy.logInfo('start lua uriRestriction')
    if uriPath == nil then
        envoy.logErr('no uri path!')
        return
    end

    -- 'nil' indicates that the route configuration does not exist (route plugin is not configured)
    if config == nil then
        return
    end

    local match = checkUriPath(uriPath, config.allowlist, config.denylist)

    envoy.logDebug('on_request_header, uri path: ' .. uriPath .. ', match result: ' .. match)

    if match > 1 then
        envoy.logDebug('path is now allowed: ' .. uriPath)
        return respond({[':status'] = FORBIDDEN}, 'Forbidden')
    end
end

return uriRestrictionHandler
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
            filename: /usr/local/lib/rider/plugins/uri-restriction.lua
        name: uri-restriction.lua
        config: {}
```

Add the corresponding Route configuration, as follows;

```yaml
typed_per_filter_config:
  proxy.filters.http.rider:
    "@type": type.googleapis.com/proxy.filters.http.rider.v3alpha1.RouteFilterConfig
    plugins:
      - name: uri-restriction
        config:
          allowlist:
            - a1
          denylist:
            - d1
```

Execute './scripts/dev/local-up.sh 'to start hango-gateway and a simple HTTP service.

`curl -v http://localhost:8002/static-to-header`

![image-20210416173118827](../images/rider_uri_restriction_test_ok.png)

response: `403 Foebidden`

### 2.3 The development of console schem

Developing the corresponding plug-in schema, the plug-in can be exposed to the gateway console for easy user configuration.

Expose the corresponding uri-restriction plug-in to the Hango console by writing a JSON schema.

According to the requirements, the development of uri-restriction front-end schema is as follows;

```json
{
  "formatter": {
    "kind": "uri-restriction",
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
      "help": "URI优先匹配白名单，命中之后直接放行，支持正则",
      "type": "multi_input",
      "rules": [
      ]
    },
    {
      "key": "denylist",
      "alias": "黑名单",
      "help": "URI优先匹配白名单，没有命中，继续匹配黑名单，命中之后直接禁止，支持正则",
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
  "name": "uri-restriction",
  "displayName": "URI黑白名单",
  "schema": "plugin/route/uri-restriction.json",
  "description": "URI黑白名单插件",
  "processor": "AggregateGatewayPluginProcessor",
  "author": "system",
  "createTime": "1655279630000",
  "updateTime": "1655279630000",
  "pluginScope": "global,routeRule",
  "pluginPriority": "3000",
  "instructionForUse": "URI黑白名单插件",
  "categoryKey": "security",
  "categoryName": "安全"
}
```

(3) Add the uri-restriction.json schema file in the /plugin/route directory

```json
---uri-restriction.json
{
  "formatter": {
    "kind": "uri-restriction",
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
      "help": "URI优先匹配白名单，命中之后直接放行，支持正则",
      "type": "multi_input",
      "rules": [
      ]
    },
    {
      "key": "denylist",
      "alias": "黑名单",
      "help": "URI优先匹配白名单，没有命中，继续匹配黑名单，命中之后直接禁止，支持正则",
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
