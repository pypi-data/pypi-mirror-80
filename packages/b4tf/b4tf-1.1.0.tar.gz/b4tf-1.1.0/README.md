![img](https://img.shields.io/gitlab/pipeline/ymd_h/b4tf.svg)
![img](https://img.shields.io/pypi/v/b4tf.svg)
![img](https://img.shields.io/pypi/l/b4tf.svg)
![img](https://img.shields.io/pypi/status/b4tf.svg)
[![img](https://gitlab.com/ymd_h/b4tf/badges/master/coverage.svg)](https://ymd_h.gitlab.io/b4tf/coverage/)

![img](./site/static/images/logo.png)


# Overview

b4tf is a Python module providing a set of bayesian neural network on
[TensorFlow](https://www.tensorflow.org/).


# Installation

b4tf requires following softwares before installation

-   [TensorFlow 2.x](https://www.tensorflow.org/)
-   [TnesorFlow Probability](https://www.tensorflow.org/probability)
-   Python 3.x


## Install from [PyPI](https://pypi.org/) (Recommended)

The following command installs b4tf together with other dependancies.

    pip install b4tf

Depending on your environment, you might need `sudo` or `--user` flag
for installation.


## Install from source code

First, download source code manually or clone the repository;

    git clone https://gitlab.com/ymd_h/b4tf.git

Then you can install same way;

    cd b4tf
    pip install .


# Implemented Algorithms

Currently, b4tf implements following algorithms. We will implement
more.

-   Probabilistic Backpropagation (PBP) ([Paper](https://arxiv.org/abs/1502.05336), [Doc](https://ymd_h.gitlab.io/b4tf/algorithms/pbp), [API](https://ymd_h.gitlab.io/b4tf/api/b4tf.models.html#b4tf.models.PBP))
-   Monte Carlo Batch Normalization (MCBN) ([Paper](https://arxiv.org/abs/1802.06455), [Doc](https://ymd_h.gitlab.io/b4tf/algorithms/mcbn/), [API](https://ymd_h.gitlab.io/b4tf/api/b4tf.models.html#b4tf.models.MCBN))


# Contributing to b4tf

Any contribution are very welcome!


## Making Community Larger

Bigger commumity makes development more active and improve b4tf.

-   Star [this GitLab repository](https://gitlab.com/ymd_h/b4tf) (and/or [GitHub Mirror](https://github.com/ymd-h/b4tf))
-   Publish your code using b4tf
-   Share this repository to your friend and/or followers.


## Report Issue

When you have any problems or requests, you can check [issues on GitLab.com](https://gitlab.com/ymd_h/b4tf/issues).
If you still cannot find any information, you can open your own issue.


## Merge Request (Pull Request)

b4tf follows local rules:

-   Branch Name
    -   "HotFix<sub>\*</sub>\*\*" for bug fix
    -   "Feature<sub>\*</sub>\*\*" for new feature implementation
-   docstring
    -   Must for external API
    -   [Numpy Style](https://numpydoc.readthedocs.io/en/latest/format.html)
-   Unit Test
    -   Put test code under "test/" directory
    -   Can test by `python -m unittest <Your Test Code>` command
    -   Continuous Integration on GitLab CI configured by `.gitlab-ci.yaml`
-   Open an issue and associate it to Merge Request

Step by step instruction for beginners is described at [here](https://ymd_h.gitlab.io/b4tf/contributing/merge_request).


# Links


## b4tf sites

-   [Project Site](https://ymd_h.gitlab.io/b4tf/)
    -   [Class Reference](https://ymd_h.gitlab.io/b4tf/api/)
    -   [Unit Test Coverage](https://ymd_h.gitlab.io/b4tf/coverage/)
-   [Main Repository](https://gitlab.com/ymd_h/b4tf)
-   [GitHub Mirror](https://github.com/ymd-h/b4tf)
-   [b4tf on PyPI](https://pypi.org/project/b4tf/)


# Lisence

b4tf is available under MIT lisence.

    MIT License
    
    Copyright (c) 2020 Yamada Hiroyuki
    
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

