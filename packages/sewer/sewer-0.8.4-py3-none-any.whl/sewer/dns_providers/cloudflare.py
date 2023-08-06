import urllib.parse

import requests

from . import common
from ..lib import log_response


class CloudFlareDns(common.BaseDns):
    """
    """

    dns_provider_name = "cloudflare"

    def __init__(
        self,
        CLOUDFLARE_EMAIL=None,
        CLOUDFLARE_API_KEY=None,
        CLOUDFLARE_API_BASE_URL="https://api.cloudflare.com/client/v4/",
        CLOUDFLARE_TOKEN=None,
        **kwargs,
    ):
        self.CLOUDFLARE_DNS_ZONE_ID = None
        self.CLOUDFLARE_EMAIL = CLOUDFLARE_EMAIL
        self.CLOUDFLARE_API_KEY = CLOUDFLARE_API_KEY
        self.CLOUDFLARE_API_BASE_URL = CLOUDFLARE_API_BASE_URL
        self.CLOUDFLARE_TOKEN = CLOUDFLARE_TOKEN
        self.HTTP_TIMEOUT = 65  # seconds

        if CLOUDFLARE_API_BASE_URL[-1] != "/":
            self.CLOUDFLARE_API_BASE_URL = CLOUDFLARE_API_BASE_URL + "/"
        else:
            self.CLOUDFLARE_API_BASE_URL = CLOUDFLARE_API_BASE_URL

        # Either only pass a token or only the email and API key
        if not (
            (CLOUDFLARE_TOKEN and not CLOUDFLARE_EMAIL and not CLOUDFLARE_API_KEY)
            or (not CLOUDFLARE_TOKEN and CLOUDFLARE_EMAIL and CLOUDFLARE_API_KEY)
        ):
            raise ValueError(
                "Error initializing Cloudflare DNS adapter. Pass either email and API key or a token."
            )

        super().__init__(**kwargs)

    def find_dns_zone(self, domain_name):
        self.logger.debug("find_dns_zone")
        url = urllib.parse.urljoin(self.CLOUDFLARE_API_BASE_URL, "zones?status=active")
        headers = self._get_auth_header()
        find_dns_zone_response = requests.get(url, headers=headers, timeout=self.HTTP_TIMEOUT)
        self.logger.debug(
            "find_dns_zone_response. status_code={0}".format(find_dns_zone_response.status_code)
        )
        if find_dns_zone_response.status_code != 200:
            raise ValueError(
                "Error creating cloudflare dns record: status_code={status_code} response={response}".format(
                    status_code=find_dns_zone_response.status_code,
                    response=log_response(find_dns_zone_response),
                )
            )

        result = find_dns_zone_response.json()["result"]
        for i in result:
            if i["name"] in domain_name:
                setattr(self, "CLOUDFLARE_DNS_ZONE_ID", i["id"])
        if isinstance(self.CLOUDFLARE_DNS_ZONE_ID, type(None)):
            raise ValueError(
                "No DNS zone for %s: status = %s, response=%s"
                % (
                    domain_name,
                    find_dns_zone_response.status_code,
                    log_response(find_dns_zone_response),
                )
            )

        self.logger.debug("find_dns_zone_success")

    def create_dns_record(self, domain_name, domain_dns_value):
        self.logger.info("create_dns_record")
        self.find_dns_zone(domain_name)

        url = urllib.parse.urljoin(
            self.CLOUDFLARE_API_BASE_URL,
            "zones/{0}/dns_records".format(self.CLOUDFLARE_DNS_ZONE_ID),
        )
        headers = self._get_auth_header()
        body = {
            "type": "TXT",
            "name": "_acme-challenge" + "." + domain_name + ".",
            "content": "{0}".format(domain_dns_value),
        }
        create_cloudflare_dns_record_response = requests.post(
            url, headers=headers, json=body, timeout=self.HTTP_TIMEOUT
        )
        self.logger.debug(
            "create_cloudflare_dns_record_response. status_code={0}. response={1}".format(
                create_cloudflare_dns_record_response.status_code,
                log_response(create_cloudflare_dns_record_response),
            )
        )
        if create_cloudflare_dns_record_response.status_code != 200:
            # raise error so that we do not continue to make calls to ACME
            # server
            raise ValueError(
                "Error creating cloudflare dns record: status_code={status_code} response={response}".format(
                    status_code=create_cloudflare_dns_record_response.status_code,
                    response=log_response(create_cloudflare_dns_record_response),
                )
            )
        self.logger.info("create_dns_record_end")

    def delete_dns_record(self, domain_name, domain_dns_value):
        self.logger.info("delete_dns_record")

        class MockResponse(object):
            def __init__(self, status_code=200, content="mock-response"):
                self.status_code = status_code
                self.content = content
                super(MockResponse, self).__init__()

            def json(self):
                return {}

        delete_dns_record_response = MockResponse()
        headers = self._get_auth_header()

        dns_name = "_acme-challenge" + "." + domain_name
        list_dns_payload = {"type": "TXT", "name": dns_name}
        list_dns_url = urllib.parse.urljoin(
            self.CLOUDFLARE_API_BASE_URL,
            "zones/{0}/dns_records".format(self.CLOUDFLARE_DNS_ZONE_ID),
        )

        list_dns_response = requests.get(
            list_dns_url, params=list_dns_payload, headers=headers, timeout=self.HTTP_TIMEOUT
        )

        for i in range(0, len(list_dns_response.json()["result"])):
            dns_record_id = list_dns_response.json()["result"][i]["id"]
            url = urllib.parse.urljoin(
                self.CLOUDFLARE_API_BASE_URL,
                "zones/{0}/dns_records/{1}".format(self.CLOUDFLARE_DNS_ZONE_ID, dns_record_id),
            )
            headers = self._get_auth_header()
            delete_dns_record_response = requests.delete(
                url, headers=headers, timeout=self.HTTP_TIMEOUT
            )
            self.logger.debug(
                "delete_dns_record_response. status_code={0}. response={1}".format(
                    delete_dns_record_response.status_code, log_response(delete_dns_record_response)
                )
            )
            if delete_dns_record_response.status_code != 200:
                # extended logging for debugging
                # we do not need to raise exception
                self.logger.error(
                    "delete_dns_record_response. status_code={0}. response={1}".format(
                        delete_dns_record_response.status_code,
                        log_response(delete_dns_record_response),
                    )
                )

        self.logger.info("delete_dns_record_success")

    def _get_auth_header(self):
        if self.CLOUDFLARE_TOKEN:
            return {"Authorization": "Bearer " + self.CLOUDFLARE_TOKEN}
        else:
            return {"X-Auth-Email": self.CLOUDFLARE_EMAIL, "X-Auth-Key": self.CLOUDFLARE_API_KEY}
