# A Quasar Spectra Scanning Tool

[![License MIT](https://img.shields.io/badge/License-MIT-blue.svg)](http://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/qscan.svg)](https://badge.fury.io/py/qscan)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.437903.svg)](https://doi.org/10.5281/zenodo.437903)

## Description

This program allows you to scan in velocity any quasar spectrum and with any transitions. This is very similar to RDGEN but with a more stable display. One can also select the fitting regions and prepare a preliminary `fort.13` in order to start fitting with VPFIT.

## Installation & Dependencies

The program can be installed very easily using the [pip Python package manager](https://pypi.org/project/pip/) as follows:

```bash
sudo pip install qscan
```

The program was built using the [Python Standard Library](https://docs.python.org/2/library/) as well as 4 external Python packages: [NumPy](http://www.numpy.org/), [Matplotlib](https://matplotlib.org/), [Astropy](http://www.astropy.org/) and [SciPy](https://www.scipy.org/).

## Usage

The usage is pretty straightforward and corresponds to the following:

```bash
qscan <spectrum> --option
```

## License

(The MIT License)

Copyright (c) 2016-2017 Vincent Dumont

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
