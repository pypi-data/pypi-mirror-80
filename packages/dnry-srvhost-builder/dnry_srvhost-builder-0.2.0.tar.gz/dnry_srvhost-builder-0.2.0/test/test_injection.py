import unittest

from dnry.config import IConfigSection
from pyioc3 import StaticContainerBuilder, Container

from dnry.srvhost.builder import SrvHostBuilder, ISrvHost, SrvHostBase, IHostingEnvironment


class HostMock(SrvHostBase):
    def run(self):
        pass


def setup_services(ctx, services: StaticContainerBuilder):
    services.bind(ISrvHost, HostMock)


class TestInjection(unittest.TestCase):
    def test_build_returns_my_host(self):
        host = SrvHostBuilder("ut") \
            .config_services(setup_services) \
            .build()
        self.assertIsInstance(host, HostMock)

    def test_build_returns_builtin_host(self):
        host = SrvHostBuilder("ut").build()
        self.assertIsInstance(host, ISrvHost)

    def test_host_has_service_provider(self):
        host = SrvHostBuilder("ut").build()
        self.assertIsInstance(host.service_provider, Container)

    def test_host_has_config(self):
        host = SrvHostBuilder("ut").build()
        self.assertIsInstance(host.configuration, IConfigSection)

    def test_host_has_environment(self):
        host = SrvHostBuilder("ut").build()
        self.assertIsInstance(host.environment, IHostingEnvironment)

    def test_host_has_app_name(self):
        host = SrvHostBuilder("ut").build()
        self.assertEqual(host.environment.application_name, "ut")

    def test_environment_defaults_to_development(self):
        host = SrvHostBuilder("ut").build()
        self.assertEqual(host.environment.environment_name, "Development")

    def test_environment_can_be_changed_by_variable(self):
        import os
        os.environ["SERVICE_ENV"] = "apples"
        host = SrvHostBuilder("ut").build()
        del os.environ["SERVICE_ENV"]
        self.assertEqual(host.environment.environment_name, "apples")

    def test_environment_can_use_alternative_environment_variable(self):
        import os
        os.environ["MY_SRV_HOST_ENV_FOR_UT"] = "bananas"
        host = SrvHostBuilder("ut", "MY_SRV_HOST_ENV_FOR_UT").build()
        self.assertEqual(host.environment.environment_name, "bananas")
