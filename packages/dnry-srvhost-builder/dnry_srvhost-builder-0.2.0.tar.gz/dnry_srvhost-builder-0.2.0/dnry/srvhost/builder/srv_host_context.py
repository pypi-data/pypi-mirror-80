from typing import Optional

from dnry.config import IConfigSection

from dnry.srvhost.builder.types import ISrvHostContext, IHostingEnvironment


class SrvHostContext(ISrvHostContext):
    __environment: Optional[IHostingEnvironment]
    __configuration: Optional[IConfigSection]

    def __init__(self, configuration: IConfigSection = None, environment: IHostingEnvironment = None):
        self.__environment = environment
        self.__configuration = configuration

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
