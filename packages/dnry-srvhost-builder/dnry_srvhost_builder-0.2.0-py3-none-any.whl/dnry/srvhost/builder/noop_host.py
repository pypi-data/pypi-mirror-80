from dnry.srvhost.builder.srv_host_base import SrvHostBase


class _NoopHost(SrvHostBase):
    def run(self):
        print("No service host installed!")
        print(f"Please see {__name__} documentation.")
        exit(255)

