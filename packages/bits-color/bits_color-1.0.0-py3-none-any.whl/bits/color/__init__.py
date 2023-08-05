# -*- coding: utf-8 -*-
"""Color class file."""
import requests


class Color(object):
    """Color class."""

    def __init__(
        self,
        token,
        base_url="https://home.color.com/api/v1",
        populations=["Employees"],
        verbose=False
    ):
        """Initialize an Color class instance."""
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
        }
        self.populations = populations
        self.verbose = verbose

    def get_results(self, page_size=500, released_at_start=None, released_at_end=None):
        """Return results from the Color API."""
        url = f"{self.base_url}/populations/results"
        params = {
            "page_size": page_size,
            "populations": self.populations,
            "released_at_start": released_at_start,

        }
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()
        count = data.get("count")
        next_page = data.get("next")
        results = data.get("results", [])
        if self.verbose:
            print(f"Count of results: {count}")
            print(f"Next page URL: {next_page}")

        while next_page:
            response = requests.get(next_page, headers=self.headers)
            data = response.json()
            results.extend(data.get("results", []))
            next_page = data.get("next")
            if self.verbose:
                print(f"Next page URL: {next_page}")

        return results
