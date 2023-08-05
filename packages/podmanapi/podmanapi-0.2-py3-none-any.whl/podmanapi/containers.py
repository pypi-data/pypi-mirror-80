"""API functions related to containers."""

import requests_unixsocket
import json

from podmanapi import api_endpoint

session = requests_unixsocket.Session()


def commit(container: str, **kwargs) -> str:
    """Create a new image form a container.

    :param container: the name or ID of a container
    :type container: str

    The following are optional parameters:
    repo: (str) the repository name for the created image
    tag: (str) tag name for the created image
    comment: (str) commit message
    author: (str) author of the image
    pause: (bool) pause the container before committing it.
    changes: (List[str]) instructions to apply while committing in Dockerfile format (i.e. "CMD=/bin/foo")
    format: (str) format of the image manifest and metadata (default "oci")

    :returns: JSON results
    """
    parameters = {key: value for key, value in kwargs.items()}
    parameters["container"] = container
    response = session.post(f"{api_endpoint}/commit", params=parameters)
    if response.status_code == 200:
        return "{'response': 200}"
    else:
        return response.json()


def health_check(container: str) -> str:
    """Execute the defined heatlcheck and return information about the results.

    :param container: the name or ID of the container
    :type container: str

    :returns: JSON results
    """
    return session.get(f"{api_endpoint}/containers/{container}/healthcheck").json()
