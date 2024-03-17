#!/usr/bin/env python3

# MIT License

# Copyright (c) 2023 MDAnalysis Development Team

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
Script to grab the compatible Python range for the latest develop branch of
MDAnalysis based on the classifiers entries in pyproject.toml.

$ ./get_mda_python_range.py
["3.9", "3.10", "3.11"]
$ ./get_mda_python_range.py --release 2.4.3
["3.8", "3.9", "3.10", "3.11"]
$ ./get_mda_python_range.py --exclude ["3.9", "3.11"]
["3.10"]
$ ./get_mda_python_range.py --exclude ["3.9"] --include ["3.8"]
["3.8", "3.10", "3.11"]
"""


import argparse
import urllib.request
import json
import tomllib


parser = argparse.ArgumentParser(
    description="Get Python versions compatible with MDAnalysis",
)
parser.add_argument(
    "--release",
    type=str,
    help="Specific release to extract pyproject.toml from",
    default=None,
)
parser.add_argument(
    "--exclude",
    type=str,
    help="JSON string of Python versions to exclude",
    default=None,
)
parser.add_argument(
    "--include",
    type=str,
    help="JSON string of Python versions to include",
    default=None,
)


def _grab_latest_release_version():
    """
    Slightly hacky way to get the package number from the url
    """
    url = 'https://github.com/MDAnalysis/mdanalysis/releases/latest'
    with urllib.request.urlopen(url) as response:
        output_url = response.url

    tag_name = output_url.split('/')[-1]
    # MDAnalysis relases under tags called package-version or release-version
    version = tag_name.split('-')[1]
    return version


def get_release_versions(release: str) -> list[str]:
    
    if release is None or release == 'develop':
        TOML_URL = "https://raw.githubusercontent.com/MDAnalysis/mdanalysis/develop/package/pyproject.toml"
    elif release == 'latest':
        version = _grab_latest_release_version()
        TOML_URL = f"https://raw.githubusercontent.com/MDAnalysis/mdanalysis/release-{version}/package/pyproject.toml"
    else:
        TOML_URL = f"https://raw.githubusercontent.com/MDAnalysis/mdanalysis/release-{release}/package/pyproject.toml"

    with urllib.request.urlopen(TOML_URL) as response:
        content = response.read().decode('utf-8')

    data = tomllib.loads(content)

    compat_versions = [
            v.split(' ')[-1]
            for v in data['project']['classifiers']
            if "Python ::" in v
    ]

    return compat_versions


def exclude_versions(versions: list[str], excludes: str) -> list[str]:
    # need to decode the exclude JSON array
    exclude_array = json.loads(excludes)
    return [i for i in set(versions) if i not in set(exclude_array)]

def include_versions(versions: list[str], includes: str) -> list[str]:
    # need to decode the include JSON array
    include_array = json.loads(includes)
    return list(set(include_array) | set(versions))


def check_include_exclude_overlap(includes: str, excludes: str) -> None:
    """
    Throw and error if include and exclude arrays overlap
    """
    exclude_array = json.loads(excludes)
    include_array = json.loads(includes)

    if len(set(exclude_array) & set(include_array)) > 0:
        errmsg = "identical entries in both include and exclude arrays"
        raise ValueError(errmsg)


def le_sort(versions: list[str]) -> list[str]:
    """
    Returns a sorted list of versions.
    """
    version_list = []
    for ver in versions:
        version_list.append((ver, int(ver.split('.')[0] + ver.split('.')[1])))

    return [i[0] for i in sorted(version_list, key=lambda x: x[1])]


if __name__ == "__main__":
    args = parser.parse_args()
    versions = get_release_versions(args.release)
    if args.exclude is not None:
        versions = exclude_versions(versions, args.exclude)
    if args.include is not None:
        if args.exclude is not None:
            check_include_exclude_overlap(args.include, args.exclude)
        versions = include_versions(versions, args.include)
    print(json.dumps(le_sort(versions)))
