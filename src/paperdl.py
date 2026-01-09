import requests

PROJECT_URL = "https://fill.papermc.io/v3/projects/paper/versions"
BUILD_URL_TEMPLATE = "https://fill.papermc.io/v3/projects/paper/versions/{}/builds/{}"


def get_latest_version_info() -> tuple[str, int]:
    """Returns (version_id, build_number)."""
    resp = requests.get(PROJECT_URL)
    resp.raise_for_status()
    data = resp.json()

    latest_ver = data["versions"][0]["version"]["id"]
    builds = data["versions"][0]["builds"]
    latest_build = builds[-1] # Last in the list
    return latest_ver, latest_build


def get_download_info(version: str, build: int) -> tuple[str, str]:
    """Returns (download_url, filename)."""
    url = BUILD_URL_TEMPLATE.format(version, build)
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    
    dl_info = data["downloads"]["server:default"]
    return dl_info["url"], dl_info["name"]


def download_file(url: str, path: str) -> None:
    """Download file from url to path."""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
