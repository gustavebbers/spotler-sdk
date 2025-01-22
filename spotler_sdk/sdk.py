# Copyright Gustav Ebbers
import hashlib
import json
from enum import Enum

import requests
from loguru import logger
from requests_oauthlib import OAuth1Session

from spotler_sdk.models import Contact, Order, OrderRequest, Product, ProductRequest

HTTP_TIMEOUT_SECONDS = 10


class SDK:
    def __init__(self, api_url: str, api_key: str, api_secret: str) -> None:
        self.api_url = api_url
        self.api_key = api_key
        self.api_secret = api_secret

        self.session = OAuth1Session(
            client_key=api_key,
            client_secret=api_secret,
        )

    def get_contact(self, email):

        hash = hashlib.sha256(email.encode()).hexdigest()
        try:
            r = self.session.get(
                self.api_url + f"contact/{hash}",
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=HTTP_TIMEOUT_SECONDS,
            )

            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `SpotlerSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 400:
                logger.debug(f"Contact: {email} not found with error: {r.json()['errorType']}")
                return None
            elif err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `SpotlerSDK.api_key` and `SpotlerSDK.api_secret` are set correctly"
                ) from err
            elif err.response.status_code == 404:
                logger.debug(f"Contact: {email} not found with error: {r.json()['errorType']}")
                return None
            else:
                raise

        return Contact(**r.json())

    def update_contact_property(self, email: str, key: str, value: str):

        hash = hashlib.sha256(email.encode()).hexdigest()
        payload = json.dumps(
            {
                "update": True,
                "purge": False,
                "contact": {
                    "externalId": hash,
                    "properties": {
                        key: value,
                    },
                    "channels": [],
                },
            }
        )
        try:
            r = self.session.put(
                self.api_url + f"contact/{hash}",
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=HTTP_TIMEOUT_SECONDS,
                data=payload,
            )

            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `SpotlerSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 400:
                logger.debug(f"Contact: {email} not updated with error: {r.json()['errorType']}")
                raise ValueError(r.json()["errorType"]) from err
            elif err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `SpotlerSDK.api_key` and `SpotlerSDK.api_secret` are set correctly"
                ) from err
            elif err.response.status_code == 404:
                logger.debug(f"Contact: {email} not updated with error: {r.json()['errorType']}")
                raise ValueError(r.json()["errorType"]) from err
            else:
                raise

    def create_order(self, order: Order):
        order_request = OrderRequest(order=order)
        try:
            r = self.session.post(
                self.api_url + "order",
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=HTTP_TIMEOUT_SECONDS,
                data=order_request.model_dump_json(),
            )

            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `SpotlerSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 400:
                raise ValueError(
                    f"Order: {order.externalId} not created with error: {r.json()['errorType']}:{r.json()['message']}"
                ) from err
            elif err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `SpotlerSDK.api_key` and `SpotlerSDK.api_secret` are set correctly"
                ) from err
            else:
                raise

    def update_order(self, order: Order):
        order_request = OrderRequest(order=order)
        try:
            r = self.session.put(
                self.api_url + f"order/{order.externalId}",
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=HTTP_TIMEOUT_SECONDS,
                data=order_request.model_dump_json(),
            )

            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `SpotlerSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 400:
                raise ValueError(
                    f"Order: {order.externalId} not created with error: {r.json()['errorType']}:{r.json()['message']}"
                ) from err
            elif err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `SpotlerSDK.api_key` and `SpotlerSDK.api_secret` are set correctly"
                ) from err
            else:
                raise

    def delete_order(self, order_id: str):
        try:
            r = self.session.delete(
                self.api_url + f"order/{order_id}",
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=HTTP_TIMEOUT_SECONDS,
            )

            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `SpotlerSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `SpotlerSDK.api_key` and `SpotlerSDK.api_secret` are set correctly"
                ) from err
            elif err.response.status_code == 404:
                raise ValueError(f"Order: {order_id} not found with error: {r.json()['errorType']}") from err
            else:
                raise

    def create_product(self, product: Product):
        product_request = ProductRequest(product=product)

        try:
            r = self.session.post(
                self.api_url + "product",
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=HTTP_TIMEOUT_SECONDS,
                data=product_request.model_dump_json(),
            )

            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `SpotlerSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `SpotlerSDK.api_key` and `SpotlerSDK.api_secret` are set correctly"
                ) from err
            elif err.response.status_code == 404:
                raise ValueError(
                    f"Product: {product.externalId} not found with error: {r.json()['errorType']}:{r.json()['message']}"
                ) from err
            else:
                raise

    def update_product(self, product: Product):
        product_request = ProductRequest(product=product)

        try:
            r = self.session.put(
                self.api_url + f"product/{product.externalId}",
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=HTTP_TIMEOUT_SECONDS,
                data=product_request.model_dump_json(),
            )

            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `SpotlerSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `SpotlerSDK.api_key` and `SpotlerSDK.api_secret` are set correctly"
                ) from err
            elif err.response.status_code == 404:
                raise ValueError(
                    f"Product: {product.externalId} not found with error: {r.json()['errorType']}:{r.json()['message']}"
                ) from err
            else:
                raise

    def delete_product(self, product_id: str):
        try:
            r = self.session.delete(
                self.api_url + f"product/{product_id}",
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=HTTP_TIMEOUT_SECONDS,
            )

            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `SpotlerSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `SpotlerSDK.api_key` and `SpotlerSDK.api_secret` are set correctly"
                ) from err
            elif err.response.status_code == 404:
                raise ValueError(
                    f"Product: {product_id} not found with error: {r.json()['errorType']}:{r.json()['message']}"
                ) from err
            else:
                raise

    def get_product(self, product_id: str):

        try:
            r = self.session.get(
                self.api_url + f"product/{product_id}",
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=HTTP_TIMEOUT_SECONDS,
            )

            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `SpotlerSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 400:
                logger.debug(
                    f"Product: {product_id} not found with error: {r.json()['errorType']}:{r.json()['message']}"
                )
                return None
            elif err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `SpotlerSDK.api_key` and `SpotlerSDK.api_secret` are set correctly"
                ) from err
            elif err.response.status_code == 404:
                logger.debug(
                    f"Product: {product_id} not found with error: {r.json()['errorType']}:{r.json()['message']}"
                )
                return None
            else:
                raise

        return Product(**r.json())
