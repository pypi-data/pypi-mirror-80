import os
from typing import List, Dict

from dnry.config import ConfigFactory, IConfigFactory, IConfigSection
from dnry.config.in_memory import InMemorySource
from pyioc3 import StaticContainerBuilder

from dnry.config import helpers as config_helpers
from dnry.srvhost.builder.hosting_environment import HostingEnvironment
from dnry.srvhost.builder.noop_host import _NoopHost
from dnry.srvhost.builder.srv_host_context import SrvHostContext
from dnry.srvhost.builder.types import ISrvHostBuilder, ConfigConfigurationDelegate, ConfigServicesDelegate, \
    IHostingEnvironment, ISrvHostContext, ISrvHost


class SrvHostBuilder(ISrvHostBuilder):
    __settings: Dict[str, str]
    __configuration: IConfigSection
    __services: StaticContainerBuilder
    __hosting_environment: IHostingEnvironment
    __configuration_builder: IConfigFactory
    __ctx: ISrvHostContext
    __configDelegates: List[ConfigConfigurationDelegate]
    __serviceDelegates: List[ConfigServicesDelegate]

    def __init__(self, app_name: str, env_key: str = "SERVICE_ENV", **kwargs):

        if "configuration_builder" in kwargs:
            self.__configuration_builder = kwargs["configuration_builder"]
        else:
            self.__configuration_builder = ConfigFactory()

        if "hosting_environment" in kwargs:
            self.__hosting_environment = kwargs["hosting_environment"]
        else:
            self.__hosting_environment = HostingEnvironment(
                application_name=app_name,
                environment_name=os.environ.get(env_key, "Development"))

        self.__settings = dict()
        self.__configDelegates = list()
        self.__serviceDelegates = list()
        self.__configuration = self.__configuration_builder.build()
        self.__services = StaticContainerBuilder()
        self.__services.bind(
            annotation=ISrvHost,
            implementation=_NoopHost)

    def config_configuration(self, config: ConfigConfigurationDelegate) -> ISrvHostBuilder:
        self.__configDelegates.append(config)
        return self

    def config_services(self, config: ConfigServicesDelegate) -> ISrvHostBuilder:
        self.__serviceDelegates.append(config)
        return self

    def add_setting(self, key: str, value: str) -> ISrvHostBuilder:
        self.__settings[key] = value
        return self

    def get_setting(self, key: str):
        if key in self.__settings:
            return self.__settings[key]
        return self.__configuration.get(key)

    def build(self) -> ISrvHost:
        # If custom settings are set, rebuild configuration
        if len(self.__settings) > 0:
            self.__configuration_builder.add_source(InMemorySource(config_helpers.explode(self.__settings)))
            self.__configuration = self.__configuration_builder.build()

        # Create a context to start building
        self.__ctx = SrvHostContext(
            environment=self.__hosting_environment,
            configuration=self.__configuration)

        # Call the the configuration delegates
        for configDelegate in self.__configDelegates:
            configDelegate(self.__ctx, self.__configuration_builder)

        # Rebuild configuration after the config delegates have completed
        self.__configuration = self.__configuration_builder.build()
        self.__ctx.configuration = self.__configuration

        # Call the service container delegates
        for serviceDelegate in self.__serviceDelegates:
            serviceDelegate(self.__ctx, self.__services)

        # Add config into the container
        self.__services.bind_constant(
            annotation=IConfigSection,
            value=self.__ctx.configuration)

        # Add environment into the container
        self.__services.bind_constant(
            annotation=IHostingEnvironment,
            value=self.__ctx.environment)

        # Build the service provider
        service_provider = self.__services.build()

        # Get the service host out of the container
        host: ISrvHost = service_provider.get(ISrvHost)

        # Setup the service host
        host.service_provider = service_provider
        host.configuration = self.__ctx.configuration
        host.environment = self.__ctx.environment

        # All done
        return host
