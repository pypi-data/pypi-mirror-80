from abc import ABC

from dnry.config import IConfigSection
from pyioc3 import Container

from dnry.srvhost.builder.types import ISrvHost, IHostingEnvironment


class SrvHostBase(ISrvHost, ABC):
    def __init__(self):
        self.__service_provider = None
        self.__configuration = None
        self.__environment = None

    @property
    def service_provider(self) -> Container:
        return self.__service_provider

    @service_provider.setter
    def service_provider(self, val: Container):
        self.__service_provider = val

    @property
    def configuration(self) -> IConfigSection:
        return self.__configuration

    @configuration.setter
    def configuration(self, val: IConfigSection):
        self.__configuration = val

    @property
    def environment(self) -> IHostingEnvironment:
        return self.__environment

    @environment.setter
    def environment(self, val: IHostingEnvironment):
        self.__environment = val
