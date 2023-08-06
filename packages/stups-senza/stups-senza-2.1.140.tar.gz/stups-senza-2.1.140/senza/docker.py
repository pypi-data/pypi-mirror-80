"""
Functions to interact with docker
"""

import requests


def docker_image_exists(docker_image: str) -> bool:
    """
    Check whether the docker image exists by calling the Docker registry REST API
    """

    parts = docker_image.split('/')
    registry = parts[0]
    repo = '/'.join(parts[1:])
    repo, tag = repo.split(':')

    for scheme in 'https', 'http':
        try:
            url = '{scheme}://{registry}/v2/{repo}/tags/list'.format(scheme=scheme,
                                                                     registry=registry,
                                                                     repo=repo)
            response = requests.get(url, timeout=5)
            result = response.json()
            return tag in result.get('tags', [])
        except requests.RequestException:
            pass
    return False
