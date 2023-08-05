"""Wikipedia REST API client."""
from dataclasses import dataclass

import click
import desert
import marshmallow
import requests


@dataclass
class Page:
    """Page resource.

    Attributes:
        title: The title of the Wikipedia page
        extract: Plain text summary

    """

    title: str
    extract: str


schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


API_URL: str = "https://ja.wikipedia.org/api/rest_v1/page/random/summary"


def random_page() -> Page:
    """Return a random page in the Japanese Language.

    Performs a GET request to the JA page/random/summary endpoint

    Returns:
        A page resource

    Raises:
        ClickException: The HTTP request fails or HTTP response contains an invalid body

    """
    try:
        with requests.get(API_URL) as response:
            response.raise_for_status()
            return schema.load(response.json())
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)
