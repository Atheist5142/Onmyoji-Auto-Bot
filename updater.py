import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from version import APP_VERSION, GITHUB_REPOSITORY


@dataclass
class UpdateInfo:
    current_version: str
    latest_version: str
    release_url: str


def _version_tuple(version):
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", version.strip())
    if not match:
        raise ValueError(f"Invalid release version: {version}")
    return tuple(int(part) for part in match.groups())


def check_for_update(timeout=5):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/releases/latest"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "OnmyojiAutoBot",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"GitHub API returned HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Cannot connect to GitHub: {error.reason}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError("GitHub returned invalid release data") from error

    tag_name = payload.get("tag_name")
    release_url = payload.get("html_url")
    if not isinstance(tag_name, str) or not isinstance(release_url, str):
        raise RuntimeError("GitHub release data is incomplete")

    current = _version_tuple(APP_VERSION)
    try:
        latest = _version_tuple(tag_name)
    except ValueError as error:
        raise RuntimeError(f"GitHub release has an invalid version: {tag_name}") from error
    return UpdateInfo(APP_VERSION, tag_name.lstrip("v"), release_url) if latest > current else None
