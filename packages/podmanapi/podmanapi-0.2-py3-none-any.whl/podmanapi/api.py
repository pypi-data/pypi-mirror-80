import requests_unixsocket

session = requests_unixsocket.Session()
api_endpoint = "http+unix://%2Frun%2Fpodman%2Fpodman.sock/v2.0.0/libpod"


def get_info():
    return session.get(f"{api_endpoint}/info").json()


def list_images():
    return session.get(f"{api_endpoint}/images/json").json()


if __name__ == "__main__":
    print(get_info())
    list_images()

# http://docs.podman.io/en/latest/_static/api.html
