"""
API client utilities for SmartShop AI Test Framework
"""

import json
from typing import Any, Dict, Optional, Union

import httpx
import requests
from loguru import logger

from src.core.constants import DEFAULT_TIMEOUT


class APIClient:
    """Generic API client for testing"""

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method, url=url, timeout=self.timeout, **kwargs
            )
            logger.info(f"{method.upper()} {url} - Status: {response.status_code}")
            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {method.upper()} {url} - Error: {e}")
            raise

    def get(
        self, endpoint: str, params: dict | None = None, **kwargs
    ) -> requests.Response:
        """Make GET request"""
        return self._make_request("GET", endpoint, params=params, **kwargs)

    def post(
        self,
        endpoint: str,
        data: dict | None = None,
        json_data: dict | None = None,
        **kwargs,
    ) -> requests.Response:
        """Make POST request"""
        return self._make_request("POST", endpoint, data=data, json=json_data, **kwargs)

    def put(
        self,
        endpoint: str,
        data: dict | None = None,
        json_data: dict | None = None,
        **kwargs,
    ) -> requests.Response:
        """Make PUT request"""
        return self._make_request("PUT", endpoint, data=data, json=json_data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request"""
        return self._make_request("DELETE", endpoint, **kwargs)

    def patch(
        self,
        endpoint: str,
        data: dict | None = None,
        json_data: dict | None = None,
        **kwargs,
    ) -> requests.Response:
        """Make PATCH request"""
        return self._make_request(
            "PATCH", endpoint, data=data, json=json_data, **kwargs
        )

    def set_auth_token(self, token: str):
        """Set authentication token"""
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Authentication token set")

    def set_headers(self, headers: dict[str, str]):
        """Set custom headers"""
        self.session.headers.update(headers)
        logger.info(f"Custom headers set: {headers}")

    def clear_headers(self):
        """Clear all custom headers"""
        self.session.headers.clear()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
        logger.info("Headers cleared")


class AsyncAPIClient:
    """Async API client for testing"""

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

    async def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> httpx.Response:
        """Make async HTTP request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = await self.client.request(method=method, url=url, **kwargs)
            logger.info(f"{method.upper()} {url} - Status: {response.status_code}")
            return response

        except httpx.RequestError as e:
            logger.error(f"Async request failed: {method.upper()} {url} - Error: {e}")
            raise

    async def get(
        self, endpoint: str, params: dict | None = None, **kwargs
    ) -> httpx.Response:
        """Make async GET request"""
        return await self._make_request("GET", endpoint, params=params, **kwargs)

    async def post(
        self,
        endpoint: str,
        data: dict | None = None,
        json_data: dict | None = None,
        **kwargs,
    ) -> httpx.Response:
        """Make async POST request"""
        return await self._make_request(
            "POST", endpoint, data=data, json=json_data, **kwargs
        )

    async def put(
        self,
        endpoint: str,
        data: dict | None = None,
        json_data: dict | None = None,
        **kwargs,
    ) -> httpx.Response:
        """Make async PUT request"""
        return await self._make_request(
            "PUT", endpoint, data=data, json=json_data, **kwargs
        )

    async def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        """Make async DELETE request"""
        return await self._make_request("DELETE", endpoint, **kwargs)

    async def patch(
        self,
        endpoint: str,
        data: dict | None = None,
        json_data: dict | None = None,
        **kwargs,
    ) -> httpx.Response:
        """Make async PATCH request"""
        return await self._make_request(
            "PATCH", endpoint, data=data, json=json_data, **kwargs
        )

    def set_auth_token(self, token: str):
        """Set authentication token"""
        self.client.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Authentication token set for async client")

    def set_headers(self, headers: dict[str, str]):
        """Set custom headers"""
        self.client.headers.update(headers)
        logger.info(f"Custom headers set for async client: {headers}")

    async def close(self):
        """Close async client"""
        await self.client.aclose()
        logger.info("Async API client closed")


def get_api_client(base_url: str) -> APIClient:
    """Factory function to get API client"""
    return APIClient(base_url)


def get_async_api_client(base_url: str) -> AsyncAPIClient:
    """Factory function to get async API client"""
    return AsyncAPIClient(base_url)
