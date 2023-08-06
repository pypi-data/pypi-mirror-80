# ASFPy

A collection of Python scripts for the Application Statement Feedback Program's
logistic needs.

<!-- toc -->

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
  * [Packaging](#packaging)
  * [Authors](#authors)

<!-- tocstop -->

## Installation

This package requires Python 3.6+ and pip 20+, and recommends using the Python
3.8 runtime. To install, run 

```
pip install asfpy-aridyckovsky
```

## Usage 

Current usage requires importing the namespace directly:

```
from asfpy import asfpy
```

This can then be used to work with internal methods. For instance:

```
asfpy.allocate(applicants, editors)
```

will run the allocation algorithm, which returns a list of matchings between
applicants and two editors each. If two editors cannot be matched, the
applicant remains in an unmatched list.

## Contributing

### Packaging

Install via pip: `setuptools`, `wheel` and `twine`. Update version number in
`setup.py` before creating a new distribution.

From root of project, run `python setup.py sdist bdist_wheel` to create
distribution in `dist/*`. Then run `twine upload dist/*`.

### Authors

Ari Dyckovsky
