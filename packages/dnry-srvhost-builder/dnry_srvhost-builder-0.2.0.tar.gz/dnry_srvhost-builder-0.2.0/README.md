# DNRY-SrvHost-Builder

A library for building a long running service in python.

This library is inspired by ASPNETCORE. This package provides a set of classes and interfaces that
simplify the initialization of a service by integrating configuration management from 
[dnry.config](https://pypi.org/project/dnry-config/) and container based dependency injection using
[pyioc3](https://pypi.org/project/pyioc3/). 

This library was intended as a platform on which to create long-running
services and reduce boiler plate code. You can create your own service host
use one from the DNRY.SrvHost library.

## Quick Start

Install dnry-srvhost-builder

```bash
pip install dnry-srvhost-builder
```

Create your own own service host

```python
from dnry.srvhost.builder import SrvHostBase

class AppHost(SrvHostBase):
    def run(self, *args, **kwargs):
        print('Do something cool!')
```

Build your program

```python
from dnry.config import IConfigFactory
from dnry.srvhost.builder import SrvHostBuilder, ISrvHostContext, ISrvHost
from pyioc3 import StaticContainerBuilder


def setup_config(ctx: ISrvHostContext, conf: IConfigFactory):
    # Add configuration files here
    pass


def setup_services(ctx: ISrvHostContext, services: StaticContainerBuilder):
    services.bind(
        annotation=ISrvHost,
        implementation=AppHost)

if __name__ == "__main__":
    SrvHostBuilder("App") \
        .config_configuration(setup_config) \
        .config_services(setup_services) \
        .build() \
        .run()
```

That's it! You are ready to build something cool. You can do much more

## How What?

in setup_service and setup_config. For information on how to use the
`IConfigFactory`, see the documentation at [en0/dnry-config](https://github.com/en0/dnry-config).
For more information on how to use `StaticContainerBuilder`, see the
documentation at [en0/pyioc3](https://github.com/en0/pyioc3).
