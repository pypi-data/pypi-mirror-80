import inspect
import logging
import sys
from dataclasses import dataclass, field
from typing import ClassVar, Mapping, Optional, Type

from ..errors import SAMLClientNotFound
from ..helpers import segment
from ..saml_clients.chooser import choose_saml_client


@dataclass
class GlobalOptions:
    saml_client_type: Type["SAMLClient"] = field(
        default_factory=lambda: choose_saml_client("auto", none_ok=True)
    )
    saml_clients: Mapping[str, "SAMLClient"] = field(default_factory=dict)

    debug: bool = False
    log_dir: Optional[str] = None

    def dprint(self, s: str):
        if s and self.debug:
            mod = inspect.getmodule(inspect.stack()[1][0])
            logging.getLogger(mod.__name__).debug(s)

    def create_saml_client(self, resource: str) -> "SAMLClient":
        if not self.saml_client_type:
            raise SAMLClientNotFound()
        segment.track("Resource Requested", resource=resource)
        if resource not in self.saml_clients:
            self.saml_clients[resource] = self.saml_client_type(resource, options=self)
        return self.saml_clients[resource]

    def to_dict(self):
        return {"debug": self.debug, "saml_client": str(self.saml_client_type)}
