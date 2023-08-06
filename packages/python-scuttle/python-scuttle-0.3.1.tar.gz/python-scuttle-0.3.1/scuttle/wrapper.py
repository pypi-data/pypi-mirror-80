#!/usr/bin/env python3

"""Provides methods to interface with a given API instance."""

import requests

from scuttle.versions import v1


def scuttle(wiki, api_key, api_version=1):
    """Create a new API wrapper for a given wiki and API version.

    str `wiki`: The domain of the wiki.
    str `api_key`: Your SCUTTLE API key.
    int `api_version`: The version of the API to use. If not provided, defaults
    to 1.
    """
    if api_version is None:
        raise NotImplementedError
    return ApiWrapper(wiki, api_key, api_version)


class ApiWrapper:
    def __init__(self, wiki, api_key, api_version):
        self.domain = wiki
        self.api_key = api_key
        self.version = api_version

        if self.version == 1:
            self.api = v1.Api(self.domain, self.api_key)
        else:
            raise ModuleNotFoundError(
                "API version {} does not exist.".format(self.version)
            )

    def __getattr__(self, attr):
        # Redirect attribute requests to api.
        # Where no such property exists, raise a verbose error.
        return getattr(self.api, attr)
