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
Quick script to grab the latest version from an input matrix.
"""
import argparse
import json


parser = argparse.ArgumentParser(
    description="Get the latest version from input matrix",
)
parser.add_argument(
    "--matrix",
    type=str,
    help="JSON string of versions to inspect",
)
parser.add_argument(
    "--index",
    type=int,
    help="Rank index along sorted version list (reverse order)",
    default=0
)


def inspect_versions(versions: str) -> str:
    # need to decode the exclude JSON array
    versions_array = json.loads(versions)
    version_list = []
    for ver in versions_array:
        version_list.append((ver, int(ver.split('.')[0] + ver.split('.')[1])))

    return sorted(version_list, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    args = parser.parse_args()
    print(inspect_versions(args.matrix)[args.index][0])
