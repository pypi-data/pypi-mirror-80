"""API functions related to containers."""

import requests_unixsocket

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
    """Execute the defined healthcheck and return information about the results.

    :param container: the name or ID of the container
    :type container: str

    :returns: JSON results
    """
    return session.get(f"{api_endpoint}/containers/{container}/healthcheck").json()


def delete():
    pass


def attach():
    pass


def changes():
    pass


def checkpoint():
    pass


def copy_files_into():
    pass


def exists(container: str) -> str:
    """Determine whether container exists by name or ID.

    :param container: the name or ID of the container
    :type container: str

    :returns: JSON results
    """
    response = session.get(f"{api_endpoint}/containers/{container}/exists")
    if response.status_code == 204:
        return "{'response': 204}"
    else:
        return response.json()


def export_container():
    pass


def initialize():
    pass


def inspect(container: str, size: bool = False) -> str:
    """Return low-level information about a container.

    :param container: the name or ID of a container
    :type container: str
    :param size: (optional, default = False) If True, display filesystem usage
    :type size: bool

    :returns: JSON results
    """
    return session.get(f"{api_endpoint}/containers/{container}/json", params={"size": size}).json()


def kill():
    pass


def logs(container: str, **kwargs) -> str:
    """Get stdout and stderr logs from a container."""
    pass


def mount():
    pass


def pause():
    pass


def resize_tty():
    pass


def restart():
    pass


def restore():
    pass


def start():
    pass


def stats():
    pass


def stop():
    pass


def list_processes():
    pass


def umount():
    pass


def unpause():
    pass


def wait():
    pass


def create():
    pass


def list_containers():
    pass


def delete_stopped():
    pass


def show_mounted():
    pass


def generate_kubernetes_yaml():
    pass


def generate_systemd_unites():
    pass


def play_kubernetes_yaml():
    pass