from abc import ABC, abstractmethod
from typing import Callable, NewType
from pyioc3 import StaticContainerBuilder, Container

from dnry.config import IConfigFactory, IConfigSection


class IHostingEnvironment(ABC):
    @property
    @abstractmethod
    def application_name(self) -> str:
        raise NotImplementedError()

    @application_name.setter
    @abstractmethod
    def application_name(self, val: str):
        raise NotImplementedError()

    @property
    @abstractmethod
    def environment_name(self) -> str:
        raise NotImplementedError()

    @environment_name.setter
    @abstractmethod
    def environment_name(self, val: str):
        raise NotImplementedError()


class ISrvHostContext(ABC):
    @property
    @abstractmethod
    def configuration(self) -> IConfigSection:
        raise NotImplementedError()

    @configuration.setter
    @abstractmethod
    def configuration(self, val: IConfigSection) -> IConfigSection:
        raise NotImplementedError()

    @property
    @abstractmethod
    def environment(self) -> IHostingEnvironment:
        raise NotImplementedError()

    @environment.setter
    @abstractmethod
    def environment(self, val: IHostingEnvironment):
        raise NotImplementedError()


class ISrvHost(ABC):
    @property
    @abstractmethod
    def service_provider(self) -> Container:
        raise NotImplementedError()

    @service_provider.setter
    @abstractmethod
    def service_provider(self, val: Container):
        raise NotImplementedError()

    @property
    @abstractmethod
    def configuration(self) -> IConfigSection:
        raise NotImplementedError()

    @configuration.setter
    @abstractmethod
    def configuration(self, val: IConfigSection):
        raise NotImplementedError()

    @property
    @abstractmethod
    def environment(self) -> IHostingEnvironment:
        raise NotImplementedError()

    @environment.setter
    @abstractmethod
    def environment(self, val: IHostingEnvironment):
        raise NotImplementedError()

    @abstractmethod
    def run(self, *args, **kwargs) -> any:
        raise NotImplementedError()


class ISrvHostBuilder(ABC):
    @abstractmethod
    def build(self) -> ISrvHost:
        raise NotImplementedError()

    @abstractmethod
    def config_configuration(self, config: "ConfigConfigurationDelegate") -> "ISrvHostBuilder":
        raise NotImplementedError()

    @abstractmethod
    def config_services(self, config: "ConfigServicesDelegate") -> "ISrvHostBuilder":
        raise NotImplementedError()

    @abstractmethod
    def add_setting(self, key: str, value: str) -> "ISrvHostBuilder":
        raise NotImplementedError()

    @abstractmethod
    def get_setting(self, key: str) -> str:
        raise NotImplementedError()


ConfigServicesDelegate = NewType("ConfigServicesDelegate", Callable[[ISrvHostContext], StaticContainerBuilder])
ConfigConfigurationDelegate = NewType("ConfigConfigurationDelegate", Callable[[ISrvHostContext], IConfigFactory])
