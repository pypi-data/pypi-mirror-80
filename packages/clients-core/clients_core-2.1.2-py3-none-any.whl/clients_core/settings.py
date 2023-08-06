from typing import Union, Optional
import os
import ast
import logging
import dataclasses

logger = logging.getLogger(__name__)

_environment = None


@dataclasses.dataclass
class Environ:
    """
    Dataclass for holing environment variables with defaults
    """
    # Runtime variables
    DEBUG: bool = False
    LOG_LEVEL: int = logging.INFO
    SSL_VERIFY: bool = True
    REDIS_CONNECTION_URL: str = "redis://localhost:6379/0"

    # E360 configuration variables
    OIDC_CLIENT_ID: str = ''
    OIDC_CLIENT_SECRET: str = ''
    OIDC_TOKEN_ENDPOINT_URL: str = ''

    def __post_init__(self) -> None:
        """
        Collects any environment variables, and reassigns them in the class
        """
        for key, dtype in self.__annotations__.items():
            if key in os.environ:
                new_val = self._map_dtype(os.environ[key])
                setattr(self, key, dtype(new_val))

    @staticmethod
    def _map_dtype(d: str) -> Union[int, str, bool, None]:
        """
        Attempts to softly return intended data types
        """
        if d.isnumeric():
            return ast.literal_eval(d)
        elif d.lower() in ['true', 'false']:
            return ast.literal_eval(d.title())
        elif d.lower() in ['none', 'null']:
            return None
        return d


def get_environ(reload: bool = False) -> Optional[Environ]:
    """
    Function for a lazy loading of an Environ instance.
    reload (bool): forces the environment variables to be re-read.
    """
    if _environment is None or reload is True:
        globals()['_environment'] = Environ()
    return _environment
