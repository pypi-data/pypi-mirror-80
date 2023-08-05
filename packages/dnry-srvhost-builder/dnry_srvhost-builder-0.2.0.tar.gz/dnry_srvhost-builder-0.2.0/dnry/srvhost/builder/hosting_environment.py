from typing import Optional

from dnry.srvhost.builder.types import IHostingEnvironment


class HostingEnvironment(IHostingEnvironment):
    __environment_name: Optional[str]
    __app_name: Optional[str]

    def __init__(self, application_name: str = None, environment_name: str = None):
        self.__app_name = application_name
        self.__environment_name = environment_name

    @property
    def application_name(self) -> str:
        return self.__app_name

    @application_name.setter
    def application_name(self, val: str):
        self.__app_name = val

    @property
    def environment_name(self) -> str:
        return self.__environment_name

    @environment_name.setter
    def environment_name(self, val: str):
        self.__environment_name = val
