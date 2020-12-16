"""
Utilities used in handlers.
"""

import json
import os
import sys

from .version import SDK_VERSION

# Base URL to make requests against.
API_URL = "https://ipinfo.io"

# Used to transform incoming responses with country abbreviations into the full
# expanded country name, e.g. "PK" -> "Pakistan".
COUNTRY_FILE_DEFAULT = "countries.json"

# The max amount of IPs allowed by the API per batch request.
BATCH_MAX_SIZE = 1000


def get_headers(access_token):
    """Build headers for request to IPinfo API."""
    headers = {
        "user-agent": "IPinfoClient/Python{version}/{sdk_version}".format(
            version=sys.version_info[0], sdk_version=SDK_VERSION
        ),
        "accept": "application/json",
    }

    if access_token:
        headers["authorization"] = "Bearer {}".format(access_token)

    return headers


def format_details(details, countries):
    """
    Format details given a countries object.

    The countries object can be retrieved from read_country_names.
    """
    details["country_name"] = countries.get(details.get("country"))
    details["latitude"], details["longitude"] = read_coords(details.get("loc"))


def read_coords(location):
    """
    Given a location of the form `<lat>,<lon>`, returns the latitude and
    longitude as a tuple.

    Returns None for each tuple item if the form is invalid.
    """
    lat, lon = None, None
    coords = tuple(location.split(",")) if location else ""
    if len(coords) == 2 and coords[0] and coords[1]:
        lat, lon = coords[0], coords[1]
    return lat, lon


def read_country_names(countries_file=None):
    """
    Read list of countries from specified country file or
    default file.
    """
    if not countries_file:
        countries_file = os.path.join(
            os.path.dirname(__file__), COUNTRY_FILE_DEFAULT
        )
    with open(countries_file) as f:
        countries_json = f.read()

    return json.loads(countries_json)
