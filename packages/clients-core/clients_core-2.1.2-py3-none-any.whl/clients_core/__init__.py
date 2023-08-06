__version__ = '2.1.2'
__package_name__ = 'clients_core'

__all__ = ["authentication", "SimpleRestClient", "SecuredRestClient", "RestClient", "ApiMatchClient", "ServiceDirectoryMatchClient", "GatewayMatchClient"]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from clients_core.simple_rest_client import SimpleRestClient
    from clients_core.secured_rest_client import SecuredRestClient
    from clients_core.rest_client import RestClient
    from clients_core.api_match_client import ApiMatchClient, ServiceDirectoryMatchClient, GatewayMatchClient
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
