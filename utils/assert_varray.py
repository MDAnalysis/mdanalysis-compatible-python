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
A quick script to compare two JSON version arrays
"""
import argparse
import json


parser = argparse.ArgumentParser(
    description="Compare two JSON version arrays",
)
parser.add_argument(
    "--input",
    type=str,
    help="JSON string of versions to inspect",
)
parser.add_argument(
    "--target",
    type=str,
    help="JSON string of expected versions",
)


def compare_versions(versions: str, target: str) -> None:
    # need to decode the exclude JSON array
    versions_array = json.loads(versions)
    print(versions_array)
    target_array = json.loads(target)
    print(target_array)

    for i, var in enumerate(versions_array):
        assert target_array[i] == var, f"unmatched array elements: {target_array[i]} {var}"

if __name__ == "__main__":
    args = parser.parse_args()
    compare_versions(args.input, args.target)
