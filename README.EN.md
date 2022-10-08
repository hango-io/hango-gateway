[//]: # "README"

# Hango Gateway

![hango](images/logo.jpg)

[中文参考](README.md)

Hango is a high-performance, scalable, and feature-rich cloud native API gateway built on Envoy.

Hango provides functions such as request proxy, dynamic routing, load balancing, current limiting, fuse, health check, security protection, etc. It can be used in application scenarios such as microservice gateways, seven-layer load balancing, Kubernetes Ingress, and Serverless gateways.

Through the Hango Rider module, users can customize multi-language plugins for capability expansion.

## Documentation

[Blog](https://hango-io.github.io/): introducing Hango
[QuickStart](https://github.com/hango-io/hango-gateway/blob/master/example/expose_api_with_ui.zh_CN.md)
[RoadMap](changelog/RoadMap%202022.md)

## Summary

[Why Hango](#why-hango)

[Features](#features)

[Architecture](#architecture)

[Projects](#projects)

[Installation](#installation)

[Usage](#usage)

[Community](#community)

[License](#license)

## Why-Hango

As a hign performance gateway, hango can provide load balancing, rate-limiting, circuit-breaker, logging, downgrade, and more through plugins. Using hango, you will not implement the common module in your businness software.

**Why Hango?**

* **Technical route**: Build on leading edge/middle/service proxy **Envoy**,  with abundant functions, excellent  performance and complete observability.

* **Extensibility**:  Enhanced Lua **Rider** extensible plugin; multi-language extensible plugin base on **WebAssembly** (Alpha, follow-up to provide)

* **Multi-scenario**: Used as API Gateway, Kubernetes Ingress, L7 Load balencer, Serveless gateway in the complex scenarios.

* **Cloud Native**: Worked as implements of Kubernetes Ingress or Service Mesh Gateway with natural compatibility.

* **API ecology & integration**:  API ecology governance and hundreds of industrial protocol integration.

* **Control usability**:  Easy-to-use control console to manage gateways, services, routes, etc.

## Features

* Enable HTTP, gRPC, Websocket and other multi-protocol proxy

* Support Kubernetes, virtual services and other forms of service discovery

* L7 traffic proxy, connection pool configuration

* Dynamic routing based on request parameters, active and passive health check strategies, and rich load balancing algorithms

* Multi-scenario flow management functions such as current limiting, fusing, downgrade, and retry

* Security protection functions such as black and white list control, authentication and authentication

* Visual console for gateway configuration management

* Thanks to Envoy's excellent performance, single instance performance can reach more than 10w TPS

* Custom plug-in framework, support users to develop custom plug-ins in multiple languages. Refer to [Rider User Guide](./example/rider_user_guide.md)

## Architecture

Hango is built based on the concept of cloud native, the data plane is extended based on Envoy, the plug-in chain is enhanced, and the Rider module is provided for custom plug-in extensions; the control plane components include Slime, Istio, API Plane and Portal modules.

Thanks to slime module, you can choose the latest stable istio as the xds-server to data-plane.

![architecture](images/architecture.png)

## Projects

Hango Gateway is a cloud-native architecture solution, we have six micro-service projects.
This package is a meta-package aggregating the following projects:

* [Envoy Proxy](https://github.com/hango-io/envoy-proxy)
* [Slime](https://github.com/slime-io/slime)
* [Istio](https://github.com/istio/istio)
* [Hango API Plane](https://github.com/hango-io/api-plane)
* [Hango Portal](https://github.com/hango-io/portal)
* [Hango UI](https://github.com/hango-io/ui)

For more details about each projects, please reference the link.
Any contributing should commit to the original repository.

## Installation

Hango Gateway can be installed on a Kubernetes cluster by using a Helm Chart.The following document will take you through the process of either Installation, verification, and remove the resource if necessary.

* [Hango Gateway Installation Guide](./install/README.md)

## Usage

We have provide user guide on UI, you can follow the guide to use Hango Gateway step by step.

![hango-ui](images/hango-ui.png)

Also, you can call the api privided by hango-portal. See [Expose api to Hango From API](./example/expose_api.md)

## Community

Hango Gateway is an open-source project, and welcomes any and all contributors. To get started:

* Mail List: Mail to hango.io@gmail.com, follow the reply to subscribe to the mailing list.
* QQ Group 914823850
* Check out the Hango documentation
* Read the [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) files.

If you're interested in contributing, here are some ways:

* Write a blog post for our blog
* Investigate an open issue
* Add more tests
* Contribute to the Docs

## License

[Apache-2.0](https://choosealicense.com/licenses/apache-2.0/)
