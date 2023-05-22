# mdanalysis-compatible-python

A github action to extract the Python versions which MDAnalysis
is compatible with (based off the classifiers field in the project's
pyproject.toml).

Specificially it extracts:
  * The matrix of supported Python versions
  * The minimum supported Python version
  * The maximum supported Python version
  * The supported stable Python version (N-1)

The aim is that this action will be used to help generate
dynamic test matrices.

## Basic usage

Plese see [action.yaml]() for all details.

The following options can be passed:

1. `release`: an MDAnalysis release number (default is "develop" - the current develop branch head commit).
2. `include`: a JSON-like string formatted array of Python versions to specifically include in the output matrix.
3. `exclude`: a JSON-like string formatted array of Python versions to specifically exclude in the output matrix.


### Example:

The workflow detailed below uses the default output of this action to generate a dynamic matrix of Python versions.

**NOTE:** This action requires access to Python 3.11 or higher due to its tomllib dependency.

```yaml
jobs:
  python-config:
    runs-on: ubuntu-latest
    outputs:
      python-matrix: ${{ steps.get-compatible-python.outputs.python-versions }}
      stable-python: ${{ steps.get-compatible-python.outputs.stable-python }}
      latest-python: ${{ steps.get-compatible-python.outputs.latest-python }}
      oldest-python: ${{ steps.get-compatible-python.outputs.oldest-python }}
    steps:
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: get compatible python
        id: get-compatible-python
        uses: MDAnalysis/mdanalysis-compatible-python@main

  main-tests:
    needs: python-config
    runs-on: ubuntu-22.04
    strategy:
      matrix:
        python: ${{ fromJSON(needs.python-config.outputs.python-marix) }}
    steps:
      - uses: actions/setup-python@v4
        with:
          python-version: ${{matrix.python}}
```
