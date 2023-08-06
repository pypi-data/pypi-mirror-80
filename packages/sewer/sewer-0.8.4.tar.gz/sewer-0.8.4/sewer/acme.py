"""
Sketching out what a clean reification of the JSON objects might look like.
"""

from typing import Dict, List, Tuple, Union

import requests

from .crypto import AcmeKey


class AcmeService:
    """
    An instance of AcmeService is intialized mostly from the directory_url.
    The timeouts in the args are mostly placeholders, and may turn out to be
    more appropriately part of some other object.

    NB: it is possible, but not really intended, that AcmeService will end up
    implementing most of the operations of the entire ACME protocol.  (see also
    memo-to-myself about nonces).
    """

    ### Let's Encrypt has no newAuthz endpoint

    resp_keys = ("newNonce", "newAccount", "newOrder", "newAuthz", "revokeCert", "keyChange")

    def __init__(
        self, *, directory_url: str, http_timeout: int = 10, process_timeout: int = 30
    ) -> None:
        self.http_timeout = http_timeout
        self.process_timeout = process_timeout
        response = requests.get(directory_url, timeout=http_timeout)

        ### TODO ### error handling (response failed AND missing endpoints, yeah)

        endpoints = {}
        respj = response.json()
        for k in respj:
            if k in self.resp_keys:
                endpoints[k] = respj[k]
        self.urls = endpoints

        ### TODO meta

    ### intrinsic operations

    def new_account(
        self,
        key: AcmeKey,
        *,
        contact: str = None,
        tos_agreed: bool = None,
        only_existing: bool = False,
    ) -> "AcmeAccount":
        raise NotImplementedError("new_account")

    def new_order(
        self,
        account: "AcmeAccount",
        identifiers: List[Tuple[str, str]],
        *,
        not_before: str = None,
        not_after: str = None,
    ) -> "AcmeOrder":
        raise NotImplementedError("new_order")

    def revoke_cert(self, *args, **kwargs):
        raise NotImplementedError("revoke_cert")

    def key_change(self, *args, **kwargs):
        raise NotImplementedError("key_change")

    memo = """
    How Should I Do... nonce harvesting.  Need to intercept all queries sent to
    this service in order to harvest nonces, but I'd rather not wire the
    implementation details of making the query (eg., requests, the user-agent,
    etc.) into AcmeService.

    2020-08-21 - leaning towards an AcmeHttps class that's instantiated with
    the service and user-agent (and timeouts?  more?) as part of the
    sewer-as-library using code.  But does that make Yet Another Thing that has
    to be juggled, passed in to too many functions, ...?  Perhaps still have
    that be its own object, but pass it to AcmeService?  Having the protocol
    send requests by invoking  service.POST(...)  does seem appropriate...
    """


class AcmeAccount:
    """
    An AcmeAccount is basically a suitable key which has been registered with
    a specific AcmeService.  Multiple keys can be registered with a service; a
    key may be registered with multiple services.  Each one would be a different
    instance of AcmeAccount.  So an async-ish driver program could have multiple
    accounts registered, each of which could have multiple orders active, ...
    in a single "session".  At least up to the point you started to run into
    the server's resource limits.

    As such, it is more or less assumed that an AcmeAccount is instantiated by
    anAcmeService.new_account(...), since that's where the key ID (kid) comes
    from (the kid is essential to the ACME protocol).
    """

    def __init__(self, *, key: AcmeKey, service: AcmeService, kid: str = None) -> None:
        self.key = key
        self.kid = kid
        self.service = service

    ### intrinsic operations

    # sign(message, sig_type?, ??) -> str or bytes?

    def jwk(self) -> Dict[str, str]:
        return self.key.jwk()


class AcmeOrder:
    """
    An AcmeOrder is created by the service's newOrder endpoint, and as for
    AcmeAccount it seems to make more sense to have the service's new_order
    method acting as a factory to create these things.
    """

    def __init__(
        self, *, location: str, json_resp: Dict[str, Union[str, List[str], List[Tuple[str]]]]
    ) -> None:
        """
        Accepts the JSON response from service.new_order as its initializer
        in part because the Order will need to be updated as the process
        progresses.  status changes, list of identifiers [to be validated]
        may change, ...  See update_status method.

        Oh right - get the Location header, too - that part's only on new_order?
        And preserving this url is the only way to compensate for LE's omission
        of the "inessential" orders attribute on account objects.
        """
        self.location = location
        self.update_from_json(json_resp)

    def update_order(self) -> str:
        """
        Updates the AcmeOrder's status (and ???) by querying location.  Returns
        ... okay, need to think about this.  There would only be something needed
        if there were an error?
        """
        raise NotImplementedError("AcmeOrder.update_order")

    def finalize(self, order: "AcmeOrder", csr: str) -> None:
        """
        Updates the order with the URL from which the certificate may be fetched.
        """
        raise NotImplementedError("AcmeOrder.finalize")

    def get_certificate(self) -> str:
        """
        Return the certificate at last!

        It will probably just do an update of the Order, which will add
        the "certificate" key.
        """
        raise NotImplementedError("AcmeOrder.get_certificate")

    ### internal implementation

    json_keys = {
        "status": True,
        "expires": None,
        "identifiers": True,
        "notBefore": None,
        "notAfter": None,
        "error": True,
        "authorizations": True,
        "finalize": True,
        "certificate": None,
    }

    required_keys = ("status", "identifiers", "authorizations", "finalize")

    def update_from_json(
        self, json_resp: Dict[str, Union[str, List[str], List[Tuple[str]]]]
    ) -> None:
        ...


def update_class_from_json(cls, json):
    raise NotImplementedError("update_class_from_json")
